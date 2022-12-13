from fastapi import HTTPException, Response, APIRouter, Depends
from ..utils import cursor, conn
from .. import schemas
from ..oauth2 import get_current_user

router = APIRouter(prefix="/api/vote", tags=["Votes"])


@router.post("/", status_code=200)
def handle_vote(req: schemas.Vote, user_id: int = Depends(get_current_user)):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (req.post_id,))
    found_post = cursor.fetchone()

    if not found_post:
        raise HTTPException(status_code=400, detail="Post doesn't exist")

    cursor.execute(
        """ SELECT * FROM likes WHERE (post_id, user_id) = (%s, %s) """, (req.post_id, int(user_id.id)))

    found_like = cursor.fetchone()

    if req.vote_dir == 1:
        if found_like:
            raise HTTPException(status_code=400, detail="Already liked post")

        cursor.execute(
            """ INSERT INTO likes (post_id, user_id) VALUES (%s, %s) """, (req.post_id, int(user_id.id)))
        conn.commit()
    elif req.vote_dir == 0:
        if not found_like:
            raise HTTPException(status_code=400, detail="Post does not exist")

        cursor.execute(
            """ DELETE FROM likes WHERE (post_id, user_id) = (%s, %s) """, (req.post_id, int(user_id.id)))
        conn.commit()
    else:
        raise HTTPException(status_code=400, detail="Invalid")
