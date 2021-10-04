import time
import os
from collections import Counter

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import APIRouter

router = APIRouter(prefix="/beatmaps",
    tags=["beatmaps"],
    responses={404: {"description": "Not found"}},
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"], username='root', password='verysecret')
db = client.database



@router.get(
    "/", response_description="List all beatmaps"
)
async def list_beatmaps(mods: str = '', top_n: int = 5):
    start_time = time.time()
    beatmaps = Counter()
    total_pp = Counter()
    scores_collection: AsyncIOMotorCollection = db["scores"]



    async for score in scores_collection.find({'$or': [{'mods': 'HD,HR'}, {'mods': 'HR'}]}):
        beatmap_id = score['beatmap_id']
        total_pp[beatmap_id] += score['pp']
        beatmaps[beatmap_id] += 1

    elapsed_time = f'{time.time() - start_time:.2f}'

    returned_beatmaps = []
    for bmap, play_count in beatmaps.most_common(top_n):
        returned_beatmaps.append({'beatmap_id': bmap,
                                  'play_count': play_count,
                                  'avg_pp': total_pp[bmap]/play_count})
    return {'beatmaps': returned_beatmaps,
            'query_time': elapsed_time}