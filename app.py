from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Criar pasta para downloads se não existir
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL não fornecida'}), 400

        # Configurações do yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True
        }

        # Download e conversão
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info['title']
            filename = f"{title}.mp3"
            safe_filename = "".join(x for x in filename if x.isalnum() or x in (' ', '-', '_', '.')).rstrip()
            
            return jsonify({
                'success': True,
                'filename': safe_filename,
                'title': title
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(
            f'downloads/{filename}',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001) 