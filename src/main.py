from fastapi import FastAPI


app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json'
)


@app.get('/hello/')
async def hello():
    return {
        "response": {
            "end_session": True,
            "text": "Привет и тебе!"
        },
        "version": "1.0",
    }
