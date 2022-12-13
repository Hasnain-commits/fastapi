from .. import schemas
from ..utils import cursor, conn
from fastapi import HTTPException, Response, APIRouter, Depends
from ..oauth2 import get_current_user
from typing import Optional

router = APIRouter(prefix="/api/posts", tags=['Posts'])


@router.get("/", response_model=schemas.Post_Response, status_code=200)
def get_posts(user_id: int = Depends(get_current_user), limit: int = 5, offset: int = 0, search: str = ''):

    if len(search):
        search += '%'

        cursor.execute(""" SELECT posts.*, COUNT(likes.post_id) AS post_likes
            FROM posts LEFT JOIN likes ON posts.id = likes.post_id 
            WHERE title LIKE %s
            GROUP BY posts.id OFFSET %s LIMIT %s """, (search, offset, limit))
    else:
        cursor.execute(""" SELECT posts.*, COUNT(likes.post_id) AS post_likes
            FROM posts LEFT JOIN likes ON posts.id = likes.post_id 
            GROUP BY posts.id OFFSET %s LIMIT %s """, (offset, limit))

    posts = cursor.fetchall()
    return posts


@router.post("/", status_code=201, response_model=schemas.Post_Response)
def create_post(post: schemas.Post_Create, user_id: int = Depends(get_current_user)):
    cursor.execute(""" INSERT INTO posts (user_id, title, content, published) VALUES (%s, %s, %s, %s) RETURNING * """,
                   (user_id.id, post.title, post.content, post.published))

    created_post = cursor.fetchone()

    conn.commit()
    return created_post


@router.get("/{id}", status_code=200, response_model=schemas.Post_Response)
def get_post(id: int, user_id: int = Depends(get_current_user)):
    cursor.execute(""" SELECT posts.*, COUNT(likes.post_id) AS post_likes 
	FROM posts LEFT JOIN likes ON likes.post_id = posts.id 
	WHERE posts.id = %s GROUP BY posts.id """, (id, ))

    found_post = cursor.fetchone()

    if not found_post:
        raise HTTPException(status_code=404, detail=f"Post not found")

    return found_post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, user_id: int = Depends(get_current_user)):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    found_post = cursor.fetchone()

    if not found_post:
        raise HTTPException(status_code=404, detail=f"Post not found")

    if found_post['user_id'] != int(user_id.id):
        raise HTTPException(status_code=401, detail=f"Incorrect permissions")

    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id, ))
    conn.commit()
    return Response(status_code=204)


@router.put("/{id}", response_model=schemas.Post_Response)
def update_post(id: int, post: schemas.Post_Create, user_id: int = Depends(get_current_user)):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    found_post = cursor.fetchone()

    if not found_post:
        raise HTTPException(status_code=404, detail=f"Post not found")

    if found_post['user_id'] != int(user_id.id):
        raise HTTPException(status_code=401, detail=f"Incorrect permissions")

    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, id))

    updated_post = cursor.fetchone()
    conn.commit()
    return updated_post
