from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from qilin.webapp.bots import create_bots_router


STATIC_FOLDER = './qilin-fe/build/'
STATIC_URL_PATH = '/'


def create_webapp():
    app = FastAPI()
    app.mount(STATIC_URL_PATH, StaticFiles(directory=STATIC_FOLDER), name="static")

    @app.get("/")
    @app.get("/{resource}")
    async def index(request: Request):
        return RedirectResponse(url='/index.html')
    
    app.include_router(create_bots_router())
        
    return app