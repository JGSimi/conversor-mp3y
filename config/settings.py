import os

# Configurações básicas
DOWNLOAD_FOLDER = 'downloads'
MAX_FILE_AGE = 3600  # 1 hora em segundos

# Configurações do yt-dlp
YDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    'quiet': True
}

# Criar pasta para downloads se não existir
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER) 