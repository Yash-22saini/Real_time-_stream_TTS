import re

def smart_chunk(text, max_chars=80):
    """
    Smaller chunks = faster streaming
    First chunk should be very short for instant playback
    """

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    buffer = ""

    for sent in sentences:
        if len(buffer) + len(sent) <= max_chars:
            buffer += " " + sent
        else:
            chunks.append(buffer.strip())
            buffer = sent

    if buffer:
        chunks.append(buffer.strip())

    return chunks

def smart_chunk(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []

    # First chunk only 1 sentence (instant playback)
    chunks.append(sentences[0])

    buffer = ""

    for sent in sentences[1:]:
        if len(buffer) + len(sent) < 120:
            buffer += " " + sent
        else:
            chunks.append(buffer.strip())
            buffer = sent

    if buffer:
        chunks.append(buffer.strip())

    return chunks
