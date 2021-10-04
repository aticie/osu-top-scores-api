import datetime
import os
import time

import pymongo
import requests
from pymongo.collection import Collection


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


if __name__ == '__main__':
    client = pymongo.mongo_client.MongoClient(os.environ["MONGODB_URL"], username='root', password='verysecret')
    scores_collection: Collection = client.database.scores

    osu_api = OsuApi(client_id=os.getenv("OSU_CLIENT_ID"), client_secret=os.getenv("OSU_CLIENT_SECRET"))
    for page_num in range(1, 11):
        top_players = osu_api.get_top_std_players(page=page_num)
        print(f'Looking at page {page_num} of performance rankings.')

        for player_details in top_players:
            player_user_id = player_details['user']['id']
            player_scores = osu_api.get_top_scores_of_player(player_user_id)

            db_scores = []
            for score in player_scores:
                score['_id'] = score['id']
                score['beatmap_id'] = score['beatmap']['id']
                score['beatmapset_id'] = score['beatmapset']['id']
                del score['statistics']
                del score['id']
                del score['beatmap']
                del score['beatmapset']
                del score['weight']
                del score['user']
                if scores_collection.find_one(score):
                    continue
                db_scores.append(score)
            if len(db_scores) != 0:
                print(f'Inserting scores for {player_details["user"]["username"]}')
                scores_collection.insert_many(db_scores)
            else:
                print(f'Skipping scores of {player_details["user"]["username"]}...')