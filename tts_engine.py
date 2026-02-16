import edge_tts
import io


async def generate_audio_bytes(text):

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-GuyNeural"
    )

    audio_stream = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    return audio_stream.getvalue()
