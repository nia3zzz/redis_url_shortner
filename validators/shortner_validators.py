from pydantic import BaseModel, Field


class CreateShortURLValidator(BaseModel):
    url: str = Field(min_length=8, max_length=2000)
