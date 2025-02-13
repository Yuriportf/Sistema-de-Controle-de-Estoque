from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pandas as pd
import io
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # Segurança das senhas
from models import db, Item, User

# Configuração do Flask
app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'sua_chave_secreta_super_segura')
app.config['SESSION_PERMANENT'] = False  # Garante que a sessão seja recriada corretamente
app.config['SESSION_TYPE'] = 'filesystem'  # Alternativa para evitar problemas de sessão

# Inicializando o banco de dados
db.init_app(app)

# Criando as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# ----------------- ROTAS E AUXILIARES -----------------


def calcular_valor_total():
    itens = Item.query.all()
    return sum(item.quantidade * item.preco for item in itens)

def calcular_total_itens():
    itens = Item.query.all()
    return sum(item.quantidade for item in itens if item.quantidade is not None)

@app.template_filter('formatar_valor')
def formatar_valor(valor):
    try:
        if valor is not None:
            return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        return 'R$ 0,00'
    except ValueError:
        return 'R$ 0,00'
# Função para obter um item específico pelo ID
def get_item_by_id(item_id):
    return Item.query.get(item_id)  # Utiliza o SQLAlchemy para buscar o item pelo ID


# ----------------- ROTAS PRINCIPAIS -----------------
@app.route('/index')
def index():
    if 'usuario' not in session:
        flash("Você precisa fazer login para acessar esta página!", "error")
        return redirect(url_for('login'))  # Redireciona para login se não estiver logado
    
    # Recupera os itens do banco de dados
    itens = Item.query.all()

    # Soma corretamente as quantidades dos itens
    total_itens = sum(item.quantidade for item in itens if item.quantidade is not None)

    # Calcula o valor total do estoque corretamente
    valor_total = sum((item.quantidade or 0) * (item.preco or 0) for item in itens)
    
    # Formata o valor total para exibição
    valor_total_formatado = "{:,.2f}".format(valor_total)  # Formato brasileiro (1.000,00)

    # Define se o botão deve ser mostrado ou não
    mostrar_botao = session.get('botao_ativado', False)

    return render_template(
        'index.html', 
        itens=itens, 
        total_itens=total_itens,  # Apenas a soma da coluna "quantidade"
        valor_total=valor_total_formatado, 
        mostrar_botao=mostrar_botao
    )



# Rota inicial
@app.route('/')
def home():
    return redirect(url_for('login'))  # Sempre leva para a tela de login ao acessar "/"

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        
        # Buscar o usuário no banco
        usuario = User.query.filter_by(nome=nome).first()
        
        # Verificar se o usuário existe e se a senha está correta
        if usuario:
            if usuario.check_password(senha):
                session['usuario'] = usuario.nome  # Cria a sessão com o nome do usuário
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for('estoque_total'))  # Redirecionar para a página de estoque total
            else:
                flash("Senha incorreta.", "error")
        else:
            flash("Usuário não encontrado.", "error")
    
    return render_template('login.html')  # Caso o método seja GET ou login falhe



# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da sua conta!", "info")
    return redirect(url_for('login'))


# Rota de registro de usuário
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash("As senhas não coincidem!", "error")
            return redirect(url_for('registro'))

        if User.query.filter_by(nome=nome).first() or User.query.filter_by(email=email).first():
            flash("Usuário ou e-mail já existe!", "error")
            return redirect(url_for('registro'))

        senha_hash = generate_password_hash(senha)  # Armazena senha de forma segura
        novo_usuario = User(nome=nome, email=email, senha_hash=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for('login'))

    return render_template('registro.html')


# Rota para exibir o estoque total
@app.route('/estoque_total', methods=['GET', 'POST'])
def estoque_total():
    itens = Item.query.all()  # Obtém todos os itens (alterei aqui)
    total_itens = len(itens)
    valor_total = sum(item.preco * item.quantidade for item in itens)  # Calculo do valor total

    mostrar_botao = True  # Defina a lógica para mostrar o botão de acordo com o contexto

    # Verifique se está sendo solicitado um item específico para alteração/remover
    item = None
    if 'item_id' in request.args:  # Verifica se um item_id foi passado na URL
        item_id = request.args['item_id']
        item = get_item_by_id(item_id)  # Chama a função corretamente passando o item_id

    return render_template('index.html', 
                           itens=itens, 
                           total_itens=total_itens, 
                           valor_total=formatar_valor(valor_total),
                           mostrar_botao=mostrar_botao, 
                           item=item)


# Função para adicionar item
@app.route('/adicionar', methods=['POST'])
def adicionar_item():
    try:
        # Captura os dados do formulário
        codigo = request.form.get('codigo', '').strip().upper()
        nome = request.form.get('nome', '').strip()
        quantidade = request.form.get('quantidade', type=int)
        preco = float(request.form.get('preco', '0').replace('.', '').replace(',', '.'))
        data_entrada = request.form.get('data_entrada', '')

        # Validação dos campos
        if not codigo or not nome or quantidade is None or quantidade < 0 or preco <= 0 or not data_entrada:
            flash('Preencha todos os campos corretamente!', 'error')
            return redirect(url_for('estoque_total'))  # Alterar 'index' para a rota correta

        # Verificação se o código já existe
        if Item.query.filter_by(codigo=codigo).first():
            flash('Código já existe no sistema!', 'error')
            return redirect(url_for('estoque_total'))  # Alterar 'index' para a rota correta

        # Processamento da data de entrada
        data_entrada = datetime.strptime(data_entrada, '%Y-%m-%d')

        # Criação do novo item e adição ao banco
        novo_item = Item(codigo=codigo, nome=nome, quantidade=quantidade, preco=preco, data_entrada=data_entrada)
        db.session.add(novo_item)
        db.session.commit()

        # Sucesso
        flash('Item adicionado com sucesso!', 'success')
    except Exception as e:
        # Em caso de erro, desfaz a transação
        db.session.rollback()
        flash(f'Erro ao adicionar item: {str(e)}', 'error')

    # Redireciona para a página de estoque_total
    return redirect(url_for('estoque_total'))  # Alterar 'index' para a rota correta

@app.route('/localizar', methods=['POST'])
def localizar_item():
    termo = request.form.get('termo', '').strip()

    if termo.isalnum():
        itens = Item.query.filter((Item.codigo == termo) | (Item.nome.ilike(f'%{termo}%'))).all()
    else:
        itens = Item.query.filter(Item.nome.ilike(f'%{termo}%')).all()
    
    total_itens = sum(item.quantidade for item in itens)  # Agora reflete apenas os itens pesquisados

    session['botao_ativado'] = bool(itens)

    return render_template('index.html', 
                           itens=itens, 
                           total_itens=total_itens,  # Agora está correto
                           valor_total=formatar_valor(calcular_valor_total()), 
                           mostrar_botao=True)




@app.route('/remover', methods=['POST'])
def remover():
    # Recuperando os dados do formulário
    codigo_item = request.form.get('codigo_item', '').strip()
    nome_item = request.form.get('nome_item', '').strip()
    confirmacao = request.form.get('confirmacao_remover', '').strip()
    remover_todos = request.form.get('remover_todos')  # Verificando se a caixa para remover todos foi marcada

    # Verifica se a confirmação foi "sim"
    if confirmacao != 'sim':
        flash("A remoção precisa ser confirmada digitando 'sim'.", "error")
        return redirect(url_for('index'))  # Redireciona caso não tenha confirmado corretamente

    # Se a checkbox "Remover todos os itens" foi marcada
    if remover_todos:
        try:
            all_items = Item.query.all()  # Obtém todos os itens
            if all_items:
                for item in all_items:
                    db.session.delete(item)  # Remove cada item
                db.session.commit()  # Commit para salvar as alterações
                flash("Todos os itens foram removidos com sucesso!", "success")
            else:
                flash("Nenhum item no estoque para ser removido.", "error")
        except Exception as e:
            db.session.rollback()  # Em caso de erro, reverte a transação
            flash(f"Erro ao remover todos os itens: {str(e)}", "error")

    else:
        # Se não for para remover todos, tenta remover um item específico
        item_removido = None
        try:
            if codigo_item:
                item_removido = Item.query.filter_by(codigo=codigo_item).first()  # Procurando pelo código do item
            elif nome_item:
                item_removido = Item.query.filter(Item.nome.ilike(f"%{nome_item}%")).first()  # Procurando pelo nome do item

            if item_removido:
                db.session.delete(item_removido)
                db.session.commit()  # Commit para salvar as alterações
                flash(f"Item '{item_removido.nome}' removido com sucesso!", "success")
            else:
                flash("Item não encontrado para remoção.", "error")
        except Exception as e:
            db.session.rollback()  # Em caso de erro, reverte a transação
            flash(f"Erro ao remover item: {str(e)}", "error")

    return redirect(url_for('index'))  # Redireciona para a página principal ou de estoque



@app.route('/alterar', methods=['POST'])
def alterar():
    codigo_item = request.form.get('codigo_item', '').strip()

    if not codigo_item:
        flash("O código do item é obrigatório para alteração.", "error")
        return redirect(url_for('index'))  # ou a página que exibe os itens

    item_encontrado = Item.query.filter_by(codigo=codigo_item).first()

    if not item_encontrado:
        flash(f"Item com código '{codigo_item}' não encontrado.", "error")
        return redirect(url_for('index'))  # Redireciona caso o item não exista

    # Obter os dados de alteração
    nome_item = request.form.get('nome_item', '').strip()
    quantidade = request.form.get('quantidade', '').strip()
    preco = request.form.get('preco', '').strip()
    tipo_item = request.form.get('tipo_item', '').strip()

    # Atualiza os campos apenas se o valor não estiver vazio
    if nome_item:
        item_encontrado.nome = nome_item
    if quantidade.isdigit() and int(quantidade) >= 0:
        item_encontrado.quantidade = int(quantidade)
    if preco.replace('.', '', 1).isdigit() and float(preco) >= 0:
        item_encontrado.preco = float(preco)
    if tipo_item:
        item_encontrado.tipo = tipo_item

    try:
        item_encontrado.preco_total = item_encontrado.quantidade * item_encontrado.preco
        db.session.commit()
        flash(f"Item '{item_encontrado.nome}' alterado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao alterar item: {str(e)}", "error")

    return redirect(url_for('index'))  # Redireciona após a alteração



# Função para exportar itens
@app.route('/exportar', methods=['POST'])
def exportar_itens():
    itens = Item.query.all()
    data = [item.to_dict() for item in itens]  # Agora pode chamar item.to_dict() sem erro
    df = pd.DataFrame(data)

    # Criação de um arquivo CSV em memória
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')
    csv_file.seek(0)

    return send_file(io.BytesIO(csv_file.getvalue().encode('utf-8-sig')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='itens.csv')

# Função para importar itens
@app.route('/importar', methods=['POST'])
def importar_itens():
    if 'file' not in request.files:
        flash("Nenhum arquivo enviado.", "error")
        return redirect(url_for('estoque_total'))

    file = request.files['file']
    if file.filename == '':
        flash("Nenhum arquivo selecionado.", "error")
        return redirect(url_for('estoque_total'))

    if file and file.filename.endswith('.csv'):
        try:
            # Tenta detectar o delimitador automaticamente
            df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8-sig')

            # Normaliza os nomes das colunas
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

            # Usa todas as colunas disponíveis no CSV
            colunas_disponiveis = df.columns.to_list()

            for _, row in df.iterrows():
                codigo = row.get(colunas_disponiveis[0])
                nome = row.get(colunas_disponiveis[1])
                quantidade = row.get(colunas_disponiveis[2])
                preco = row.get(colunas_disponiveis[3])
                data_entrada = row.get(colunas_disponiveis[4])

                try:
                    data_entrada = pd.to_datetime(data_entrada, errors='coerce').date()
                    if pd.isna(data_entrada):
                        flash(f"Data inválida para o item {nome}.", "warning")
                        continue
                except Exception:
                    flash(f"Erro ao processar a data do item {nome}.", "warning")
                    continue

                # Verifica se o item já existe no banco
                if not Item.query.filter_by(codigo=codigo).first():
                    item = Item(codigo=codigo, nome=nome, quantidade=quantidade, preco=preco, data_entrada=data_entrada)
                    db.session.add(item)

            db.session.commit()
            flash("Itens importados com sucesso!", "success")

        except Exception as e:
            flash(f"Erro ao importar itens: {str(e)}", "error")
            db.session.rollback()

    return redirect(url_for('estoque_total'))


if __name__ == '__main__':
    app.run(debug=True)
