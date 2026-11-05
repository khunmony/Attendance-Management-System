import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import Role


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    email: str  # plain str on output: stored values are already validated on input
    first_name: str
    last_name: str
    role: Role
    is_active: bool
