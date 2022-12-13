from .. import schemas
from ..utils import cursor, conn, hash
from fastapi import HTTPException, APIRouter, Depends
from ..oauth2 import get_current_user


router = APIRouter(prefix="/api/users", tags=['Users'])


@router.post("/", status_code=201)
def create_user(user: schemas.User_Create):
    cursor.execute(
        """ SELECT * FROM users WHERE email = %s """, (user.email, ))
    found_user = cursor.fetchone()

    if found_user:
        raise HTTPException(
            status_code=404, detail=f"Email has already been signed up with")

    user.password = hash(user.password)
    cursor.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """,
                   (user.email, user.password))
    created_user = cursor.fetchone()

    conn.commit()
    return created_user


@router.get("/{id}", status_code=200)
def get_user(id: int):
    cursor.execute(""" SELECT * FROM users WHERE id = %s """, (id, ))
    found_user = cursor.fetchone()

    if not found_user:
        raise HTTPException(status_code=404, detail=f"User doesn't exist")

    return found_user


@router.get("/{id}/posts", status_code=201)
def get_user_posts(id: int, user_id: int = Depends(get_current_user)):
    if int(user_id.id) != id:
        raise HTTPException(status_code=401, detail=f"Incorrect permissions")

    cursor.execute(""" SELECT * FROM posts WHERE user_id = %s """, (id,))
    posts = cursor.fetchall()

    return posts
