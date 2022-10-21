from pydantic import BaseModel


class History(BaseModel):
    history: dict
