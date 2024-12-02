import os
import time
import logging
import threading
from config.settings import DOWNLOAD_FOLDER, MAX_FILE_AGE

logger = logging.getLogger(__name__)

class CleanupService:
    @staticmethod
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

    @staticmethod
    def start_cleanup_thread():
        """Inicia a thread de limpeza em background."""
        cleanup_thread = threading.Thread(
            target=CleanupService.cleanup_old_files, 
            daemon=True
        )
        cleanup_thread.start()
        logger.info("Thread de limpeza iniciada") 