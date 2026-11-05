from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.enums import Role
from app.models.user import User


def require_roles(*roles: Role):
    """Dependency: allow only users whose role is in `roles`.

    Usage:  @router.post("/...", dependencies=[Depends(require_roles(Role.ADMIN))])
    or:     user: User = Depends(require_roles(Role.ADMIN, Role.TEACHER))
    """

    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")
        return user

    return checker
