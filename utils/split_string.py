import math


def split_string_with_padding(text, length, elements):
    """
    Breaks a string into a list of strings of a specified length.
    Pads the final string with spaces if it is shorter than the length.
    """
    if length <= 0:
        return [text]

    # Create the initial list of chunks
    chunks = [text[i:i + length] for i in range(0, len(text), length)]

    # Check if the last chunk needs padding
    if chunks and len(chunks[-1]) < length:
        chunks[-1] = chunks[-1].ljust(length)

    if len(chunks) < elements:
        for _ in range(elements - len(chunks)):
            chunks.append(" " * length)
    return chunks


def split_string(s, w):
    results = []

    for i in range(len(s)):
        lengths = [len(s[i][j]) / w[j] for j in range(len(s[i]))]
        max_len = math.ceil(max(lengths))
        chunks = [split_string_with_padding(s[i][j], w[j], max_len) for j in range(len(s[i]))]
        for k in range(max_len):
            p = "|".join([chunks[j][k] for j in range(len(s[i]))])
            results.append(p)
        results.append("\n")

    return results
