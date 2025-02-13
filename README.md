# 📊 Sistema de Gestão de Estoque com Flask

Este é um sistema simples de **gestão de estoque** desenvolvido com **Flask**, **SQLAlchemy** e **SQLite**. A aplicação permite realizar o controle de itens de estoque, oferecendo uma interface para cadastro, consulta e atualização dos itens de maneira eficiente e intuitiva.

## ⚙️ Frameworks Utilizados

- **Flask**: Framework web minimalista para Python, utilizado para construir a aplicação e gerenciar as rotas e a lógica de negócios.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para gerenciar a conexão e as operações no banco de dados de forma simples e eficiente.
- **SQLite**: Banco de dados relacional embutido, utilizado para armazenar as informações de itens no estoque.

## 📚 Bibliotecas Utilizadas

As principais bibliotecas do projeto são:

- **Flask**: Para a construção da aplicação web.
    ```bash
    pip install Flask
    ```

- **Flask-SQLAlchemy**: Para facilitar a integração do Flask com o banco de dados SQLite.
    ```bash
    pip install Flask-SQLAlchemy
    ```

- **Werkzeug**: Para o gerenciamento seguro de senhas e criptografia de dados sensíveis.
    ```bash
    pip install Werkzeug
    ```

- **SQLite3**: Para gerenciar o banco de dados local (já incluído no Python por padrão).

## 🎨 Visual e Estilo

O design do sistema é baseado em um esquema de cores escuras com um visual moderno, e inclui animações suaves para melhorar a experiência do usuário. 

Aqui estão os principais aspectos do layout:

- **Cor de fundo**: Utilização de um gradiente de tons escuros, criando uma aparência moderna e agradável.
- **Animações de Transição**: Elementos da interface, como cabeçalhos e caixas de mensagens, possuem animações suaves para uma navegação mais fluida.
- **Responsividade**: O layout é totalmente responsivo, adaptando-se a diferentes dispositivos, seja desktop ou mobile, para garantir a melhor experiência em qualquer tamanho de tela.

## 🚀 Funcionalidades

O sistema oferece diversas funcionalidades para facilitar a gestão do estoque:

- 📝 **Cadastro de Itens**: Permite adicionar novos itens ao estoque, informando dados como código, nome, quantidade e preço.
- 🔍 **Consulta de Itens**: Visualize os itens cadastrados, com detalhes completos e possibilidade de filtrar informações.
- ✏️ **Edição de Itens**: Atualize as informações dos itens do estoque sempre que necessário, como quantidade e preço.
- 🔒 **Armazenamento Seguro de Senhas**: As senhas dos usuários são armazenadas de forma segura usando hashing.
  

