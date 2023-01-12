from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

#calling fastapi
api = FastAPI()

class bird_data(BaseModel):
    name: str
    sci_name: str
    breeding: str
    threat: str

bird_posts = [
{
    "name": "African red-eyed bulbul",
    "sci_name": "Pycnonotus nigricans",
    "breeding": "two to three eggs per breeding season",
    "threat": "None",
    "id": 1
},
{
    "name": "African Black Oystercatcher",
    "sci_name": "Pycnonotus nigricans",
    "breeding": "one to four eggs per breeding season",
    "threat": "Unknown",
    "id": 2
}
]

def find_bird(id):
    for bird in bird_posts:
        if bird["id"] == id:
            return bird

@api.get("/")
async def root():
    return{"message": "Hi there, Python."}

@api.get("/posts")
async def get_birds():
    return {"data": bird_posts}

@api.post("/posts")
async def get_birds(birdData: bird_data):
    post_dict = birdData.dict()
    post_dict["id"] = randrange(3, 1000000)
    bird_posts.append(post_dict)
    return{"data": post_dict}

@api.get("/posts/{id}")
async def get_bird(id: int):
    post = find_bird(id)
    print(post)
    return {"post_detail": post}
