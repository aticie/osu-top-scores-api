import datetime
import logging
import os
import time

import pymongo
import requests
import schedule
from pymongo.collection import Collection

logger = logging.getLogger('user_update')
logger.setLevel(os.getenv('LOG_LEVEL').upper())
loggers_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(process)d | %(name)s | %(funcName)s | %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S')

ch = logging.StreamHandler()
ch.setFormatter(loggers_formatter)
logger.addHandler(ch)
logger.propagate = False


class OsuApi:
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

        self._base_url = 'https://osu.ppy.sh/api/v2/'
        self._last_request_time = datetime.datetime.now() - datetime.timedelta(hours=1000)
        self._cooldown = datetime.timedelta(seconds=1)

        self._auth_header = self._authorize()

    def _authorize(self) -> dict:
        data = {'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'client_credentials',
                'scope': 'public'}

        with requests.post('https://osu.ppy.sh/oauth/token', json=data) as r:
            response = r.json()

        access_token = response['access_token']

        return {'Authorization': f'Bearer {access_token}'}

    def get_top_std_players(self, page=1):
        params = {'page': page}
        response = self._get_endpoint('rankings/osu/performance', params)
        return response['ranking']

    def get_top_scores_of_player(self, user_id):
        params = {'mode': 'osu',
                  'limit': 50}
        top_scores = []
        top_scores.extend(self._get_endpoint(f'users/{user_id}/scores/best', params))
        params = {'mode': 'osu',
                  'limit': 50,
                  'offset': 50}
        top_scores.extend(self._get_endpoint(f'users/{user_id}/scores/best', params))
        return top_scores

    def _get_endpoint(self, endpoint, params=None):
        time_now = datetime.datetime.now()
        if time_now < self._last_request_time + self._cooldown:
            wait_for = (self._last_request_time + self._cooldown - time_now).total_seconds()
            time.sleep(wait_for)

        with requests.get(self._base_url + endpoint, params=params, headers=self._auth_header) as r:
            response = r.json()

        self._last_request_time = time_now
        return response


def insert_scores_routine(osu_api: OsuApi, scores_collection: Collection):
    logger.info(f'Started insert_scores_routine()!')
    for page_num in range(1, 21):
        top_players = osu_api.get_top_std_players(page=page_num)
        logger.info(f'Looking at page {page_num} of performance rankings.')

        for player_details in top_players:
            player_user_id = player_details['user']['id']
            player_scores = osu_api.get_top_scores_of_player(player_user_id)

            db_scores = []
            for score in player_scores:
                score['_id'] = score['id']
                if scores_collection.find_one({'_id': score['id']}):
                    continue
                db_scores.append(score)
            if len(db_scores) != 0:
                logger.info(f'Inserting scores for {player_details["user"]["username"]}')
                scores_collection.insert_many(db_scores)
            else:
                logger.info(f'Skipping scores of {player_details["user"]["username"]}...')


def initialize_db():
    client = pymongo.mongo_client.MongoClient(os.environ["MONGODB_URL"], username='root', password='verysecret')
    scores_collection: Collection = client.database.scores
    scores_collection.create_index([("pp", pymongo.DESCENDING)])
    scores_collection.create_index([("score", pymongo.DESCENDING)])
    scores_collection.create_index([("beatmap.$**", 1)])
    scores_collection.create_index([("beatmapset.$**", 1)])
    scores_collection.create_index([("user.$**", 1)])

    return scores_collection


if __name__ == '__main__':

    api = OsuApi(client_id=os.getenv("OSU_CLIENT_ID"), client_secret=os.getenv("OSU_CLIENT_SECRET"))
    collection = initialize_db()

    insert_scores_routine(api, collection)
    schedule.every().day.at("12:00").do(insert_scores_routine, api, collection)
    while True:
        schedule.run_pending()
        logger.info(f'Waiting...')
        time.sleep(600)
