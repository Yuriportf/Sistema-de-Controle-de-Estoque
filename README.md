
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



