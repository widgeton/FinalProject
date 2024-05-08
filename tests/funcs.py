from sqlalchemy import select, delete, insert


async def clean_table(async_session, model):
    await async_session.execute(delete(model))


async def get_item(async_session, model, id):
    return await async_session.scalar(select(model).filter_by(id=id))


async def get_all_items(async_session, model):
    items = await async_session.scalars(select(model))
    return items.all()


async def add_item(async_session, model, data):
    await async_session.execute(insert(model).values(**data))
