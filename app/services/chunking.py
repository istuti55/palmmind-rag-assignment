
def fixed_size_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def sentence_based_chunking(
    text: str,
    max_chunk_size: int = 500
) -> list[str]:

    if max_chunk_size <= 0:
        raise ValueError("Maximum chunk size must be greater than zero")

    sentences = text.split(".")

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence += "."

        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence

        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
