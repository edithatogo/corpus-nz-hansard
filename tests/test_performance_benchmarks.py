from __future__ import annotations

from scripts.build_search_index import chunk_text


def test_chunk_text_benchmark(benchmark):
    text = " ".join(
        ["Parliamentary debate text with repeated procedural, ministerial, and legislative terms."]
        * 200
    )

    chunks = benchmark(chunk_text, text, 1600, 200)

    assert chunks
    assert chunks[0]["start_char"] == 0
