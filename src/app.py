import os
import time
from collections import Counter

import motor.motor_asyncio
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from routers import beatmaps

app = FastAPI()
app.include_router(beatmaps.router)

