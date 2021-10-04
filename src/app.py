import os

from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from routers import beatmaps

app = FastAPI()
app.include_router(beatmaps.router)


@app.get('/')
async def index():
    index_page = FileResponse('dist/index.html')
    return index_page


dist_directory = os.path.join(os.getcwd(), "dist")
app.mount("/", StaticFiles(directory=dist_directory), name='dist')
