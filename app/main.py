from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor


app = FastAPI()

# this class defines the fields needed in a post message
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    


# request GET method url: "/", order DOES matter
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='api_dev', user= 'postgres', 
                password = 'postgresql1', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "Hello World, this is my api"}

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":"favorite foods", "content": "I love pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id :
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/posts")
def get_posts():
    return {"data": my_posts} 

# payLoad is the variable to store all the body data it is of type dictionary and 
# it's going to extract all of the fields from Body and convert it into a python dictionary
# and store it into payLoad
# @app.post("/createposts")
# def create_posts(payload : dict = Body(...)):
#     print(payload)
#     return {"new_post" : f"Title: {payload['title']} Content:{payload['content']}"}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data" : post_dict} 


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)

    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index =find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    index =find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")
    post_dict =post.dict()
    post_dict['id'] =  id
    my_posts[index] = post_dict
    print(post)
    return {'message': 'Updated post'}

    