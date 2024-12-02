import yt_dlp
import logging
from config.settings import YDL_OPTS

logger = logging.getLogger(__name__)

class ConverterService:
    @staticmethod
    def convert_url_to_mp3(url: str) -> dict:
        """
        Converte uma URL do YouTube para MP3.
        
        Args:
            url (str): URL do vídeo do YouTube
            
        Returns:
            dict: Dicionário com informações do arquivo convertido
        """
        try:
            with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info['title']
                filename = f"{title}.mp3"
                safe_filename = "".join(x for x in filename if x.isalnum() or x in (' ', '-', '_', '.')).rstrip()
                
                logger.info(f"Conversão concluída com sucesso: {safe_filename}")
                return {
                    'success': True,
                    'filename': safe_filename,
                    'title': title
                }
                
        except Exception as e:
            logger.error(f"Erro na conversão: {str(e)}")
            raise 