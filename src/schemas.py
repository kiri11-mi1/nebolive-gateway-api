from pydantic import BaseModel


class ResponseNestedSchema(BaseModel):
    text: str
    end_session: bool = True


class ServerResponse(BaseModel):
    response: ResponseNestedSchema
    version: str = '1.0'
