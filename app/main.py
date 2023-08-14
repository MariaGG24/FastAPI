from fastapi import FastAPI, HTTPException

import os
from pydantic import BaseModel #VALIDACIÓN DE DATOS
from typing import Optional

from .nytimes_client import get_top_stories
from .story_formatter import format_stories_to_string
from .summariser import summarise_news_stories

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str] #Para que sea un atributo opcional

#http://127.0.0.1:8000
# http://127.0.0.1:8000/docs --> Documentación de la API
@app.get("/")
def index():
    return {"message" : "Hola Mundo"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {"data" : id}

@app.post("/libros")
def insertar_libro(libro: Libro):
    return {"message": f"libro {libro.titulo} insertado"}


#@app.get("/news")
#def news():
#    return get_top_stories()

@app.get("/news")
def news():
    summary = ""
    images = []
    try:
        stories = get_top_stories()
        for story in stories:
            images.extend(story["multimedia"])
        summary = summarise_news_stories(format_stories_to_string(stories))
        images = list(
            filter(lambda image: image["format"] == "Large Thumbnail", images)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Apologies, something bad happened :("
        )
    return {"summary": summary, "images": images}