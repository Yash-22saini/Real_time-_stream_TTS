import asyncio
import websockets

async def test_stream():
    uri = "ws://localhost:8000/stream-tts"

    async with websockets.connect(uri) as ws:

        long_text = """
        Hello Yash! This is a real-time streaming TTS demo.
        The audio will start immediately without waiting.
        Chunking ensures voice breaks are natural.
        """

        await ws.send(long_text)

        while True:
            msg = await ws.recv()

            if isinstance(msg, bytes):
                print("🎧 Received audio chunk:", len(msg))

            else:
                print("📊 Latency Report:", msg)
                break

asyncio.run(test_stream())