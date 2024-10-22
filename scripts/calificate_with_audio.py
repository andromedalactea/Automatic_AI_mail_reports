import requests
from pydub import AudioSegment
import io
import numpy as np
import soundfile as sf
import base64

# Función para convertir de float32 a PCM16
def float32_to_pcm16(audio_float_array):
    pcm16 = np.int16(audio_float_array * 32767)
    return pcm16

# Función para codificar el audio en base64
def encode_base64_audio(pcm_audio_data):
    byte_data = pcm_audio_data.tobytes()
    base64_audio = base64.b64encode(byte_data).decode('utf-8')
    return base64_audio

# Descarga, convierte el MP3, y ajusta el WAV a PCM16-LE con 16kHz
def download_and_process_mp3_as_pcm16_wav(url):
    try:
        # Paso 1: Descargar el MP3 desde la URL
        print(f"Descargando archivo desde: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error al descargar el archivo. HTTP Status Code: {response.status_code}")
        
        # Paso 2: Convertir el archivo MP3 a WAV en memoria usando pydub
        print("Convirtiendo MP3 a WAV en memoria...")
        mp3_audio = AudioSegment.from_mp3(io.BytesIO(response.content))

        # Paso 3: Forzar la tasa de muestreo a 16kHz, y convertir a MONO (1 canal)
        wav_audio = mp3_audio.set_frame_rate(16000).set_channels(1)  # 16000Hz y Mono

        # Paso 4: Exportar el WAV a Bytes en formato PCM16LE (s16le)
        wav_io = io.BytesIO()
        wav_audio.export(wav_io, format="wav", codec="pcm_s16le")  # PCM Signed 16-bit Little Endian

        # Reiniciamos el puntero para empezar la lectura desde el principio
        wav_io.seek(0)

        # Paso 5: Leer el WAV desde memoria con SoundFile (float32 para posterior procesamiento)
        print("Leyendo el WAV resultante en formato float32...")
        audio_data, samplerate = sf.read(wav_io, dtype='float32')

        # Paso 6: Revisar si es estéreo, y convertir a mono (seleccionando el primer canal)
        channel_data = audio_data[:, 0] if len(audio_data.shape) > 1 else audio_data

        pcm_audio_data = float32_to_pcm16(channel_data)

        base64_audio_data = encode_base64_audio(pcm_audio_data)

        # Retornar los datos procesados (canal usado y frecuencia de muestreo)
        return base64_audio_data
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return None, None

import os
import soundfile as sf
import numpy as np
import asyncio
import websockets
import json
import base64

# Función de conversión de float32 a PCM16
def float32_to_pcm16(audio_float_array):
    pcm16 = np.int16(audio_float_array * 32767)
    return pcm16

# Función para codificar el audio en base64
def encode_base64_audio(pcm_audio_data):
    byte_data = pcm_audio_data.tobytes()
    base64_audio = base64.b64encode(byte_data).decode('utf-8')
    return base64_audio

# Función para leer y procesar los archivos de audio
def process_audio_file(file_path):
    audio_data, samplerate = sf.read(file_path, dtype='float32')
    channel_data = audio_data[:, 0] if len(audio_data.shape) > 1 else audio_data  # Channel 0 si es estéreo
    pcm_audio_data = float32_to_pcm16(channel_data)
    base64_audio_data = encode_base64_audio(pcm_audio_data)
    return base64_audio_data

# Función asincrónica para manejar la conexión websocket
async def main():
    try:
        # Lee y procesa el archivo de audio
        audio_file_path = '/home/clickgreen/freelancers/Automatic_AI_mail_reports/develop-purposes/file.wav'
        base64_audio_data = process_audio_file(audio_file_path)
        base_64 = download_and_process_mp3_as_pcm16_wav('http://38.107.174.254/9820/2024-09-12/20240912-093749_5305273801-all.mp3')
        print('-'*50)
        print(base_64 == base64_audio_data)
        # WebSocket URL para OpenAI
        websocket_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"

        # Encabezados (incluye tu clave de API de OpenAI)
        headers = {
            'Authorization': 'Bearer ' + os.getenv('OPENAI_API_KEY'),  # Usa tu propia variable de entorno o reemplaza con tu clave
            'OpenAI-Beta': 'realtime=v1',
        }
        
        async with websockets.connect(websocket_url, extra_headers=headers) as websocket:
            print("Conectado al servidor.")

            # Evento de creación de mensaje con audio
            event_audio = {
                'type': 'conversation.item.create',
                'item': {
                    'type': 'message',
                    'role': 'user',
                    'content': [
                        {
                            'type': 'input_audio',
                            'audio': base_64
                        }
                    ]
                }
            }

            # Evento de creación de mensaje con texto
            event_text = {
                'type': 'conversation.item.create',
                'item': {
                    'type': 'message',
                    'role': 'user',
                    'content': [
                        {
                            'type': 'input_text',
                            'text': 'Please tell me all the information in the audio and do a response in text format. Also, provide an emotion analysis of the tone. Can you detect tone or do you only process the transcription text?'
                        }
                    ]
                }
            }

            # Enviar eventos (audio y texto)
            await websocket.send(json.dumps(event_audio))
            await websocket.send(json.dumps(event_text))

            # Evento adicional
            response_instructions = {
                'type': 'response.create',
                'response': {'modalities': ['text'], 'instructions': 'help to the user'}
            }
            await websocket.send(json.dumps(response_instructions))
            # await websocket.send(json.dumps(response_instructions))

            # Escuchar respuesta del servidor
            async for message in websocket:
                try:
                    response = json.loads(message)
                    print("Mensaje recibido del servidor:", json.dumps(response, indent=2))
                    if response.get('type') == 'response.done':
                        print("Procesamiento completado. Cerrando el WebSocket...")
                        websocket.close()
                        break  # Salimos del bucle y cerramos
                except json.JSONDecodeError:
                    print("Error al parsear el mensaje:", message)

    except Exception as e:
        print(f"Error en la ejecución del script: {e}")

# Corre la función asincrónica
if __name__ == '__main__':
    asyncio.run(main())