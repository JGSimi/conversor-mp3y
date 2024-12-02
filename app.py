from flask import Flask, request, render_template
from flask_cors import CORS
import logging
from src.controllers.converter_controller import ConverterController
from src.services.cleanup_service import CleanupService

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação
app = Flask(__name__)
CORS(app)

# Iniciar serviço de limpeza
CleanupService.start_cleanup_thread()

@app.route('/')
def index():
    logger.info("Página inicial acessada")
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    return ConverterController.convert(request.json.get('url'))

@app.route('/download/<filename>')
def download(filename):
    return ConverterController.download(filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 