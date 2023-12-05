from sqlalchemy.orm import Session

import models, schemas


def get_music(db: Session, music_id: int):
    return db.query(models.Music) \
        .filter(models.Music.id == music_id) \
        .first()


def get_music_by_id(db: Session, id: int):
    return db.query(models.Music) \
        .filter(models.Music.id == id) \
        .first()


def get_musics(db: Session):
    return db.query(models.Music) \
        .all()


def create_music(db: Session, music: schemas.MusicCreate):
    db_music = models.Music(title=music.title,
                            blues=music.blues,
                            classical=music.classical,
                            country=music.country,
                            disco=music.disco,
                            hiphop=music.hiphop,
                            jazz=music.jazz,
                            metal=music.metal,
                            pop=music.pop,
                            reggae=music.reggae,
                            rock=music.rock)
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return [db_music.id, db_music.title
