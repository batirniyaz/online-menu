from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.auth.database import User, get_async_session
from app.auth.manager import get_user_manager
from app.auth.schemas import UserRead, UserCreate
from app.config import SECRET_KEY

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = SECRET_KEY
router = APIRouter()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=None)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router_def = APIRouter()


@router_def.delete("/delete")
async def delete_user(db: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    res = await db.execute(select(User).filter_by(id=user.id))
    db_user = res.scalars().first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    await db.delete(db_user)
    await db.commit()

    response = JSONResponse(content={"detail": "User deleted"})
    response.delete_cookie(key="Authorization")
    return response


@router_def.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


router.include_router(router_def, prefix="/auth", tags=["auth"])
