from ..utils import cursor, conn, verify
from ..oauth2 import create_access_token
from ..schemas import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import HTTPException, APIRouter, Response, Depends

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login_user(req: OAuth2PasswordRequestForm = Depends()):
    cursor.execute(""" SELECT * FROM users WHERE email = %s """,
                   (req.username, ))

    found_user = cursor.fetchone()

    if not found_user or not verify(req.password, found_user['password']):
        raise HTTPException(status_code=403, detail="Incorrect Credentials")

    # After veryifying password and that user exists give JWT Token
    access_token = create_access_token(data={"user_id": found_user['id']})

    return {"access_token": access_token, "token_type": "bearer"}
