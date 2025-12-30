import os
import json
import time
import subprocess
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÕES DINÂMICAS (Funciona em qualquer PC)
# ==============================================================================

# Pega o caminho da pasta Roaming do usuário atual automaticamente
# (Ex: C:\Users\SeuAmigo\AppData\Roaming)
ROAMING_FOLDER = os.getenv('APPDATA')

# Define o caminho do Spotify baseado no usuário atual
SPOTIFY_EXE = os.path.join(ROAMING_FOLDER, "Spotify", "Spotify.exe")

# Define uma pasta própria para o seu programa salvar o banco de dados
# Isso impede que o arquivo se perca quando roda via Inicialização do Windows
PROGRAM_DATA_FOLDER = os.path.join(ROAMING_FOLDER, "AutoSpicetify")
DB_FILE = os.path.join(PROGRAM_DATA_FOLDER, "last_update.json")

# Garante que a pasta de dados exista antes de começar
if not os.path.exists(PROGRAM_DATA_FOLDER):
    try:
        os.makedirs(PROGRAM_DATA_FOLDER)
    except Exception as e:
        print(f"⚠️ Erro ao criar pasta de dados: {e}")

# ==============================================================================
# FUNÇÕES
# ==============================================================================

def get_file_info(path):
    """
    Pega a data de modificação e o tamanho do arquivo.
    Se o arquivo mudar (update), esses números mudam.
    """
    if not os.path.exists(path):
        return None
    
    try:
        stats = os.stat(path)
        return f"{stats.st_size}_{stats.st_mtime}"
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None

def apply_spicetify_patch():
    print("\n[Spicetify] ⚠️ Aplicando Spicetify (Update ou Primeira Instalação)...")
    
    commands = [
        "iwr -useb https://raw.githubusercontent.com/spicetify/cli/main/install.ps1 | iex",
        "spicetify backup apply"
    ]
    
    for cmd in commands:
        print(f"[Executando] {cmd}")
        try:
            # capture_output=False permite que o usuário veja o progresso no terminal
            subprocess.run(
                ["powershell", "-Command", cmd],
                input=b"Y\n", 
                capture_output=False 
            )
        except Exception as e:
            print(f"[Erro] Falha ao rodar comando: {e}")

    print("[Spicetify] ✅ Processo finalizado.")

def check_routine():
    current_signature = get_file_info(SPOTIFY_EXE)
    
    # Se não achar o Spotify, avisa e para.
    if not current_signature:
        print(f"❌ ERRO CRÍTICO: Não foi possível encontrar o Spotify em:")
        print(f"   {SPOTIFY_EXE}")
        print("   Verifique se o Spotify está instalado na versão padrão (não Microsoft Store).")
        return

    last_known = {}
    
    # Tenta ler o banco de dados da pasta AppData
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                last_known = json.load(f)
        except:
            pass # Se o arquivo estiver corrompido, trata como vazio

    saved_signature = last_known.get("signature")

    # --- CENÁRIO 1: PRIMEIRA VEZ (Sem registro anterior) ---
    if saved_signature is None:
        print("🆕 Primeira execução detectada (Sem registro anterior).")
        print("🚀 Iniciando instalação/patch do Spicetify para garantir funcionamento...")
        
        apply_spicetify_patch()
        
        # Salva o estado atual
        with open(DB_FILE, 'w') as f:
            json.dump({"signature": current_signature, "last_check": str(datetime.now())}, f)
        return

    # --- CENÁRIO 2: VERIFICAÇÃO DE UPDATE ---
    if saved_signature != current_signature:
        print(f"🔄 ATUALIZAÇÃO DO SPOTIFY DETECTADA!")
        print(f"   Antigo: {saved_signature}")
        print(f"   Novo:   {current_signature}")
        
        apply_spicetify_patch()
        
        # Atualiza o DB com a nova assinatura
        with open(DB_FILE, 'w') as f:
            json.dump({"signature": current_signature, "last_check": str(datetime.now())}, f)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Spotify atualizado e seguro. Nenhuma ação necessária.")

# ==============================================================================
# LOOP PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    print("---------------------------------------------------")
    print(f"🔎 AutoSpicetify - by Lacrymosaa")
    print("---------------------------------------------------")
    
    check_routine()
    
    print("\n👋 Encerrando em 5 segundos...")
    time.sleep(5)