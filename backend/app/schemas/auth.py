from __future__ import annotations

from pydantic import BaseModel, Field


class Credentials(BaseModel):
    """Payload for /auth and /authentication login/password input."""
    login: str = Field(..., max_length=254)
    password: str = Field(..., min_length=6)


class RegisterPayload(BaseModel):
    """Data for registering a new account with selected roles."""
    login: str = Field(..., max_length=254)
    password: str = Field(..., min_length=6)
    roles: str = Field(..., description="Role codes separated by whitespace (e.g. \"0 2\")")


class TokenResponse(BaseModel):
    """JWT response returned when issuing a token."""
    access_token: str
    token_type: str = "bearer"
    role: int


class RoleSelection(BaseModel):
    """Explicit role selection payload for /authentication."""
    login: str = Field(..., max_length=254)
    password: str = Field(..., min_length=6)
    role: int = Field(..., ge=0, le=4)


class AdminTokenRequest(BaseModel):
    """Admin request to issue a token for another user."""
    login: str = Field(..., max_length=254)
    role: int = Field(..., ge=0, le=4)


class MultiRoleResponse(BaseModel):
    """Roles offered when a user has multiple options."""
    roles: list[int]

