@echo off
cd /d "C:\Users\yuris\OneDrive\Desktop\Projetos de programação\PROJETOSDEPYTHON\PROJEOSGERAIS\SistemadeControledeEstoque\ProjetoEstoque"
call .\venv\Scripts\activate.bat
python app.py
start http://127.0.0.1:5000
pause
