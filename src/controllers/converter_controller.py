import os
import logging
from flask import jsonify, send_file
from src.services.converter_service import ConverterService
from config.settings import DOWNLOAD_FOLDER

logger = logging.getLogger(__name__)

class ConverterController:
    @staticmethod
    def convert(url: str):
        """
        Controla o processo de conversão de URL para MP3.
        """
        try:
            if not url:
                logger.warning("Tentativa de conversão sem URL")
                return jsonify({'error': 'URL não fornecida'}), 400

            logger.info(f"Iniciando conversão para URL: {url}")
            result = ConverterService.convert_url_to_mp3(url)
            return jsonify(result)

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Erro na conversão: {error_msg}")
            return jsonify({
                'error': error_msg,
                'message': 'Ocorreu um erro durante a conversão. Por favor, tente novamente.'
            }), 400

    @staticmethod
    def download(filename: str):
        """
        Controla o download do arquivo convertido.
        """
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