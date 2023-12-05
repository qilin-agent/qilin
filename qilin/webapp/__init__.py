from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from qilin.webapp.bots import create_bots_router


STATIC_FOLDER = './qilin-fe/build/static'
STATIC_URL_PATH = '/static'


def create_webapp():
    app = FastAPI()
    
    app.include_router(create_bots_router(), prefix='/api')

    app.mount(STATIC_URL_PATH, StaticFiles(directory=STATIC_FOLDER, html=True), name="static")

    @app.get("/{static_file}")
    async def get_static_file(static_file: str):
        # Get media type from file extension for .ico, .png, .html, .json, .txt
        if static_file.endswith('.ico'):
            media_type = 'image/x-icon'
        elif static_file.endswith('.png'):
            media_type = 'image/png'
        elif static_file.endswith('.html'):
            media_type = 'text/html'
        elif static_file.endswith('.json'):
            media_type = 'application/json'
        elif static_file.endswith('.txt'):
            media_type = 'text/plain'
        else:
            media_type=None
        return FileResponse(f'./qilin-fe/build/{static_file}', media_type=media_type)

    @app.get("/{file_path:path}")
    async def index(request: Request):
        return FileResponse(f'./qilin-fe/build/index.html', media_type='text/html')
        
    return app
