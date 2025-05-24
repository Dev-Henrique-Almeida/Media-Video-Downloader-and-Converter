## 📌 Media Video Downloader and Converter

Este é um script Python para baixar vídeos do YouTube com a opção de escolher entre MP4 (vídeo) ou MP3 (áudio). O usuário insere o link do vídeo, escolhe o formato desejado, e o download é realizado automaticamente.

## 📂 Requisitos

Antes de rodar o script, é necessário ter as seguintes ferramentas instaladas:

1️⃣ Instalar a última versão do Python
Baixe e instale a versão mais recente do Python pelo site oficial:

🔗 Download do Python[https://www.python.org/downloads/]

✅ Durante a instalação, marque a opção:
☑ "Add Python to PATH" (Isso permite rodar python no terminal).

Para verificar se a instalação foi bem-sucedida, execute no terminal (CMD ou PowerShell):

```bash
python --version
```

2️⃣ Instalar Chocolatey (Windows)
Se estiver usando Windows, recomendamos instalar o Chocolatey, um gerenciador de pacotes que facilita a instalação de programas.

1. Abra o PowerShell como Administrador (pesquise "PowerShell" no menu iniciar, clique com o botão direito e escolha "Executar como Administrador").

2. Execute o seguinte comando para instalar o Chocolatey:

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

3. Feche e reabra o PowerShell.
4. Para testar se o Chocolatey foi instalado corretamente, rode

```bash
choco --version
```

Se aparecer algo como 1.x.x, o Chocolatey está instalado! ✅

3️⃣ Instalar FFmpeg
O FFmpeg é necessário para juntar áudio e vídeo corretamente.

📌 Método mais fácil: Instalar via Chocolatey:

```bash
choco install ffmpeg
```
