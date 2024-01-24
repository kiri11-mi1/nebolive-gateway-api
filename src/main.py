from fastapi import FastAPI, Query

from schemas import YandexStationResponse, ResponseNestedSchema
from service import get_nebolive_service, NeboliveService
from fastapi import Depends

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.post('/station/')
async def station(
    city: str = Query(..., description='Город'),
    nebolive: NeboliveService = Depends(get_nebolive_service),
):
    nebolive_report = nebolive.get_report_by_city(city)
    return {
        'response': {
            'text': nebolive_report.message,
            'value': nebolive_report.aqi,
            'end_session': True,
            'buttons': [
                {
                    "title": "234",
                    "payload": {},
                    "url": "https://nebo.live/ru/",
                    "hide": True,
                },
            ],
        },
        "session_state": {
            "value": 10
        },
        "user_state_update": {
            "value": 42
        },
        "application_state": {
            "value": 37
        },
        'version': '1.0',
    }
