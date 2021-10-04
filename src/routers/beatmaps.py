import os
import time
from collections import Counter

import motor.motor_asyncio
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter(prefix="/beatmaps",
                   tags=["beatmaps"],
                   responses={404: {"description": "Not found"}},
                   )

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"], username='root', password='verysecret')
db = client.database


def create_query_from_mod(mod: str, include_hd: bool):
    mod = mod.upper()
    if mod == 'ANY':
        if include_hd:
            return
        query = {'mods': {'$ne': 'HD'}}
        return query

    if mod == '':
        if include_hd:
            query = {'$or': [{'mods': []}, {'mods': ['HD']}]}
        else:
            query = {'mods': []}
        return query

    if include_hd:
        if mod == 'DT':
            query = {'$or': [{'mods': mod}, {'mods': [mod, 'HD']}, {'mods': 'NC'}, {'mods': {'$all': ['NC', 'HD']}}]}
        else:
            query = {'$or': [{'mods': mod}, {'mods': {'$all': [mod, 'HD']}}]}
    else:
        query = {'mods': {'$and': [{'$all': [mod]}, {'$ne': ['HD']}]}}

    return query


@router.get(
    "", response_description="List all beatmaps"
)
async def list_beatmaps(mod: str = '', include_hd: bool = True, top_n: int = 5):
    start_time = time.time()
    beatmaps = Counter()
    total_pp = Counter()
    beatmap_mods = {}
    scores_collection: AsyncIOMotorCollection = db["scores"]

    query = create_query_from_mod(mod, include_hd)

    async for score in scores_collection.find(query):
        beatmap_id = score['beatmap_id']
        total_pp[beatmap_id] += score['pp']
        beatmaps[beatmap_id] += 1

        if beatmap_id in beatmap_mods:
            beatmap_mods[beatmap_id].add(','.join(score['mods']))
        else:
            beatmap_mods[beatmap_id] = {','.join(score['mods'])}

    elapsed_time = f'{time.time() - start_time:.2f}'

    returned_beatmaps = []
    for bmap, play_count in beatmaps.most_common(top_n):
        returned_beatmaps.append({'beatmap_id': bmap,
                                  'play_count': play_count,
                                  'avg_pp': total_pp[bmap] / play_count,
                                  'mods': beatmap_mods[bmap]})
    return {'beatmaps': returned_beatmaps,
            'query_time': elapsed_time}
