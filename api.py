# api.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from tts_engine import generate_audio_bytes
import time
from tts_logger import log_performance, log_summary

app = FastAPI()


@app.websocket("/live-tts")
async def live_tts(websocket: WebSocket):
    await websocket.accept()
    print("\n🎙 Client Connected (Live Streaming Started)\n")

    last_sentence = None

    try:
        while True:
            # ✅ Receive sentence from client
            sentence = await websocket.receive_text()
            sentence = sentence.strip()

            # Ignore empty text
            if len(sentence) < 2:
                continue

            # Ignore duplicate sentence
            if sentence == last_sentence:
                continue

            last_sentence = sentence

            print(f"\n➡ Speaking: {sentence}")

            # --------------------------
            # Performance Tracking
            # --------------------------
            start_time = time.perf_counter()

            # Generate TTS audio
            audio_bytes = await generate_audio_bytes(sentence)

            end_time = time.perf_counter()

            total_time_ms = (end_time - start_time) * 1000
            tts_time_ms = total_time_ms
            first_chunk_ms = None  # optional

            # --------------------------
            # Log Performance Per Chunk
            # --------------------------
            log_performance(
                sentence=sentence,
                tts_time_ms=tts_time_ms,
                total_time_ms=total_time_ms,
                first_chunk_ms=first_chunk_ms
            )

            # --------------------------
            # Send audio back to client
            # --------------------------
            await websocket.send_bytes(audio_bytes)

    except WebSocketDisconnect:
        print("\n✅ Client Disconnected Normally")

    except Exception as e:
        print("\n❌ Unexpected Error:", e)

    finally:
        # --------------------------
        # ✅ Final Optimization Summary
        # --------------------------
        print("\n📌 Printing Final Optimization Summary...\n")
        log_summary()

        print("\n🚀 Server Session Finished\n")
