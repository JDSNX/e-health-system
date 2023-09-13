from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.app.users.services import create, get_all_user, get_user_by_id, update
from src.app.database.core import get_db
from src.app.schemas import UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_user(*, db: Session):
    user = await get_all_user(db=db)

    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOTFOUND,
            detail="Could not generate users"
        )
    
    return user


@router.post("/")
async def create_user(user_in: UserCreate, db: Session=Depends(get_db)) -> dict[str, str]:
    _user = await create(user=user_in, db=db)

    return _user

@router.put("/{user_id}")
async def update_user(user_id: int, db: Session, *, user_obj: UserUpdate):
    user = await get_user_by_id(user_id=user_id, db=db)

    if user:
        await update(user_db=user, obj=user_obj)

    return user