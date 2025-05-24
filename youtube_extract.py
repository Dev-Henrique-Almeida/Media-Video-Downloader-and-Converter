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

def format_duration(seconds):
    """Converte a duração de segundos para o formato 'X minutos e Y segundos'."""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} minutos e {seconds} segundos"

def format_number(number):
    """Formata números grandes para separação por pontos (ex: 1.000.000)."""
    return f"{number:,}".replace(",", ".")

video_url = input("🔗 Insira o link do vídeo ou da playlist do YouTube Music: ").strip()

print("\n🎵 Escolha o formato de download:")
print("1️⃣ - MP4 (Vídeo)")
print("2️⃣ - MP3 (Áudio)")
formato = input("Digite 1 para MP4 ou 2 para MP3: ").strip()


info_opts = {
    "quiet": True,
    "extract_flat": True,  
}

with yt_dlp.YoutubeDL(info_opts) as ydl:
    info = ydl.extract_info(video_url, download=False)

is_playlist = "_type" in info and info["_type"] == "playlist"

video_title = sanitize_filename(info.get("title", "playlist_desconhecida" if is_playlist else "video_desconhecido"))
download_folder = os.path.join("downloads", video_title)
info_folder = os.path.join("informations", video_title)

os.makedirs(download_folder, exist_ok=True)
os.makedirs(info_folder, exist_ok=True)

json_path = os.path.join(info_folder, f"{video_title}.json")

video_data = {
    "Título": info.get("title"),
    "Canal": info.get("uploader"),
    "Visualizações": format_number(info.get("view_count", 0)),
    "Curtidas": format_number(info.get("like_count", 0)),
    "Data de Upload": format_date(info.get("upload_date")),
    "Duração": format_duration(info.get("duration", 0)),
    "URL": info.get("webpage_url"),
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(video_data, f, indent=4, ensure_ascii=False)

print("\n📊 Informações:")
for key, value in video_data.items():
    print(f"🔹 {key}: {value}")

print(f"\n📄 Metadados salvos em '{json_path}'.")

if formato == "1":
    ydl_opts = {
        "format": "bv*+ba/best",
        "outtmpl": os.path.join(download_folder, "%(playlist_index)s - %(title)s.%(ext)s" if is_playlist else "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferredformat": "mp4",
            }
        ],
    }
    tipo_download = "🎬 Baixando vídeo(s) em MP4..."
elif formato == "2":
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(download_folder, "%(playlist_index)s - %(title)s.%(ext)s" if is_playlist else "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    tipo_download = "🎵 Baixando áudio(s) em MP3..."
else:
    print("❌ Opção inválida! Saindo...")
    exit()

print(f"\n{tipo_download}")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("\n✅ Download concluído! Os arquivos foram salvos em:")
print(f"📂 {download_folder} (Mídia)")
print(f"📂 {info_folder} (Informações)")
