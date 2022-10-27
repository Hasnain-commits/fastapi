from fastapi import FastAPI, HTTPException, Response
from . import schemas
import psycopg2
import time
from psycopg2.extras import RealDictCursor


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", user="pg4e", dbname="fastapi", password="secret", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print({"Error": error})
        time.sleep(2)


@app.get("/")
def root():
    print("Hello World!")


@app.get("/api/posts", response_model=list[schemas.Post_Response], status_code=200)
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)

    posts = cursor.fetchall()

    return posts


@app.post("/api/posts", status_code=201, response_model=schemas.Post_Response)
def create_post(post: schemas.Post_Create):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    (post.title, post.content, post.published))

    created_post = cursor.fetchone()

    conn.commit()

    return created_post


@app.get("/api/posts/{id}", status_code=200, response_model=schemas.Post_Response)
def find_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    
    found_post = cursor.fetchone() 

    if not found_post:
        raise HTTPException(status_code=404, detail=f"Post with {id} was not found in our database") 

    return found_post


@app.delete("/api/posts/{id}", status_code=204)
def find_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id, ))
    
    found_post = cursor.fetchone()

    if not found_post:
        raise HTTPException(status_code=404, detail=f"Post with {id} was not found in our database") 

    conn.commit()

    return Response(status_code=204)


@app.put("/api/posts/{id}", response_model=schemas.Post_Response)
def update_post(id: int, post: schemas.Post_Create):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """,
    (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(status_code=404, detail=f"Post with {id} was not found in our database") 
    
    conn.commit()

    return updated_post



@app.post("/api/users", status_code=201)
def create_user(user: schemas.User_Create):
    cursor.execute(""" SELECT * FROM users WHERE email = %s """, (user.email, ))

    found_user = cursor.fetchone()

    if found_user:
        raise HTTPException(status_code=404, detail=f"A user with the email : {user.email} already exists")  

    cursor.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """, (user.email, user.password))

    conn.commit()

    created_user = cursor.fetchone()

    return created_user

