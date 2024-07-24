import json
import os
import re
from datetime import datetime
from typing import Set, Dict, List, Callable, Optional


class PZLog:

    @staticmethod
    async def print(msg: str):
        print(msg)

    def __init__(self, directory) -> None:
        self.directory = directory
        self.log_parsers: Dict[str, Callable[[str], Dict[str, str]]] = {
            "PerkLog.txt": self.parse_perk_log,
            "ClientActionLog.txt": self.parse_client_action_log,
            "item.txt": self.parse_item_log,
            "map.txt": self.parse_map_log,
        }

    def parse_perk_log(self, line: str) -> Dict[str, str]:
        log_pattern = re.compile(r'\[(.*?)\] \[(.*?)\]\[(.*?)\]\[(.*?)\]\[(.*?)\]\[(.*?)\]')
        match = log_pattern.match(line)
        if match:
            return {
                "type": "PERK",
                "datetime": match.group(1),
                "player": match.group(3),
                "action": match.group(5),
                "position": match.group(4),
                "action_parameter": match.group(6)
            }
        return {}

    def parse_client_action_log(self, line: str) -> Dict[str, str]:
        log_pattern = re.compile(r'\[(.*?)\] \[(.*?)\]\[(.*?)\]\[(.*?)\]\[(.*?)\]\[(.*?)\]')
        match = log_pattern.match(line)
        if match:
            return {
                "type": "ACTION",
                "datetime": match.group(1),
                "player": match.group(4),
                "action": match.group(3),
                "position": match.group(5),
                "action_parameter": match.group(6)
            }
        return {}

    def parse_item_log(self, line: str) -> Dict[str, str]:
        log_pattern = re.compile(r'\[(.*?)\] (\d+) "(.*?)" (.*?) ([-\d]+) (\d+,\d+,\d+) \[(.*?)\]')
        match = log_pattern.match(line)
        if match:
            return {
                "type": "ITEM",
                "datetime": match.group(1),
                "player": match.group(3),
                "action": match.group(4),
                "position": match.group(6),
                "action_parameter": match.group(7),
                "action_parameter2": match.group(5),
            }
        return {}

    def parse_map_log(self, line: str) -> Dict[str, str]:
        log_pattern = re.compile(r'\[(.*?)\] (\d+) "(.*?)" (.*?) (.*?) \((.*?)\) at (.*?),(.*?),(.*?)\.')
        match = log_pattern.match(line)
        if match:
            return {
                "type": "MAP",
                "datetime": match.group(1),
                "player": match.group(3),
                "action": match.group(4),
                "object": match.group(5),
                "details": match.group(6),
                "position": f"{match.group(7)},{match.group(8)},{match.group(9)}"
            }
        return {}

    def get_log_type(self, file_name: str) -> str:
        for log_type in self.log_parsers.keys():
            if log_type in file_name:
                return log_type
        return None

    def scan_logs(self) -> List[Dict[str, str]]:
        logs = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                log_type = self.get_log_type(file)
                if log_type:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as log_file:
                        parser = self.log_parsers[log_type]
                        for line in log_file:
                            log_entry = parser(line)
                            if log_entry:
                                logs.append(log_entry)
        return logs

    def get_logs_as_json(self) -> str:
        logs = self.scan_logs()
        return json.dumps(logs, indent=4)

    def search_logs(self, player: Optional[str] = None, start_date: Optional[str] = None,
                    end_date: Optional[str] = None, log_type: Optional[str] = None) -> List[Dict[str, str]]:
        logs = self.scan_logs()
        filtered_logs = []

        def parse_iso_datetime(dt_str: str) -> datetime:
            # Remove 'Z' if it's present
            if dt_str.endswith('Z'):
                dt_str = dt_str[:-1]
            parse_start_date = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
            return parse_start_date

        for log in logs:
            log_datetime = datetime.strptime(log["datetime"], '%d-%m-%y %H:%M:%S.%f')
            if player and log["player"] != player:
                continue
            if start_date and log_datetime < parse_iso_datetime(start_date):
                continue
            if end_date and log_datetime > parse_iso_datetime(end_date):
                continue
            if log_type and log["type"] != log_type:
                continue

            filtered_logs.append(log)

        return filtered_logs

    def search_logs_as_json(self, player: Optional[str] = None, start_date: Optional[str] = None,
                            end_date: Optional[str] = None, log_type: Optional[str] = None) -> str:
        filtered_logs = self.search_logs(player, start_date, end_date, log_type)
        return json.dumps(filtered_logs, indent=4)

    def get_all_players(self) -> Set[str]:
        logs = self.scan_logs()
        players = set()

        for log in logs:
            players.add(log["player"])

        return players
