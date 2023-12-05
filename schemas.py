from pydantic import BaseModel


class MusicBase(BaseModel):
    title: str
    blues: float
    classical: float
    country: float
    disco: float
    hiphop: float
    jazz: float
    metal: float
    pop: float
    reggae: float
    rock: float


class MusicCreate(MusicBase):

    def __init__(self, title, vector):
        super().__init__(
            title=title,
            blues=vector[0],
            classical=vector[1],
            country=vector[2],
            disco=vector[3],
            hiphop=vector[4],
            jazz=vector[5],
            metal=vector[6],
            pop=vector[7],
            reggae=vector[8],
            rock=vector[9]
        )


class Music(MusicBase):
    id: int
