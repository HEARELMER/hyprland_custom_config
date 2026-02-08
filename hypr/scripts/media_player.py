#!/usr/bin/env python3
import json
import subprocess
import sys
import html  # <--- IMPORTANTE: Esta librería arregla el error del "&"

def get_media_info():
    try:
        # Preguntamos a playerctl el estado, artista y titulo
        cmd = "playerctl --player=brave,chromium,spotify metadata --format '{\"status\": \"{{status}}\", \"artist\": \"{{artist}}\", \"title\": \"{{title}}\"}'"

        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

        if not result.strip():
            return None

        return json.loads(result)

    except subprocess.CalledProcessError:
        return None
    except json.JSONDecodeError:
        return None

def main():
    data = get_media_info()

    if not data:
        print(json.dumps({"text": "", "tooltip": ""}))
        return

    # --- AQUÍ ESTÁ EL ARREGLO ---
    # Usamos html.escape() para convertir "&" en "&amp;" automáticamente
    status = data.get("status", "")
    artist = html.escape(data.get("artist", "Desconocido"))
    title = html.escape(data.get("title", "Desconocido"))

    # Icono de Spotify siempre (como pediste)
    icon = " " 

    full_text = f"{artist} - {title}"
    short_text = (full_text[:35] + '...') if len(full_text) > 35 else full_text

    output = {
        "text": f"{icon} {short_text}",
        "tooltip": f"Reproduciendo: {full_text}",
        "class": "custom-media",
        "alt": status
    }

    print(json.dumps(output))

if __name__ == "__main__":
    main()