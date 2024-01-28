from fastapi import FastAPI, Query

from schemas import YandexStationResponse, ResponseNestedSchema
from service import get_nebolive_service, NeboliveService
from fastapi import Depends

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.post('/station/', response_model=YandexStationResponse)
async def station(
    city: str = Query(..., description='Город'),
    nebolive: NeboliveService = Depends(get_nebolive_service),
):
    nebolive_report = nebolive.get_report_by_city(city)
    return YandexStationResponse(
        response=ResponseNestedSchema(
            text=nebolive_report.message,
            end_session=True,
        )
    )
