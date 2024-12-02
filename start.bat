@echo off
cd /d "%~dp0"

:: Verifica se o ambiente virtual existe, se não, cria
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

:: Ativa o ambiente virtual
call .venv\Scripts\activate.bat

:: Instala ou atualiza as dependências
pip install -r requirements.txt

:: Abre o navegador (aguarda 2 segundos para o servidor iniciar)
start "" cmd /c "timeout /t 2 /nobreak && start http://127.0.0.1:5001"

:: Inicia o servidor
python app.py 