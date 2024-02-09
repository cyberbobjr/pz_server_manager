import json
import os
import time

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

    def get_mod_info(self, workshop_id: str, force=False):
        cache_filename = os.path.join(self.cache_folder, f"{workshop_id}.json")
        if os.path.exists(cache_filename) and force is False:
            with open(cache_filename, "r") as cache_file:
                cached_data = json.load(cache_file)
            return cached_data

        url = "IPublishedFileService/GetDetails/v1/"
        query_params = {
            "key": self.key,
            "appid": self.app_id,
            "publishedfileids[0]": workshop_id,
            "includevotes": 1
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
            print("The request has been failed with the code:", response.status_code)

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
            "return_short_description": 1,
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
            data = response.json()
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
