from app.config import settings
from app.database.repositories import user_repository
from app.middleware.error_handler import AuthenticationError, NotFoundError, ValidationError
from app.models.user import UserCreate
from app.schemas.auth import (
    ChangePasswordRequest,
    ProfileUpdateRequest,
    SettingsUpdateRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.utils.security import create_access_token, hash_password, verify_password
from app.utils.text_utils import sanitize_email, sanitize_text


def _build_user_response(user: dict) -> UserResponse:
    return UserResponse(
        id=str(user["_id"]),
        full_name=user["full_name"],
        email=user["email"],
        created_at=user["created_at"].isoformat(),
        has_gemini_api_key=bool(user.get("gemini_api_key")),
    )


def _build_token_response(user: dict) -> TokenResponse:
    user_id = str(user["_id"])
    return TokenResponse(
        access_token=create_access_token(user_id),
        expires_in=settings.jwt_expire_minutes * 60,
        user=_build_user_response(user),
    )


async def register_user(payload: UserRegisterRequest) -> TokenResponse:
    email = sanitize_email(payload.email)
    full_name = sanitize_text(payload.full_name, max_length=100)

    existing_user = await user_repository.find_by_email(email)
    if existing_user:
        raise ValidationError("An account with this email already exists.")

    user_document = await user_repository.create_user(
        UserCreate(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(payload.password),
        )
    )

    return _build_token_response(user_document)


async def login_user(payload: UserLoginRequest) -> TokenResponse:
    email = sanitize_email(payload.email)

    user = await user_repository.find_by_email(email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise AuthenticationError("Invalid email or password.")

    return _build_token_response(user)


async def get_user_by_id(user_id: str) -> dict:
    user = await user_repository.find_by_id_str(user_id)
    if not user:
        raise NotFoundError("User not found.")
    return user


async def get_user_profile(user_id: str) -> UserResponse:
    user = await get_user_by_id(user_id)
    return _build_user_response(user)


async def update_user_profile(user_id: str, payload: ProfileUpdateRequest) -> UserResponse:
    full_name = sanitize_text(payload.full_name, max_length=100)
    updated = await user_repository.update_profile(user_id, full_name)
    if not updated:
        raise NotFoundError("User not found.")
    return _build_user_response(updated)


async def update_user_settings(user_id: str, payload: SettingsUpdateRequest) -> UserResponse:
    await user_repository.update_gemini_api_key(user_id, payload.gemini_api_key)
    user = await get_user_by_id(user_id)
    return _build_user_response(user)


async def change_user_password(user_id: str, payload: ChangePasswordRequest) -> None:
    from app.utils.text_utils import utc_now

    user = await get_user_by_id(user_id)

    if not verify_password(payload.current_password, user["hashed_password"]):
        raise AuthenticationError("Current password is incorrect.")

    if verify_password(payload.new_password, user["hashed_password"]):
        raise ValidationError("New password must be different from the current password.")

    await user_repository.update_by_id(
        user["_id"],
        {"$set": {"hashed_password": hash_password(payload.new_password), "updated_at": utc_now()}},
    )


async def get_user_gemini_api_key(user_id: str) -> str | None:
    user = await get_user_by_id(user_id)
    return user.get("gemini_api_key")
