import sys, os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

if len(sys.argv) != 3: sys.exit("Uso: python teste.py <arquivo_audio.mp3> <imagem_capa.jpg>")

audio_path, cover_path = sys.argv[1], sys.argv[2]
if not os.path.isfile(audio_path): sys.exit(f"Arquivo de áudio não encontrado: {audio_path}")
if not os.path.isfile(cover_path): sys.exit(f"Arquivo de imagem não encontrado: {cover_path}")

dirname, basename = os.path.split(audio_path)
new_audio_path = os.path.join(dirname, f"capa - {basename}")
if os.path.exists(new_audio_path): sys.exit(f"Arquivo de destino já existe: {new_audio_path}")

try:
    with open(audio_path, 'rb') as src, open(new_audio_path, 'wb') as dst: dst.write(src.read())
    
    audio = MP3(new_audio_path, ID3=ID3)
    try: audio.add_tags()
    except error: pass
    
    with open(cover_path, 'rb') as img: image_data = img.read()
    mime_type = 'image/jpeg' if cover_path.lower().endswith(('.jpg', '.jpeg')) else 'image/png' if cover_path.lower().endswith('.png') else sys.exit("Formato de imagem não suportado. Use JPG ou PNG.")
    
    if audio.tags is not None: audio.tags.delall('APIC')
    audio.tags.add(APIC(encoding=3, mime=mime_type, type=3, desc='Cover', data=image_data))
    audio.save(v2_version=3)
    print(f"Capa adicionada com sucesso em: {new_audio_path}")

except Exception as e:
    print(f"Erro: {e}")
    if os.path.exists(new_audio_path): os.remove(new_audio_path)
    sys.exit(1)