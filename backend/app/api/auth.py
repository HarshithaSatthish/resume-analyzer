from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.middleware.auth import get_current_user_id
from app.schemas.auth import (
    ChangePasswordRequest,
    LogoutResponse,
    ProfileUpdateRequest,
    SettingsUpdateRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.services.auth_service import (
    change_user_password,
    get_user_profile,
    login_user,
    register_user,
    update_user_profile,
    update_user_settings,
)

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, summary="Register a new user")
async def register(payload: UserRegisterRequest) -> TokenResponse:
    return await register_user(payload)


@router.post("/login", response_model=TokenResponse, summary="Login with email and password")
async def login(payload: UserLoginRequest) -> TokenResponse:
    return await login_user(payload)


@router.post("/logout", response_model=LogoutResponse, summary="Logout current user")
async def logout(
    _: Annotated[str, Depends(get_current_user_id)],
) -> LogoutResponse:
    return LogoutResponse()


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_me(user_id: Annotated[str, Depends(get_current_user_id)]) -> UserResponse:
    return await get_user_profile(user_id)


@router.put("/profile", response_model=UserResponse, summary="Update user profile")
async def update_profile(
    payload: ProfileUpdateRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> UserResponse:
    return await update_user_profile(user_id, payload)


@router.put("/settings", response_model=UserResponse, summary="Update user settings")
async def update_settings(
    payload: SettingsUpdateRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> UserResponse:
    return await update_user_settings(user_id, payload)


@router.put("/password", response_model=MessageResponse, summary="Change password")
async def update_password(
    payload: ChangePasswordRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> MessageResponse:
    await change_user_password(user_id, payload)
    return MessageResponse(message="Password updated successfully.")
