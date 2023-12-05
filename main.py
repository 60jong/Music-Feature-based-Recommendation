from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy.orm import Session
import numpy as np

from db import SessionLocal, engine
import crud, models, schemas

from neural import MFR_modules
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("")
async def hello():
    return "Hello World!"


@app.get("/musics")
async def get_musics(
        db: Session = Depends(get_db)
):
    return crud.get_musics(db)


@app.get("/musics/recommend")
async def get_recommended(
        music_id: int,
        limit: int,
        db: Session = Depends(get_db)
):
    musics = crud.get_musics(db)
    target = crud.get_music_by_id(db, music_id)
    target_vec_arr = np.array(target.get_vectors())

    cos_sims = []
    for m in musics:
        if m.id == id:
            continue
        cos_sims.append(
            (cos_sim(target_vec_arr, np.array(m.get_vectors())), m.id)
        )

    cos_sims = sorted(cos_sims, key=lambda x: x[0], reverse=True)
    return cos_sims[:limit]


def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


@app.post("/musics/register", response_model=schemas.Music)
async def create_upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # save file
    title = file.filename
    new_file_path = os.path.join(os.getcwd(), "static", "musics", title)

    if os.path.exists(new_file_path):
        return {
            "message": "already registered"
        }

    # new file
    with open(new_file_path, "wb") as f:
        f.write(file.file.read())

    # convert 10-D vector
    sample_input = MFR_modules.ext_sample_input(new_file_path)
    arr = MFR_modules.return_result_for_crnn(sample_input, "neural/MFR_model_mk_5")
    genre_vector = arr.tolist()

    return crud.create_music(db, schemas.MusicCreate(title, genre_vector))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
