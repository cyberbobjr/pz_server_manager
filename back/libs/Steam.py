import json
import os
from datetime import datetime, timedelta

import requests


class Steam(object):
    baseUrl = "https://api.steampowered.com/"
    cache_folder = "mod_cache"

    def __init__(self, key: str, cache_folder, app_id):
        self.key = key
        self.app_id = app_id
        self.cache_folder = cache_folder
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder, exist_ok=True)

    def _is_cache_valid(self, cache_filename):
        """Vérifie si le cache est valide (moins de 3 jours)."""
        cache_time = datetime.fromtimestamp(os.path.getmtime(cache_filename))
        return datetime.now() - cache_time < timedelta(days=3)

    def _load_from_cache(self, workshop_id):
        """Charge les données du workshop_id depuis le cache si elles existent et sont valides."""
        cache_filename = os.path.join(self.cache_folder, f"{workshop_id}.json")
        if os.path.exists(cache_filename) and self._is_cache_valid(cache_filename):
            with open(cache_filename, "r") as cache_file:
                return json.load(cache_file)
        return None

    def _save_to_cache(self, workshop_id, data):
        """Sauvegarde les données du workshop_id dans le cache."""
        cache_filename = os.path.join(self.cache_folder, f"{workshop_id}.json")
        with open(cache_filename, "w") as cache_file:
            json.dump(data, cache_file, indent=4)

    def _fetch_from_steam(self, workshop_ids):
        """Fait la requête à Steam pour obtenir les infos des workshop_ids."""
        query_params = {"key": self.key, "appid": self.app_id, "includevotes": 1}
        for i, workshop_id in enumerate(workshop_ids):
            query_params[f"publishedfileids[{i}]"] = workshop_id

        response = requests.get(f"{self.baseUrl}IPublishedFileService/GetDetails/v1/", params=query_params)
        if response.status_code == 200:
            return response.json().get('response', {}).get('publishedfiledetails', [])
        else:
            print("The request has been failed with the code:", response.status_code)
            return []

    def get_mod_info(self, workshop_ids: list, force=False):
        cached_data = {}
        missing_ids = []

        for workshop_id in workshop_ids:
            data = self._load_from_cache(workshop_id) if not force else None
            if data:
                cached_data[workshop_id] = data
            else:
                missing_ids.append(workshop_id)

        if missing_ids:
            fetched_data = self._fetch_from_steam(missing_ids)
            for detail in fetched_data:
                workshop_id = detail.get('publishedfileid')
                if workshop_id:
                    self._save_to_cache(workshop_id, detail)
                    cached_data[workshop_id] = detail

        return cached_data

    def get_latest_mods(self):
        return self.search_mod("*", None, None)

    def search_mod(self, cursor=None, text=None, tags=None):
        if tags is None:
            tags = []
        url = "IPublishedFileService/QueryFiles/v1/"
        if cursor is None:
            cursor = "*"
        query_params = {
            "key": self.key,
            "appid": self.app_id,
            "cursor": cursor,
            "match_all_tags": 1,
            "return_children": 1,
            "return_tags": 1,
            "return_metadata": 1,
            "query_type": 21,  # 9 nb of subscription, 21 = last updated
            "numperpage": 100
        }
        if text is not None:
            query_params["search_text"] = text

        for idx, tag in enumerate(tags):
            query_params[f"requiredtags[{idx}]"] = tag
        response = requests.get(f"{self.baseUrl}{url}", params=query_params)
        if response.status_code == 200:
            data = response.json()['response']
            return data
        else:
            print("The request has been failed with the code:", response.status_code)

    def get_lastupdate_mod(self, workshop_id):
        url = "IPublishedFileService/GetDetails/v1/"
        query_params = {
            "key": self.key,
            "appid": self.app_id,
            "publishedfileids[0]": workshop_id
        }
        response = requests.get(f"{self.baseUrl}{url}", params=query_params)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'publishedfiledetails' in data['response'] and \
                    len(data['response']['publishedfiledetails']) > 0:
                return data['response']['publishedfiledetails'][0]['time_updated']
        else:
            print("The request has been failed with the code:", response.status_code)
        return None
