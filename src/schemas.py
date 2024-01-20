from pydantic import BaseModel


class ResponseNestedSchema(BaseModel):
    text: str
    end_session: bool = True


class YandexStationResponse(BaseModel):
    response: ResponseNestedSchema
    version: str = '1.0'
