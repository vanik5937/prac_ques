from fastapi import FastAPI, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db

from models import (
    Farm,
    CropBatches
)

from schemas import(
    ParentCreate,
    ParentOut,
    ChildOut,
    ChildCreate,
    ChildUpdate,
    ParentWithChildren
)

Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.post("/farms", response_model=ParentOut, status_code=201)
def add_farm(data: ParentCreate, db: Session = Depends(get_db)):
    item = Farm(**data.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.post("/farms/{parent_id}/crop_batches", response_model= ChildOut, status_code=201)
def add_child(parent_id: int, data: ChildCreate, db: Session = Depends(get_db)):

    parent = db.get(Farm, parent_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Farm does not exist")

    item = CropBatches(**data.model_dump(), farm_id = parent_id)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

#@app.get("/farms/{parent_id}/crop_batches/{child_id}", response_model=ParentWithChildren, status_code=200)

@app.get("/farms/{parent_id}", response_model=ParentWithChildren, status_code=200)
def get_datas(parent_id: int, db: Session = Depends(get_db), crop_type: str | None = Query(default = None), sort: str | None = Query(default=None)):
    parent = db.get(Farm, parent_id)
    if parent is None:
        raise HTTPException(status_code=404, message="Farm Not Found")

    crops = list(parent.crop_batches)
    if crop_type is not None and crop_type.strip():
        crops = [i for i in crops if i.crop_type == crop_type]

    if sort is not None:
        if sort not in ("batch_name", "expected_yield_kg"):
            raise HTTPException(status_code=404, message = "Invalid Sort Type")
        crops.sort(key = lambda c: getattr(c,sort))

    return {
        "id":parent.id,
        "name": parent.name,
        "region": parent.region,
        "children": crops

    }





    
    

    
    