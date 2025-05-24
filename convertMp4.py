#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import subprocess
import glob
from pathlib import Path
import shutil


def check_ffmpeg():
    """Verifica se o FFmpeg e ffprobe estão instalados no sistema."""
    ffmpeg_installed = shutil.which("ffmpeg") is not None
    ffprobe_installed = shutil.which("ffprobe") is not None
    
    if not ffmpeg_installed or not ffprobe_installed:
        print("Erro: Ferramentas necessárias não encontradas.")
        if not ffmpeg_installed:
            print("FFmpeg não está instalado.")
        if not ffprobe_installed:
            print("FFprobe não está instalado.")
            
        print("\nPor favor, instale o pacote completo do FFmpeg:")
        print("Em sistemas baseados em Debian/Ubuntu: sudo apt install ffmpeg")
        print("Em sistemas baseados em Fedora: sudo dnf install ffmpeg")
        print("Em macOS com Homebrew: brew install ffmpeg")
        print("Em Windows, baixe de: https://ffmpeg.org/download.html")
        return False
    return True


def get_file_size(file_path):
    """Retorna o tamanho do arquivo em formato legível."""
    size_bytes = os.path.getsize(file_path)
    
    # Converter para KB, MB, GB conforme apropriado
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def convert_file(input_file, output_file=None, quality=23, preset="medium", audio_codec="copy"):
    """Converte um arquivo MKV para MP4 usando FFmpeg."""
    if not os.path.exists(input_file):
        print(f"Erro: O arquivo '{input_file}' não existe.")
        return False

    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".mp4"

    print(f"Iniciando conversão:")
    print(f"Arquivo de entrada: {input_file}")
    print(f"Arquivo de saída: {output_file}")
    print(f"Qualidade (CRF): {quality}")
    print(f"Preset: {preset}")
    print(f"Codec de áudio: {audio_codec}")
    
    duration_cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        input_file
    ]
    
    try:
        duration = float(subprocess.check_output(duration_cmd).decode('utf-8').strip())
        has_duration = True
    except (subprocess.SubprocessError, ValueError):
        print("Não foi possível determinar a duração do vídeo. O progresso não será exibido.")
        has_duration = False
    
    cmd = [
        "ffmpeg",
        "-i", input_file
    ]
    
    if has_duration:
        cmd.extend(["-progress", "-", "-nostats"])
    
    cmd.extend([
        "-c:v", "libx264",
        "-crf", str(quality),
        "-preset", preset,
        "-c:a", audio_codec
    ])
    
    cmd.extend(["-c:s", "copy"])  
    cmd.extend(["-map", "0"])    
    
    cmd.append(output_file)
    
    print("\nExecutando comando:")
    print(" ".join(cmd))
    print("\nConvertendo...")
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        
        if has_duration:
            # Monitorar o progresso
            current_time = 0
            for line in process.stdout:
                if "out_time_ms=" in line:
                    time_str = line.strip().split('=')[1]
                    try:
                        current_time = float(time_str) / 1000000
                        progress = min(100, (current_time / duration) * 100)
                        print(f"\rProgresso: {progress:.1f}% ({current_time:.1f}s / {duration:.1f}s)", end="")
                    except ValueError:
                        pass
        
        process.wait()
        if process.returncode != 0:
            print(f"\nERRO: A conversão falhou com código de retorno {process.returncode}")
            return False
        
        print("\n") 
        
        input_size = get_file_size(input_file)
        output_size = get_file_size(output_file)
        
        print(f"Conversão concluída com sucesso!")
        print(f"Arquivo gerado: {output_file}")
        print(f"Tamanho do arquivo original: {input_size}")
        print(f"Tamanho do arquivo convertido: {output_size}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\nERRO: A conversão falhou!")
        print(f"Mensagem de erro: {e}")
        return False


def batch_convert(quality=23, preset="medium", audio_codec="copy"):
    """Converte todos os arquivos MKV no diretório atual."""
    mkv_files = glob.glob("*.mkv")
    
    if not mkv_files:
        print("Nenhum arquivo MKV encontrado no diretório atual.")
        return
    
    print(f"Modo de lote: encontrados {len(mkv_files)} arquivos MKV para converter")
    
    successful = 0
    failed = 0
    
    for input_file in mkv_files:
        output_file = os.path.splitext(input_file)[0] + ".mp4"
        print(f"\n{'-' * 60}")
        print(f"Convertendo: {input_file} -> {output_file}")
        
        if convert_file(input_file, output_file, quality, preset, audio_codec):
            successful += 1
        else:
            failed += 1
    
    print(f"\n{'-' * 60}")
    print(f"Processo de lote concluído.")
    print(f"Arquivos convertidos com sucesso: {successful}")
    print(f"Falhas na conversão: {failed}")


def main():
    parser = argparse.ArgumentParser(
        description="Converte arquivos MKV para MP4 sem limitações de tamanho usando FFmpeg"
    )
    parser.add_argument(
        "input_file", 
        nargs="?", 
        help="Arquivo MKV de entrada (não necessário com --batch)"
    )
    parser.add_argument(
        "output_file", 
        nargs="?", 
        help="Arquivo MP4 de saída (opcional)"
    )
    parser.add_argument(
        "-q", "--quality", 
        type=int, 
        default=23, 
        help="Qualidade do vídeo (0=melhor, 51=pior, padrão=23)"
    )
    parser.add_argument(
        "-p", "--preset", 
        default="medium", 
        choices=["ultrafast", "superfast", "veryfast", "faster", "fast", 
                 "medium", "slow", "slower", "veryslow"],
        help="Preset de codificação (padrão=medium)"
    )
    parser.add_argument(
        "-a", "--audio-codec", 
        default="copy", 
        help="Codec de áudio (copy, aac, padrão=copy)"
    )
    parser.add_argument(
        "-b", "--batch", 
        action="store_true", 
        help="Converter todos os arquivos MKV no diretório atual"
    )
    
    args = parser.parse_args()
    
    if not check_ffmpeg():
        sys.exit(1)
    
    if args.batch:
        batch_convert(args.quality, args.preset, args.audio_codec)
    elif args.input_file:
        convert_file(args.input_file, args.output_file, args.quality, args.preset, args.audio_codec)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()