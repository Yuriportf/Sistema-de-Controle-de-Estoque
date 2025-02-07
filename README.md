# Sistema de Controle de Estoque

Este projeto é um sistema de controle de estoque simples e eficiente, desenvolvido com Python, utilizando o framework **Flask** para a criação da aplicação web e o **SQLAlchemy** para interagir com um banco de dados SQLite. O sistema permite gerenciar itens de estoque, com funcionalidades de adicionar, alterar, remover e visualizar itens. Além disso, inclui a possibilidade de importar e exportar dados no formato CSV.

## Tecnologias Utilizadas

### Frameworks

1. **Flask**
   - **Descrição**: Flask é um microframework web para Python, fácil de usar e bem flexível, adequado para a criação de pequenas e médias aplicações web.
   - **Função no Projeto**: Usado para gerenciar as rotas da aplicação e fornecer a estrutura para a interação entre o servidor e os usuários. Ele cuida das requisições HTTP e renderiza templates HTML dinâmicos.

2. **Flask-SQLAlchemy**
   - **Descrição**: Uma extensão do Flask para integração com bancos de dados relacionais, utilizando o ORM SQLAlchemy.
   - **Função no Projeto**: Usado para conectar e interagir com o banco de dados SQLite. Ele mapeia a tabela do banco de dados para objetos Python, facilitando as operações CRUD (criar, ler, atualizar e excluir) de maneira intuitiva.

### Bibliotecas

1. **SQLAlchemy**
   - **Descrição**: SQLAlchemy é um ORM (Object-Relational Mapper) que facilita a comunicação com bancos de dados relacionais, permitindo manipular dados como objetos Python.
   - **Função no Projeto**: Usado para criar e manipular os dados armazenados na tabela `Item`, que armazena informações sobre os itens do estoque, como código, nome, quantidade e preço.

2. **Pandas**
   - **Descrição**: Pandas é uma biblioteca poderosa para análise e manipulação de dados, especialmente útil para trabalhar com tabelas e CSVs.
   - **Função no Projeto**: Usado para importar e exportar dados do estoque em arquivos CSV. Ao importar, os dados são convertidos para um formato manipulado (DataFrame), e ao exportar, eles são convertidos de volta para CSV.

3. **Locale**
   - **Descrição**: A biblioteca `locale` permite que você formate números, datas e outros valores de acordo com as convenções regionais.
   - **Função no Projeto**: Usada para formatar valores monetários no padrão brasileiro (R$), proporcionando uma melhor experiência para o usuário.

4. **datetime**
   - **Descrição**: A biblioteca `datetime` fornece funções para manipulação e formatação de datas e horas.
   - **Função no Projeto**: Usada para registrar a data de entrada dos itens no estoque e para formatar as datas na interface.

5. **os**
   - **Descrição**: Biblioteca padrão do Python que fornece uma maneira de interagir com o sistema operacional.
   - **Função no Projeto**: Usada para acessar variáveis de ambiente, como a chave secreta do Flask, com o intuito de garantir maior segurança.

---

## Funcionalidades

O sistema de controle de estoque oferece várias funcionalidades para o gerenciamento dos itens do estoque. Aqui estão algumas das principais:

### 1. **Visualização de Itens**
   - A página inicial (`/`) exibe todos os itens cadastrados no estoque, incluindo o código, nome, quantidade, preço e a data de entrada.
   - Também são exibidos o total de itens no estoque e o valor total calculado com base nas quantidades e preços dos itens.

### 2. **Adicionar Itens ao Estoque**
   - Na página inicial, o usuário pode adicionar um novo item, preenchendo um formulário com o código, nome, quantidade, preço e data de entrada.
   - O sistema verifica se o código do item já existe, evitando duplicação.

### 3. **Alterar ou Remover Itens**
   - Itens podem ser alterados ou removidos com base no código fornecido.
   - A alteração permite modificar os campos do item, enquanto a remoção apaga completamente o item do banco de dados.

### 4. **Pesquisar Itens**
   - Os usuários podem pesquisar itens pelo nome ou código. Quando a pesquisa retorna resultados, o botão de "voltar ao estoque total" é ativado.

### 5. **Importar e Exportar Dados**
   - **Importar**: Os usuários podem importar itens de um arquivo CSV. O sistema irá verificar e adicionar os itens ao banco de dados, ignorando os itens com códigos já existentes.
   - **Exportar**: O sistema permite exportar todos os itens do estoque para um arquivo CSV, que pode ser baixado pelo usuário.

### 6. **Visibilidade do Botão "Voltar ao Estoque Total"**
   - O botão de "voltar ao estoque total" é exibido somente quando uma pesquisa retorna resultados, permitindo que o usuário volte à lista completa de itens.

---

## Lógica do Código

### Configuração e Banco de Dados

O Flask é configurado para usar um banco de dados SQLite, armazenando os dados de estoque na tabela `Item`. A configuração do banco de dados é feita com SQLAlchemy, e a tabela `Item` tem os seguintes campos:
- `id`: Identificador único do item (chave primária).
- `codigo`: Código único do item.
- `nome`: Nome do item.
- `quantidade`: Quantidade de itens disponíveis no estoque.
- `preco`: Preço unitário do item.
- `data_entrada`: Data de entrada do item no estoque.

Quando o aplicativo é iniciado, a tabela `Item` é criada no banco de dados, se ainda não existir.

### Funções Principais

- **calcular_total_itens**: Calcula o número total de itens no estoque somando as quantidades de todos os itens.
- **calcular_valor_total**: Calcula o valor total do estoque multiplicando a quantidade de cada item pelo seu preço unitário e somando os resultados.
- **formatar_valor**: Formata os valores monetários para o padrão brasileiro, exibindo-os como `R$ X,XX`.

### Rotas

- **`/`**: Página inicial que exibe todos os itens do estoque e o total de itens e valor total.
- **`/estoque_total`**: Exibe todos os itens do estoque, com a possibilidade de voltar para a visualização total ou realizar uma pesquisa.
- **`/ativar_botao`**: Ativa o botão de "voltar ao estoque total".
- **`/localizar`**: Realiza uma pesquisa por nome ou código de item.
- **`/adicionar`**: Adiciona um novo item ao estoque.
- **`/alterar_ou_remover`**: Permite alterar ou remover um item do estoque com base no código.
- **`/importar`**: Importa itens de um arquivo CSV para o estoque.
- **`/exportar`**: Exporta todos os itens do estoque para um arquivo CSV.

