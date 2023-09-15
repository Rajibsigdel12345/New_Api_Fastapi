from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

# data model


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default true


while (True):

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='Fromhell', cursor_factory=RealDictCursor)  # bad practice
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)


# my_posts = [{"title": "title content", "content": "content", 'id': 1}, {
#     'title': "Favourite", "content": "pizza", "id": 2}]

# for memory  database
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get("/")  # routing
async def root():
    # async for calling api asunchronously
    return {"message": "Welcome to my program"}
# converts dictionary to json
# no need to manually serialize


@app.get('/posts')  # looks for first matching path if duplicate path
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


# @app.post('/createpost')  # bad practice '/posts' ie plural
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.published))  # no sql injection so no format f string
    newpost = cursor.fetchone()
    conn.commit()
    print(post.model_dump())  # .dict deprecated
    return {'data': newpost}

# title as string, content as string form post optional category and bool published


@app.get('/posts/{id}')  # id = path parameter as string convert to int
def get_posts(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id:{id} was not found"}
    return {"detail": test_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} doesnt exists')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content= %s, published= %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)  # check in database
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} doesnt exists')
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    print(post)
    return {"data": updated_post}
