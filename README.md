<<<<<<< HEAD
# Sistema de Controle de Estoque

Este é um projeto de **Sistema de Controle de Estoque** desenvolvido com **Flask** e **SQLite**. O sistema permite o gerenciamento de itens no estoque, incluindo cadastro, pesquisa, edição, remoção, e a capacidade de importar/exportar itens usando arquivos CSV. A aplicação também oferece funcionalidades como cálculo do valor total do estoque e a exibição de informações formatadas de forma clara.

## Tecnologias Utilizadas

- **Flask**: Framework web para desenvolvimento da aplicação.
- **SQLAlchemy**: ORM utilizado para interação com o banco de dados SQLite.
- **SQLite**: Banco de dados utilizado para armazenar os dados do estoque.
- **Pandas**: Biblioteca usada para importar e exportar arquivos CSV.
- **HTML/CSS**: Para a construção da interface web.
- **Bootstrap (opcional)**: Pode ser usado para melhorar o design da interface, se necessário.

## Funcionalidades

- **Cadastro de Itens**: Permite adicionar novos itens ao estoque.
- **Alteração e Remoção de Itens**: Permite editar ou remover itens existentes.
- **Pesquisa de Itens**: Realiza a busca por nome ou código de item.
- **Visualização do Estoque**: Exibe todos os itens do estoque, juntamente com a quantidade total e o valor total calculado.
- **Importação de Itens**: Permite importar itens a partir de um arquivo CSV.
- **Exportação de Itens**: Exporte todos os itens em um arquivo CSV.

=======
# 📦 Sistema de Controle de Estoque

Este é um sistema simples para gerenciar o estoque de itens, criado com Python, utilizando o **Flask** e o **SQLAlchemy** para interagir com o banco de dados SQLite. Ele permite adicionar, alterar, remover e visualizar itens do estoque, além de importar e exportar dados em formato CSV.

## 🔧 Tecnologias Utilizadas

- **Flask**: Framework web para Python, utilizado para criar a aplicação e gerenciar as rotas.
- **Flask-SQLAlchemy**: Extensão do Flask para integrar o banco de dados SQLite de forma simples.
- **SQLAlchemy**: ORM para manipular dados de forma intuitiva.
- **Pandas**: Usado para importar e exportar dados em arquivos CSV.
- **Locale**: Para formatar valores monetários no padrão brasileiro (R$).
- **Datetime**: Para manipulação e formatação de datas.
- **OS**: Para acessar variáveis de ambiente, garantindo segurança.

---

## 💡 Funcionalidades

- **👀 Visualizar Itens**: A página inicial mostra todos os itens do estoque com detalhes como código, nome, quantidade, preço e data de entrada.
- **➕ Adicionar Itens**: Permite adicionar novos itens ao estoque com código, nome, quantidade, preço e data de entrada.
- **✏️ Alterar ou 🗑️ Remover Itens**: Altere ou remova itens com base no código.
- **🔍 Pesquisar Itens**: Pesquise itens pelo nome ou código e veja resultados rapidamente.
- **📥 Importar e 📤 Exportar Dados**: Importe itens de um arquivo CSV ou exporte todos os itens do estoque para CSV.
- **🔙 Voltar ao Estoque Total**: A opção "Voltar ao Estoque Total" aparece após uma pesquisa, para retornar à lista completa de itens.

---

## 🧑‍💻 Lógica do Código

- **Banco de Dados**: Utilizamos SQLite para armazenar os itens do estoque, com os campos: `id`, `codigo`, `nome`, `quantidade`, `preco` e `data_entrada`.
  
- **Funções Principais**:
  - **calcular_total_itens**: Soma as quantidades dos itens no estoque.
  - **calcular_valor_total**: Calcula o valor total do estoque.


---
>>>>>>> 372a474c1499e06a05271a791c709843cb449b28
