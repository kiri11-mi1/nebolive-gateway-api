from fastapi import FastAPI, Query

from schemas import YandexStationResponse, ResponseNestedSchema
from service import generate_report, get_nebolive_service, NeboliveService
from fastapi import Depends

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.post('/station/v1/', response_model=YandexStationResponse)
async def station(
    city: str = Query(..., description='Город'),
    nebolive: NeboliveService = Depends(get_nebolive_service),
):
    aqi = nebolive.aqi_in_city(city)
    return YandexStationResponse(
        response=ResponseNestedSchema(
            text=generate_report(aqi=aqi),
            end_session=True,
        )
    )


@app.post('/station/v2/', response_model=YandexStationResponse)
async def station(
    long: float = Query(..., description='Долгота'),
    lat: float = Query(..., description='Широта'),
    nebolive: NeboliveService = Depends(get_nebolive_service),
):
    pass
