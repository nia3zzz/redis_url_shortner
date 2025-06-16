from pydantic import BaseModel, Field


class CreateShortURLValidator(BaseModel):
    url: str = Field(min_length=8, max_length=2000)


class RedirectedShortURLValidator(BaseModel):
    shortened_url: str = Field(min_length=6, max_length=6)
