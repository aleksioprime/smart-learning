from uuid import UUID
from typing import List

from src.repositories.uow import UnitOfWork
from src.schemas.user import UserUpdate, UserSchema
from src.serializers.user import BaseSerializer
from src.models.user import User

class UserService:

    def __init__(self, uow: UnitOfWork, serializer: BaseSerializer):
        self.uow = uow
        self.serializer = serializer

    async def get_user_all(self) -> List[UserSchema]:
        """
        Выдаёт информацию обо всех пользователях
        """
        async with self.uow:
            users = await self.uow.user.get_user_all()

        return [self.serializer.serialize(user) for user in users]

    async def get_user_by_id(self, user_id: UUID) -> UserSchema:
        """
        Выдаёт информацию о пользователе
        """
        async with self.uow:
            user = await self.uow.user.get_user_by_id(user_id)

        return self.serializer.serialize(user)

    async def update(self, user_id: UUID, body: UserUpdate) -> UserSchema:
        """
        Обновляет информацию о пользователе
        """
        async with self.uow:
            user = await self.uow.user.update(user_id, body)

        return self.serializer.serialize(user)

    async def delete(self, user_id: UUID):
        """
        Удаляет пользователя из базы данных
        """
        async with self.uow:
            await self.uow.user.delete(user_id)
