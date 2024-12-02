#!/bin/bash

# Obtém o diretório do script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Verifica se o ambiente virtual existe, se não, cria
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativa o ambiente virtual
source .venv/bin/activate

# Instala ou atualiza as dependências
pip install -r requirements.txt

# Abre o navegador (aguarda 2 segundos para o servidor iniciar)
(sleep 2 && open "http://127.0.0.1:5001") &

# Inicia o servidor
python app.py 