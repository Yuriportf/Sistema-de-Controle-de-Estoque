from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pandas as pd
import io
import os
import locale
from datetime import datetime

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'sua_chave_secreta_super_segura')

db = SQLAlchemy(app)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)  # Preço unitário
    data_entrada = db.Column(db.Date, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def calcular_total_itens():
    return db.session.query(func.sum(Item.quantidade)).scalar() or 0

def calcular_valor_total():
    return db.session.query(func.sum(Item.quantidade * Item.preco)).scalar() or 0.0

@app.template_filter('formatar_valor')
def formatar_valor(valor):
    try:
        return locale.currency(valor, grouping=True) if valor else 'R$ 0,00'
    except ValueError:
        return 'R$ 0,00'

@app.route('/')
def index():
    itens = Item.query.all()
    total_itens = calcular_total_itens()
    valor_total = calcular_valor_total()

    # Controlar a visibilidade do botão com base na sessão
    mostrar_botao = 'botao_ativado' in session and session['botao_ativado']

    return render_template('index.html', itens=itens, total_itens=total_itens, valor_total=formatar_valor(valor_total), mostrar_botao=mostrar_botao)

@app.route('/estoque_total', methods=['GET', 'POST'])
def estoque_total():
    itens = Item.query.all()
    total_itens = calcular_total_itens()
    valor_total = calcular_valor_total()

    # Controlar a visibilidade do botão com base na sessão
    mostrar_botao = 'botao_ativado' in session and session['botao_ativado']

    return render_template('index.html', 
                           itens=itens, 
                           total_itens=total_itens, 
                           valor_total=formatar_valor(valor_total),
                           mostrar_botao=mostrar_botao)

@app.route('/ativar_botao')
def ativar_botao():
    # Quando o botão for clicado, guardamos na sessão que ele foi ativado
    session['botao_ativado'] = True
    return redirect(url_for('estoque_total'))

@app.route('/voltar_ao_estoque_total')
def voltar_ao_estoque_total():
    # Limpar a variável de sessão que controla a visibilidade do botão
    session.pop('botao_ativado', None)
    return redirect(url_for('index'))  # Redireciona para a página inicial

@app.route('/localizar', methods=['POST'])
def localizar_item():
    termo = request.form.get('termo', '').strip()
    itens = Item.query.filter(Item.nome.ilike(f'%{termo}%') | Item.codigo.ilike(f'%{termo}%')).all()

    # Quando realizar uma pesquisa, o botão de voltar aparece
    session['botao_ativado'] = bool(itens)  # O botão só será ativado se houver resultados
    return render_template('index.html', 
                           itens=itens, 
                           total_itens=calcular_total_itens(), 
                           valor_total=formatar_valor(calcular_valor_total()), 
                           mostrar_botao=True)

@app.route('/adicionar', methods=['POST'])
def adicionar_item():
    try:
        codigo = request.form.get('codigo', '').strip().upper()
        nome = request.form.get('nome', '').strip()
        quantidade = request.form.get('quantidade', type=int)
        
        # Ajuste para lidar com vírgula e ponto
        preco = float(request.form.get('preco', '0').replace('.', '').replace(',', '.'))
        
        data_entrada = request.form.get('data_entrada', '')

        if not codigo or not nome or quantidade is None or quantidade < 0 or preco <= 0 or not data_entrada:
            flash('Preencha todos os campos corretamente!', 'error')
            return redirect(url_for('index'))

        if Item.query.filter_by(codigo=codigo).first():
            flash('Código já existe no sistema!', 'error')
            return redirect(url_for('index'))

        data_entrada = datetime.strptime(data_entrada, '%Y-%m-%d')
        novo_item = Item(codigo=codigo, nome=nome, quantidade=quantidade, preco=preco, data_entrada=data_entrada)
        db.session.add(novo_item)
        db.session.commit()
        flash('Item adicionado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao adicionar item: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/alterar_ou_remover', methods=['POST'])
def alterar_ou_remover():
    codigo = request.form.get('codigo', '').strip().upper()
    nome = request.form.get('nome', '').strip()
    quantidade = request.form.get('quantidade', type=int)
    
    # Ajuste para lidar com vírgula e ponto
    preco = float(request.form.get('preco', '0').replace('.', '').replace(',', '.'))
    
    confirmacao = request.form.get('confirmacao', '').strip().upper()

    if not codigo or not nome or quantidade is None or quantidade < 0 or preco <= 0:
        flash('Preencha todos os campos corretamente!', 'error')
        return redirect(url_for('index'))

    item = Item.query.filter_by(codigo=codigo).first()

    if not item:
        flash('Item não encontrado!', 'error')
        return redirect(url_for('index'))

    if confirmacao == 'SIM':
        if request.form.get('acao') == 'alterar':
            # Atualizar apenas os campos permitidos
            item.nome = nome
            item.quantidade = quantidade
            item.preco = preco
            db.session.commit()
            flash('Item alterado com sucesso!', 'success')

        elif request.form.get('acao') == 'remover':
            db.session.delete(item)
            db.session.commit()
            flash('Item removido com sucesso!', 'success')

        else:
            flash('Ação inválida!', 'error')
    else:
        flash('Você precisa confirmar digitando "SIM".', 'error')

    return redirect(url_for('index'))

@app.route('/importar', methods=['POST'])
def importar_itens():
    arquivo = request.files.get('arquivo')
    if not arquivo:
        flash('Selecione um arquivo para importar!', 'error')
        return redirect(url_for('index'))

    try:
        # Carregar arquivo CSV para DataFrame
        df = pd.read_csv(arquivo)

        for _, row in df.iterrows():
            codigo = row.get('codigo', '').strip().upper()
            nome = row.get('nome', '').strip()
            quantidade = int(row.get('quantidade', 0))
            
            # Ajuste para lidar com vírgula e ponto
            preco = float(str(row.get('preco', 0)).replace('.', '').replace(',', '.'))
            
            data_entrada = datetime.strptime(row.get('data_entrada', ''), '%Y-%m-%d')

            if Item.query.filter_by(codigo=codigo).first():
                continue  # Ignorar itens com código já existente
            item = Item(codigo=codigo, nome=nome, quantidade=quantidade, preco=preco, data_entrada=data_entrada)
            db.session.add(item)
        db.session.commit()
        flash('Itens importados com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao importar itens: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/exportar', methods=['POST'])
def exportar_itens():
    # Obter todos os itens do estoque
    itens = Item.query.all()
    data = [{
        'codigo': item.codigo,
        'nome': item.nome,
        'quantidade': item.quantidade,
        'preco': item.preco,
        'data_entrada': item.data_entrada.strftime('%Y-%m-%d') if item.data_entrada else ''
    } for item in itens]

    # Converter para DataFrame
    df = pd.DataFrame(data)

    # Salvar em CSV com separação correta
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')
    csv_file.seek(0)

    return send_file(io.BytesIO(csv_file.getvalue().encode('utf-8-sig')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='itens.csv')

if __name__ == '__main__':
    app.run(debug=True)
