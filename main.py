from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI()

class Movie(BaseModel):
    id: int = Field()
    title: str
    director: str
    release_year: int = Field(min_length=1896, max_length=2024)
    rating: float = Field(min_length=1, max_length=5)

movies_database = [
    Movie(id=1, title="Alien", director="Ridley Scott", release_year=1979, rating=4.6),
    Movie(id=2, title="Spider-Man", director="Sam Raimi", release_year=2002, rating=4.7),
    Movie(id=3, title="The Terminator", director="James Cameron", release_year=1984, rating=4.7)
]

@app.get("/")
async def docs():
    return RedirectResponse("/docs")

@app.get("/movies", response_model=list[Movie])
async def get_all_movies():
    return movies_database

@app.post("/movies", response_model=Movie)
async def add_movie(movie: Movie):
    if movie.id not in movies_database:
        movies_database.append(movie)
        return movie
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/movies/{id}", response_model=Movie)
async def get_movie_by_id(id: int):
    for movie in movies_database:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{id}", response_model=Movie)
async def delete_movie(id: int):
    for movie in movies_database:
        if movie.id == id:
            movies_database.remove(movie)
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)