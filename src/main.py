from fastapi import FastAPI, Query

from src.schemas import YandexStationResponse, ResponseNestedSchema

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.post('/station/', response_model=YandexStationResponse)
async def station(
    latitude: float = Query(..., description='Широта'),
    longitude: float = Query(..., description='Долгота'),
):
    return YandexStationResponse(
        response=ResponseNestedSchema(text='Привет, мир!'),
    )
