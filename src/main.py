from fastapi import FastAPI

from src.schemas import ServerResponse, ResponseNestedSchema

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.post('/hello/')
async def hello():
    return ServerResponse(
        response=ResponseNestedSchema(text='Привет, мир!'),
    )
