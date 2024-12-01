from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import os
import logging
from datetime import datetime
import time
import threading

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações
DOWNLOAD_FOLDER = 'downloads'
MAX_FILE_AGE = 3600  # 1 hora em segundos

# Criar pasta para downloads se não existir
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def cleanup_old_files():
    """Remove arquivos antigos do diretório de downloads."""
    while True:
        try:
            current_time = time.time()
            for filename in os.listdir(DOWNLOAD_FOLDER):
                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > MAX_FILE_AGE:
                        os.remove(file_path)
                        logger.info(f"Arquivo removido: {filename}")
        except Exception as e:
            logger.error(f"Erro na limpeza de arquivos: {str(e)}")
        time.sleep(300)  # Verifica a cada 5 minutos

# Iniciar thread de limpeza
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    logger.info("Página inicial acessada")
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        url = request.json.get('url')
        if not url:
            logger.warning("Tentativa de conversão sem URL")
            return jsonify({'error': 'URL não fornecida'}), 400

        logger.info(f"Iniciando conversão para URL: {url}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info['title']
            filename = f"{title}.mp3"
            safe_filename = "".join(x for x in filename if x.isalnum() or x in (' ', '-', '_', '.')).rstrip()
            
            logger.info(f"Conversão concluída com sucesso: {safe_filename}")
            return jsonify({
                'success': True,
                'filename': safe_filename,
                'title': title
            })

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Erro na conversão: {error_msg}")
        return jsonify({
            'error': error_msg,
            'message': 'Ocorreu um erro durante a conversão. Por favor, tente novamente.'
        }), 400

@app.route('/download/<filename>')
def download(filename):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            logger.warning(f"Tentativa de download de arquivo inexistente: {filename}")
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        logger.info(f"Iniciando download do arquivo: {filename}")
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Erro no download do arquivo {filename}: {str(e)}")
        return jsonify({'error': 'Erro ao baixar arquivo'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 