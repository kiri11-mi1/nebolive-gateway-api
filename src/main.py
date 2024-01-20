from fastapi import FastAPI


app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.post('/hello/')
async def hello():
    return {
        "response": {
            "end_session": True,
            "text": "Оксана ты жопка"
        },
        "version": "1.0",
    }
