from sqlalchemy.exc import IntegrityError

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions.auth_exception import (
    InvalidCredentialsError,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import (
    AuthenticatedUser,
    UserLogin,
    UserRegistration,
)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, data: UserRegistration) -> AuthenticatedUser:
        if self.user_repository.user_exists(data.email):
            raise InvalidCredentialsError()

        password_hash = hash_password(data.password)

        try:
            user = self.user_repository.create_user(
                email=data.email,
                password_hash=password_hash,
            )
        except IntegrityError:
            raise InvalidCredentialsError()

        return AuthenticatedUser.model_validate(user)

    def login(self, data: UserLogin) -> str:
        user = self.user_repository.get_user_by_email(
            data.email,
        )

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError()

        return create_access_token(str(user.id))

    def get_authenticated_user(self, user_id: str) -> AuthenticatedUser:
        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError()

        return AuthenticatedUser.model_validate(user)