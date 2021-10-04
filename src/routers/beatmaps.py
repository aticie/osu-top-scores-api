import os

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
    scores_collection: AsyncIOMotorCollection = db["scores"]

    query = create_query_from_mod(mod, include_hd)
    aggregation = [
        {'$match': query},
        {'$group': {'_id': "$beatmap_id", 'play_count': {'$count': {}}, 'avg_pp': {'$avg': '$pp'},
                    'beatmapset_id': {'$first': "$beatmapset_id"}, 'mods': {'$addToSet': '$mods'}}},
        {'$sort': {'play_count': -1}},
        {'$limit': top_n}
    ]
    results = []
    async for score in scores_collection.aggregate(aggregation):
        score['beatmap_id'] = score['_id']
        results.append(score)

    return {'beatmaps': results}
