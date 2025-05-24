import os
import json
import yt_dlp
import re
from datetime import datetime

def sanitize_filename(filename):
    """Remove caracteres inválidos para nomes de arquivos e pastas."""
    return re.sub(r'[<>:"/\\|?*]', "", filename).strip()

def format_date(yt_date):
    """Converte a data do formato YYYYMMDD para DD-MM-YYYY."""
    try:
        return datetime.strptime(yt_date, "%Y%m%d").strftime("%d-%m-%Y")
    except:
        return "Data desconhecida"
        raise

def format_duration(seconds):
    """Converte a duração de segundos para o formato 'X minutos e Y segundos'."""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} minutos e {seconds} segundos"

def format_number(number):
    """Formata números grandes para separação por pontos (ex: 1.000.000)."""
    return f"{number:}".replace(",", ".")

# Pergunta ao usuário o link do vídeo
video_url = input("🔗 Insira o link do vídeo do YouTube: ").strip()

# Escolha do formato
print("\n🎵 Escolha o formato de download:")
print("1️⃣ - MP4 (Vídeo)")
print("2️⃣ - MP3 (Áudio)")
formato = input("Digite 1 para MP4 ou 2 para MP3: ").strip()

# Configuração do yt-dlp para extrair informações do vídeo
info_opts = {
    "quiet": True,
    "extract_flat": False,
}

# Obtém informações do vídeo
with yt_dlp.YoutubeDL(info_opts) as ydl:
    info = ydl.extract_info(video_url, download=False)

# Formata o nome do vídeo para criar a pasta corretamente
video_title = sanitize_filename(info.get("title", "video_desconhecido"))
video_folder_downloads = os.path.join("downloads", video_title)
video_folder_info = os.path.join("informations", video_title)

# Cria as pastas específicas para o vídeo
os.makedirs(video_folder_downloads, exist_ok=True)
os.makedirs(video_folder_info, exist_ok=True)

# Caminho para o JSON de metadados
json_path = os.path.join(video_folder_info, f"{video_title}.json")

# Formatar informações do vídeo
video_data = {
    "Título": info.get("title"),
    "Canal": info.get("uploader"),
    "Visualizações": format_number(info.get("view_count", 0)),
    "Curtidas": format_number(info.get("like_count", 0)),
    "Data de Upload": format_date(info.get("upload_date")),
    "Duração": format_duration(info.get("duration", 0)),
    "URL": info.get("webpage_url"),
}

# Salva as informações em um arquivo JSON dentro da pasta correta
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(video_data, f, indent=4, ensure_ascii=False)

# Exibe as informações no terminal
print("\n📊 Informações do Vídeo:")
for key, value in video_data.items():
    print(f"🔹 {key}: {value}")

print(f"\n📄 Metadados salvos em '{json_path}'.")

# Configuração para baixar o vídeo ou áudio
if formato == "1":
    ydl_opts = {
        "format": "bv*+ba/best",
        "outtmpl": os.path.join(video_folder_downloads, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
    }
    tipo_download = "🎬 Baixando vídeo em MP4..."
elif formato == "2":
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(video_folder_downloads, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    tipo_download = "🎵 Baixando áudio em MP3..."
else:
    print("❌ Opção inválida! Saindo...")
    exit()

print(f"\n{tipo_download}")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("\n✅ Download concluído! Os arquivos foram salvos em:")
print(f"📂 {video_folder_downloads} (Mídia)")
print(f"📂 {video_folder_info} (Informações)")
