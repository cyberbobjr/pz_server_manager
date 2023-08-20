import json
import os

import requests


class Steam(object):
    baseUrl = "https://api.steampowered.com/"
    cache_folder = "mod_cache"

    def __init__(self, key: str, cache_folder):
        self.key = key
        self.cache_folder = cache_folder
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder, exist_ok=True)

    def get_mod_info(self, workshop_id: str):
        cache_filename = os.path.join(self.cache_folder, f"{hash(workshop_id)}.txt")
        if os.path.exists(cache_filename):
            with open(cache_filename, "r") as cache_file:
                cached_data = json.load(cache_file)
            return cached_data

        url = "IPublishedFileService/GetDetails/v1/"
        query_params = {
            "key": self.key,
            "appid": app_config["steam"]["appid"],
            "publishedfileids[0]": workshop_id
        }

        response = requests.get(f"{self.baseUrl}{url}", params=query_params)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'publishedfiledetails' in data['response'] and len(
                    data['response']['publishedfiledetails']) > 0:
                content = data['response']['publishedfiledetails'][0]
                with open(cache_filename, "w") as cache_file:
                    json.dump(content, cache_file, indent=4)
                return content
            return None
        else:
            print("La requête a échoué avec le code:", response.status_code)

    def search_mod(self, cursor=None, text=None, tags=None):
        if tags is None:
            tags = []
        url = "IPublishedFileService/QueryFiles/v1/"
        if cursor is None:
            cursor = "*"
        from main import app_config
        query_params = {
            "key": self.key,
            "appid": app_config["steam"]["appid"],
            "cursor": cursor,
            "match_all_tags": 1,
            "return_short_description": 1,
            "return_children": 1,
            "return_tags": 1,
            "return_metadata": 1,
            "query_type": 21,  # 9 si tri par nombre de souscription, 21 = dernière mise à jour
            "numperpage": 100
        }
        if text is not None:
            query_params["search_text"] = text

        for idx, tag in enumerate(tags):
            query_params[f"requiredtags[{idx}]"] = tag
        response = requests.get(f"{self.baseUrl}{url}", params=query_params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("La requête a échoué avec le code:", response.status_code)
