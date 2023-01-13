from fastapi import FastAPI, Response, status, HTTPException
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

def find_bird_index(id):
    for x, bird in enumerate(bird_posts):
        if bird["id"] == id:
            return x

@api.get("/")
async def root():
    return{"message": "Hi there, Python."}

@api.get("/posts")
async def get_birds():
    return {"data": bird_posts}

@api.post("/posts", status_code=status.HTTP_201_CREATED)
async def get_birds(birdData: bird_data):
    post_dict = birdData.dict()
    post_dict["id"] = randrange(3, 1000000)
    bird_posts.append(post_dict)
    return{"data": post_dict}

@api.get("/posts/{id}")
async def get_bird(id: int):
    post = find_bird(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID number {id} was not found..."
        )
    return {"post_detail": post}

@api.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bird(id: int):
    index = find_bird_index(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID number {id} was not found..."
            )
    
    bird_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Back to the End - Rama
#Warrior - Mulperi 

# Don't mind me, just taking done some song names I'm listening to here...