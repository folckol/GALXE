import requests

from network.network_helper import NetworkHelper
from loguru import logger


class Twitter(NetworkHelper):

    def __init__(self, index, auth_token, csrf, proxy):
        self.index = index

        self.session = NetworkHelper._make_scraper()
        self.session.proxies = proxy
        self.session.user_agent = NetworkHelper.random_user_agent()

        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

        self.csrf = csrf
        self.auth_token = auth_token
        self.cookie = f'auth_token={self.auth_token}; ct0={self.csrf}'

        liketweet_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {authorization_token}',
            'x-csrf-token': self.csrf,
            'cookie': self.cookie
        }

        self.session.headers.update(liketweet_headers)

    def tweet(self, text):

        payload = {"variables": {
            "tweet_text": text,
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": True,
            "withSuperFollowsUserFields": True,
            "semantic_annotation_ids": []
        }, "features": {
            "tweetypie_unmention_optimization_enabled": True,
            "vibe_api_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "interactive_text_enabled": True,
            "responsive_web_text_conversations_enabled": False,
            "responsive_web_twitter_blue_verified_badge_is_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": False,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": False,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_enhance_cards_enabled": False
        },
            "queryId": "Tz_cZL9zkkY2806vRiQP0Q"
        }

        with self.session.post("https://api.twitter.com/graphql/Tz_cZL9zkkY2806vRiQP0Q/CreateTweet", json=payload, timeout=30) as response:
            if response.ok:
                logger.success(f'{self.index}: tweet successful')
                return response.json()['data']['create_tweet']['tweet_results']['result']['rest_id']
            else:
                logger.error(f'{self.index}: tweet failed')

    def retweet(self, retweet_id, name):
        if retweet_id != 0:
            try:
                payload = {
                    "variables": {
                        "tweet_id": str(retweet_id)
                    },
                    "queryId": "ojPdsZsimiJrUGLR1sjUtA"
                }

                with self.session.post("https://api.twitter.com/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet", json=payload, timeout=30) as response:
                    if response.json()['errors']:
                        logger.error(f'{self.index}: Retweet failed | {response.json()["errors"][0]["message"]}')
                    else:
                        logger.success(f'{self.index}: {name} retweet successful')
            except:
                logger.error(f'{self.index}: Retweet failed')
        else:
            pass

    def follow(self, user_id):
        self.session.headers.update({'Content-Type': 'application/json'})

        with self.session.post(f"https://api.twitter.com/1.1/friendships/create.json?user_id={user_id}&follow=True", timeout=30) as response:
            if response.json()['errors']:
                logger.error(f'{self.index}: follow failed | {response.json()["errors"][0]["message"]}')
            else:
                logger.success(f'{self.index}: follow successful')

