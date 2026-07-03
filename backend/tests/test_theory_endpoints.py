from __future__ import annotations


def test_list_theory_returns_six_blocks_in_order(client):
    response = client.get("/api/theory")
    assert response.status_code == 200
    blocks = response.json()
    assert len(blocks) == 6
    assert [b["order_index"] for b in blocks] == [1, 2, 3, 4, 5, 6]


def test_get_theory_block_by_slug(client):
    response = client.get("/api/theory/rest-basics-http-methods")
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Основы REST и HTTP-методы"
    assert "content_markdown" in body


def test_get_theory_block_404_for_unknown_slug(client):
    response = client.get("/api/theory/does-not-exist")
    assert response.status_code == 404
