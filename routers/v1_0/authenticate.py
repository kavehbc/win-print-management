from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils.authentication import authenticate


router = APIRouter(
    tags=["v0.1"],
)


@router.post("/authenticate", include_in_schema=False)
def authentication(form_data: OAuth2PasswordRequestForm = Depends()):
    return authenticate(form_data)
