from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TheoryBlockListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    order_index: int
    title: str
    summary: str


class TheoryBlockOut(TheoryBlockListOut):
    content_markdown: str
