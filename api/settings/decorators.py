from functools import wraps
from fastapi import Depends, HTTPException, status
from user.backend import get_user
from typing import List

role = [
    "ADMIN",
    "HOST",
]


def role_required(allowed_roles: List[str]):
    if not allowed_roles:
        raise ValueError("Allowed roles must be provided")

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user_id: str, **kwargs):
            user = await get_user(user_id)
            if user["role"] not in (role + allowed_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied",
                )
            return await func(*args, user=user, **kwargs)

        return wrapper

    return decorator
