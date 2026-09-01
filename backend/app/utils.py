from datetime import date, datetime
from uuid import UUID

from sqlalchemy.inspection import inspect


def serialize(obj, extra: dict | None = None) -> dict:
    data: dict = {}
    for col in inspect(obj).mapper.column_attrs:
        val = getattr(obj, col.key)
        if isinstance(val, UUID):
            val = str(val)
        elif isinstance(val, datetime):
            val = val.isoformat()
        elif isinstance(val, date):
            val = val.isoformat()
        data[col.key] = val
    if extra:
        data.update(extra)
    return data
