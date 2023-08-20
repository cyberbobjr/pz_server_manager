export interface Mod {
  workshopId: number;
  name: string;
  path: string;
  file: string;
  id: string;
  steam_data?: SteamInfo
}

export interface SteamInfo {
  'result': number;
  'publishedfileid': number;
  'creator': number;
  'creator_appid': number;
  'consumer_appid': number;
  'consumer_shortcutid': number;
  'filename': string;
  'file_size': number;
  'preview_file_size': number;
  'preview_url': string;
  'url': string;
  'hcontent_file': number;
  'hcontent_preview': number;
  'title': string;
  'file_description': string;
  'time_created': number;
  'time_updated': number;
  'visibility': number;
  'flags': number;
  'workshop_file': boolean;
  'workshop_accepted': boolean;
  'show_subscribe_all': boolean;
  'num_comments_public': number;
  'banned': boolean;
  'ban_reason': string;
  'banner': number;
  'can_be_deleted': boolean;
  'app_name': string;
  'file_type': number;
  'can_subscribe': boolean;
  'subscriptions': number;
  'favorited': number;
  'followers': number;
  'lifetime_subscriptions': number;
  'lifetime_favorited': number;
  'lifetime_followers': number;
  'lifetime_playtime': number;
  'lifetime_playtime_sessions': number;
  'views': number;
  'num_children': number;
  'num_reports': number;
  'tags': { tag: string, display_name: string }[];
  'language': number;
  'maybe_inappropriate_sex': boolean;
  'maybe_inappropriate_violence': boolean;
  'revision_change_number': number;
  'revision': number;
  'ban_text_check_result': number;
  'vote_data': {
    score: number
  }
}

export interface Modpack {
  name: string;
  mod_ids: string[];
}
