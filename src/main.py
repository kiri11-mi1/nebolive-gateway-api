from fastapi import FastAPI

from report import generate_report
from service import get_nebolive_service, NeboliveService
from fastapi import Depends
from pydantic import BaseModel

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


class ResponseNestedSchema(BaseModel):
    text: str
    end_session: bool = True


class YandexStationResponse(BaseModel):
    response: ResponseNestedSchema
    version: str = '1.0'


@app.post('/station/v1/', response_model=YandexStationResponse)
async def station(nebolive: NeboliveService = Depends(get_nebolive_service)):
    aqi = nebolive.exact_aqi()
    return YandexStationResponse(
        response=ResponseNestedSchema(
            text=generate_report(aqi=aqi),
            end_session=True,
        )
    )
