
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


def chunk_pages(
    pages: list[dict],
    strategy: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[dict]:
    """
    Split extracted document pages into chunks
    while preserving their page numbers.
    """

    chunked_pages = []

    for page in pages:
        page_number = page["page"]
        text = page["text"]

        if strategy == "fixed_size":
            chunks = fixed_size_chunking(
                text,
                chunk_size=chunk_size,
                overlap=overlap
            )

        elif strategy == "sentence_based":
            chunks = sentence_based_chunking(
                text,
                max_chunk_size=chunk_size
            )

        else:
            raise ValueError("Unsupported chunking strategy")

        for chunk in chunks:
            chunked_pages.append({
                "text": chunk,
                "page": page_number
            })

    return chunked_pages
