from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import pyodbc
import pandas as pd
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#calling fastapi
api = FastAPI()

class bird_data(BaseModel):
    birdID: int
    birdName: str
    birdSciName: str
    birdDescription: str
    eggsPerSeasonMIN: int
    eggsPerSeasonMAX: int
    Threat: str
    habitats: str

while True:
    try:
        cnxn_str = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + os.getenv("SERVER_NAME") + ";DATABASE=" + os.getenv("DATABASE_NAME") + ";Trusted_Connection=yes;")
        cursor = cnxn_str.cursor()
        print("A okay!")
        break
    except Exception as error:
        ("oof!")
        print("Error", error)
        time.sleep(3)

cursor = cursor.execute("""SELECT * FROM dbo.Birds """)
columns = [column[0] for column in cursor.description]
results = []
for row in cursor.fetchall():
    results.append(dict(zip(columns, row)))

bird_posts = [
{
    "birdName": "African red-eyed bulbul",
    "birdSciName": "Pycnonotus nigricans",
    "birdDescription": "The African red-eyed bulbul has greyish/brown plumage on its upper parts, extending onto the chest, with white plumage on their underparts.",
    "eggsPerSeasonMIN": 2,
    "eggsPerSeasonMAX": 3,
    "Threat": "None",
    "id": 1
},
{
    "birdName": "African Black Oystercatcher",
    "birdSciName": "Haematopus moquini",
    "birdDescription": "The adult oystercatcher is entirely black with bright red eyes surrounded by an orange ring. The wedge-like orange-tipped red bill is somewhat longer than the head and the mandibles do not meet at the tip.",
    "eggsPerSeasonMIN": 1,
    "eggsPerSeasonMAX": 4,
    "Threat": "Mild",
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
    return {"data": results}

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

@api.put("/post/{id}")
async def update_bird(id: int, post: bird_data):
    index = find_bird_index(id) #Find index

    if index == None: #Error 404 if we cannot find the index
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID number {id} was not found..."
            )

    post_dict = post.dict() #take the data from front-end and convert it to a dictionary
    post_dict["id"] = id # grabbing the id of the post
    bird_posts[index] = post_dict #update the post within the array
    return{"data": post_dict}