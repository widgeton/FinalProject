from typing import override

from sqlalchemy import select, bindparam

from utils.repository import SQLAlchemyDelRepository
from models import DepartmentModel


class DepartmentRepository(SQLAlchemyDelRepository):
    model = DepartmentModel

    @override
    async def update(self, id_, **fields) -> type(model):
        old_path = None
        if "old_path" in fields:
            old_path = fields.pop("old_path")

        dep = await super().update(id_, **fields)

        if old_path:
            query = select(self.model).filter(self.model.path.like(bindparam('old_path') + '.%'))
            res = await self.session.scalars(query, {"old_path": old_path})
            new_path = dep.path.split('.')
            old_path_len = len(old_path.split('.'))
            for child in res.all():
                path = child.path.split(".")
                path[:old_path_len] = new_path
                child.path = '.'.join(path)
        return dep
