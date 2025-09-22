from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class VersionOut(BaseModel):
    app: str 
    version: str 


@router.get("/version", response_model=VersionOut)
def version() -> VersionOut:
    return VersionOut(app="tasks-api", version="0.1.0")