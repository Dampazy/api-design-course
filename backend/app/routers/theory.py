from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.theory import TheoryBlock
from app.schemas.theory import TheoryBlockListOut, TheoryBlockOut

router = APIRouter(prefix="/api/theory", tags=["theory"])


@router.get("", response_model=List[TheoryBlockListOut])
def list_theory_blocks(db: Session = Depends(get_db)) -> List[TheoryBlock]:
    return db.query(TheoryBlock).order_by(TheoryBlock.order_index).all()


@router.get("/{slug}", response_model=TheoryBlockOut)
def get_theory_block(slug: str, db: Session = Depends(get_db)) -> TheoryBlock:
    block = db.query(TheoryBlock).filter(TheoryBlock.slug == slug).first()
    if block is None:
        raise HTTPException(status_code=404, detail="Theory block not found")
    return block
