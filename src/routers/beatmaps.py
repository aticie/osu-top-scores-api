import os
import time
from typing import Tuple

import motor.motor_asyncio
from fastapi import APIRouter, Query
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter(prefix="/beatmaps",
                   tags=["beatmaps"],
                   responses={404: {"description": "Not found"}},
                   )

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client.Farmer
scores_collection: AsyncIOMotorCollection = db["Scores"]


def create_query_from_mod(mod: str, pp_range: Tuple[int, int], include_hd: bool):
    mod = mod.upper()

    pp_query = {'$and': [{'pp': {'$gt': pp_range[0]}}, {'pp': {'$lt': pp_range[1]}}]}

    if mod == 'ANY':
        if include_hd:
            return pp_query
        query = {'$and': [{'mods': {'$ne': 'HD'}}, pp_query]}
        return query

    if mod == '':
        if include_hd:
            query = {'$and': [{'$or': [{'mods': []}, {'mods': ['HD']}]}, pp_query]}
        else:
            query = {'$and': [{'mods': []}, pp_query]}
        return query

    if include_hd:
        if mod == 'DT':
            query = {'$and': [{'$or': [{'mods': mod}, {'mods': [mod, 'HD']}, {'mods': 'NC'}, {'mods': ['NC', 'HD']}]},
                              pp_query]}
        else:
            query = {'$and': [{'$or': [{'mods': mod}, {'mods': [mod, 'HD']}]}, pp_query]}
    else:
        query = {'$and': [{'$and': [{'mods': mod}, {'mods': {'$ne': 'HD'}}]}, pp_query]}

    return query


@router.get(
    "", response_description="List all beatmaps"
)
async def list_beatmaps(mod: str = '',
                        pp_range: Tuple[int, int] = Query([400, 900], alias="pp_range[]"),
                        include_hd: bool = True,
                        page: int = 1):
    start_time = time.time()
    limit = 10
    skip_this = (page - 1) * limit

    query = create_query_from_mod(mod, pp_range, include_hd)
    aggregation = []
    if query is not None:
        aggregation.extend([{'$match': query}])

    aggregation.extend([{'$group': {'_id': "$beatmap.id", 'play_count': {'$sum': 1}, 'avg_pp': {'$avg': '$pp'},
                                    'beatmapset_id': {'$first': "$beatmapset.id"}, 'mods': {'$addToSet': '$mods'},
                                    'beatmap_id': {'$first': "$beatmap.id"},
                                    'cover_url': {'$first': '$beatmapset.covers.cover'},
                                    'artist': {'$first': '$beatmapset.artist'},
                                    'artist_unicode': {'$first': '$beatmapset.artist_unicode'},
                                    'title': {'$first': '$beatmapset.title'},
                                    'title_unicode': {'$first': '$beatmapset.title_unicode'},
                                    'difficulty': {'$first': '$beatmap.version'},
                                    }},
                        {'$sort': {'play_count': -1}},
                        {'$skip': skip_this},
                        {'$limit': limit}
                        ])
    results = []
    async for score in scores_collection.aggregate(aggregation):
        results.append(score)

    print(f'list_beatmaps() took: {time.time() - start_time:.2f}s')
    return {'beatmaps': results}
