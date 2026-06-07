from pathlib import Path
import math
import re
from collections import Counter


def load_project_notes(path: str | Path) -> list[dict[str, str]]:
    text = Path(path).read_text(encoding="utf-8")
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    documents = []

    for index, block in enumerate(blocks, start=1):
        first_line, _, body = block.partition("\n")
        documents.append(
            {
                "source": first_line.replace(":", ""),
                "content": body.strip() or first_line.strip(),
                "chunk_id": f"note-{index}",
            }
        )

    return documents


def retrieve(query: str, documents: list[dict[str, str]], top_k: int = 3) -> list[dict]:
    query_vector = _text_vector(query)
    scored = [
        (_cosine_similarity(query_vector, _text_vector(doc["content"])), doc)
        for doc in documents
    ]
    scored.sort(key=lambda item: item[0], reverse=True)

    results = []
    for score, doc in scored[:top_k]:
        results.append(
            {
                "source": doc["source"],
                "content": doc["content"],
                "score": round(float(score), 3),
            }
        )

    return results


def _text_vector(text: str) -> Counter:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]+", text.lower())
    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "was",
        "were",
        "are",
        "because",
        "project",
    }
    return Counter(word for word in words if word not in stop_words)


def _cosine_similarity(left: Counter, right: Counter) -> float:
    common_words = set(left) & set(right)
    numerator = sum(left[word] * right[word] for word in common_words)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if not left_norm or not right_norm:
        return 0.0

    return numerator / (left_norm * right_norm)


def make_answer(query: str, retrieved_docs: list[dict]) -> str:
    if not retrieved_docs:
        return "No relevant project notes were found."

    evidence = "\n\n".join(
        f"- {doc['source']}: {doc['content']}" for doc in retrieved_docs
    )
    return (
        "Based on the retrieved project notes, here is the most relevant evidence:\n\n"
        f"{evidence}\n\n"
        "Use this evidence to prepare a final LLM-generated answer with citations."
    )
