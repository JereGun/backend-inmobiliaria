from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash # Assuming this will be created in a later step

class CRUDUsuario:
    def get_user(self, db: Session, user_id: int):
        return db.query(Usuario).filter(Usuario.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Usuario).offset(skip).limit(limit).all()

    def create_user(self, db: Session, *, obj_in: UsuarioCreate) -> Usuario:
        db_obj = Usuario(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password), # Hashing the password
            is_active=obj_in.is_active if obj_in.is_active is not None else True,
            is_superuser=obj_in.is_superuser if obj_in.is_superuser is not None else False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_user(
        self, db: Session, *, db_obj: Usuario, obj_in: UsuarioUpdate
    ) -> Usuario:
        update_data = obj_in.model_dump(exclude_unset=True) # Use model_dump
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"] # remove plain password
            update_data["hashed_password"] = hashed_password # add hashed password

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_user(self, db: Session, *, id: int) -> Usuario:
        obj = db.query(Usuario).get(id)
        db.delete(obj)
        db.commit()
        return obj

usuario = CRUDUsuario()
