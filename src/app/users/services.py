from .models import User as User_Model
from sqlalchemy.orm import Session
from .schemas import UserCreate, User, UserUpdate

async def get_user_by_id(user_id: int, db: Session) -> User_Model:
    return db.query(User_Model).filter(User_Model.id == user_id).first()

async def get_all_user(db: Session):
    return db.query(User_Model).all()

async def create(*, user=UserCreate, db: Session):
    user_obj = User_Model(
        full_name=user.full_name,
        emergency_contact_person=user.emergency_contact_person,
        emergency_contact_number=user.emergency_contact_number,
        password=user.password
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return User.model_validate(user_obj)

async def update(*, user_db: User_Model, obj: UserUpdate, db: Session):
    user_data = obj.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)

    return User.model_validate(user_db)