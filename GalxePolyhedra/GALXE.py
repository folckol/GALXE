import base64
import json
import pickle
import random
import re
import shutil
import ssl
import string
import traceback

import capmonster_python
import cloudscraper
import requests
from eth_account.messages import encode_defunct, defunct_hash_message
from web3 import Web3, Account
import warnings
# from anticaptchaofficial.geetestproxyless import *

from web3.auto import w3

from GALXE_PW import *
from logger import logger

warnings.filterwarnings("ignore", category=DeprecationWarning)



def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{2}_{3}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{1}.{2}) Gecko/20100101 Firefox/{1}.{2}',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

class Discord:

    def __init__(self, token, proxy, cap_key):

        self.cap = capmonster_python.HCaptchaTask(cap_key)
        self.token = token
        self.proxy = proxy

        # print(token)
        # print(proxy)
        # print(cap_key)

        self.session = self._make_scraper()
        self.ua = random_user_agent()
        self.session.user_agent = self.ua
        self.session.proxies = self.proxy
        self.super_properties = self.build_xsp(self.ua)


        self.cfruid, self.dcfduid, self.sdcfduid = self.fetch_cookies(self.ua)
        self.fingerprint = self.get_fingerprint()


    def JoinServer(self, invite):

        rer = self.session.post("https://discord.com/api/v9/invites/" + invite, headers={"authorization": self.token})

        # print(rer.text, rer.status_code)
        # print(rer.text)
        # print(rer.status_code)

        if "200" not in str(rer):
            site = "a9b5fb07-92ff-493f-86fe-352a2803b3df"
            tt = self.cap.create_task("https://discord.com/api/v9/invites/" + invite, site)
            # print(f"Created Captcha Task {tt}")
            captcha = self.cap.join_task_result(tt)
            captcha = captcha["gRecaptchaResponse"]
            # print(f"[+] Solved Captcha ")
            # print(rer.text)

            self.session.headers = {'Host': 'discord.com', 'Connection': 'keep-alive',
                               'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                               'X-Super-Properties': self.super_properties,
                               'Accept-Language': 'en-US', 'sec-ch-ua-mobile': '?0',
                               "User-Agent": self.ua,
                               'Content-Type': 'application/json', 'Authorization': 'undefined', 'Accept': '*/*',
                               'Origin': 'https://discord.com', 'Sec-Fetch-Site': 'same-origin',
                               'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                               'Referer': 'https://discord.com/@me', 'X-Debug-Options': 'bugReporterEnabled',
                               'Accept-Encoding': 'gzip, deflate, br',
                               'x-fingerprint': self.fingerprint,
                               'Cookie': f'__dcfduid={self.dcfduid}; __sdcfduid={self.sdcfduid}; __cfruid={self.cfruid}; __cf_bm=DFyh.5fqTsl1JGyPo1ZFMdVTupwgqC18groNZfskp4Y-1672630835-0-Aci0Zz919JihARnJlA6o9q4m5rYoulDy/8BGsdwEUE843qD8gAm4OJsbBD5KKKLTRHhpV0QZybU0MrBBtEx369QIGGjwAEOHg0cLguk2EBkWM0YSTOqE63UXBiP0xqHGmRQ5uJ7hs8TO1Ylj2QlGscA='}
            rej = self.session.post("https://discord.com/api/v9/invites/" + invite, headers={"authorization": self.token}, json={
                "captcha_key": captcha,
                "captcha_rqtoken": str(rer.json()["captcha_rqtoken"])
            })
            # print(rej.text())
            # print(rej.status_code)
            if "200" in str(rej):
                return 'Successfully Join 0', self.super_properties
            if "200" not in str(rej):
                return 'Failed Join'

        else:
            with self.session.post("https://discord.com/api/v9/invites/" + invite, headers={"authorization": self.token}) as response:
                # print(response.text)
                pass
            return 'Successfully Join 1', self.super_properties

    def AcceptTerms(self):

        response = self.session.put('https://discord.com/api/v9/guilds/1060795343983366144/requests/@me', payload={"version":"2023-04-04T06:47:21.620000+00:00","form_fields":[{"automations":None,"description":None,"field_type":"TERMS","label":"Read and agree to the server rules","required":True,"values":["No external links irrelevant to polyhedra or advertisements","No false/misleading information","No spamming","No offensive names or words","No discrimination","Be respectful"],"response":True}]})
        if response.json()["application_status"] == "APPROVED":
            return True
        else:
            return False


    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

    def build_xsp(self, ua):
        # ua = get_useragent()
        _,fv = self.get_version(ua)
        data = json.dumps({
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": ua,
            "browser_version": fv,
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": self.get_buildnumber(),
            "client_event_source": None
        }, separators=(",",":"))
        return base64.b64encode(data.encode()).decode()

    def get_version(self, user_agent):  # Just splits user agent
        chrome_version = user_agent.split("/")[3].split(".")[0]
        full_chrome_version = user_agent.split("/")[3].split(" ")[0]
        return chrome_version, full_chrome_version

    def get_buildnumber(self):  # Todo: make it permanently work
        r = requests.get('https://discord.com/app', headers={'User-Agent': 'Mozilla/5.0'})
        asset = re.findall(r'([a-zA-z0-9]+)\.js', r.text)[-2]
        assetFileRequest = requests.get(f'https://discord.com/assets/{asset}.js',
                                        headers={'User-Agent': 'Mozilla/5.0'}).text
        try:
            build_info_regex = re.compile('buildNumber:"[0-9]+"')
            build_info_strings = build_info_regex.findall(assetFileRequest)[0].replace(' ', '').split(',')
        except:
            # print("[-]: Failed to get build number")
            pass
        dbm = build_info_strings[0].split(':')[-1]
        return int(dbm.replace('"', ""))

    def fetch_cookies(self, ua):
        try:
            url = 'https://discord.com/'
            headers = {'user-agent': ua}
            response = self.session.get(url, headers=headers, proxies=self.proxy)
            cookies = response.cookies.get_dict()
            cfruid = cookies.get("__cfruid")
            dcfduid = cookies.get("__dcfduid")
            sdcfduid = cookies.get("__sdcfduid")
            return cfruid, dcfduid, sdcfduid
        except:
            # print(response.text)
            return 1

    def get_fingerprint(self):
        try:
            fingerprint = self.session.get('https://discord.com/api/v9/experiments', proxies=self.proxy).json()['fingerprint']
            # print(f"[=]: Fetched Fingerprint ({fingerprint[:15]}...)")
            return fingerprint
        except Exception as err:
            # print(err)
            return 1

class Twitter:

    def __init__(self, auth_token, csrf, proxy):

        self.session = self._make_scraper()
        self.session.proxies = proxy
        self.session.user_agent = random_user_agent()

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

        # print('Аккаунт готов')


    # Основные функции твиттер аккаунта

    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

    def MyNickname(self):

        with self.session.get("https://api.twitter.com/1.1/account/settings.json", timeout=10) as response:
            return response.json()['screen_name']

    def Tweet(self, text="Just applied for the @MuhammadAliNFT allowlist!\n\nOn-chain generative art by @Ze_blocks "):

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

        with self.session.post("https://api.twitter.com/graphql/Tz_cZL9zkkY2806vRiQP0Q/CreateTweet", json=payload,
                               timeout=30) as response:
            if response.ok:
                print(response.json())
                return response.json()['data']['create_tweet']['tweet_results']['result']['rest_id']

    def Retweet(self, id):
        payload = {
            "variables": {
                "tweet_id": str(id)
            },
            "queryId": "ojPdsZsimiJrUGLR1sjUtA"
        }

        with self.session.post("https://api.twitter.com/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet", json=payload, timeout=30) as response:
            if response.ok:
                # print(response.text)
                pass

    def Follow(self, user_id):
        # Не работает
        self.session.headers.update({'Content-Type': 'application/json'})

        with self.session.post(f"https://api.twitter.com/1.1/friendships/create.json?user_id={user_id}&follow=True", timeout=30) as response:
            # print(response.text)

            if 'suspended' in response.text:
                # print(f'Аккаунт {self.name} забанен')
                return 'ban'
            else:
                return 1


class AccountG:

    def __init__(self, proxy, address,private, auth_token, csrf, discord_token, capKey):

        proxy = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        # self.cap_key = cap_key

        self.private = private
        self.capKey = capKey

        self.discord_token = discord_token

        self.address = address.lower()
        self.tw_auth_token = auth_token
        self.tw_csrf = csrf
        self.proxy = {'http': proxy, 'https': proxy}

        self.session = self._make_scraper()
        self.session.proxies = self.proxy
        self.session.user_agent = random_user_agent()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.nonce = self.GetNonce()
        # self.TwitterModel = Twitter(auth_token=self.tw_auth_token,
        #                             csrf=self.tw_csrf,
        #                             proxy=self.proxy)
        # self.DiscordModel = Discord(token=self.discord_token,
        #                             proxy=self.proxy,
        #                             cap_key=self.capKey)



    def reformat_timestamp(self, timestamp=time.time()) -> str:
        # Преобразуем строку timestamp в объект datetime
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        # Преобразуем дату и время в нужный формат
        formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return formatted_dt

    def GetNonce(self):

        payload = {"operationName":"RecentParticipation",
                   "variables":
                       {"address":self.address,
                        "participationInput":
                            {"first":30,
                             "onlyGasless":False,
                             "onlyVerified":False}},
                   "query":"query RecentParticipation($address: String!, $participationInput: ListParticipationInput!) {\n  addressInfo(address: $address) {\n    id\n    recentParticipation(input: $participationInput) {\n      list {\n        id\n        chain\n        tx\n        campaign {\n          id\n          name\n          dao {\n            id\n            alias\n            __typename\n          }\n          __typename\n        }\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print(response.text)
            return response.json()['data']['addressInfo']['id']

    def Authorize(self):

        message = "galxe.com wants you to sign in with your Ethereum account:\n" \
                  f"{self.address}\n\n" \
                  "Sign in with Ethereum to the app.\n\n" \
                  "URI: https://galxe.com\n" \
                  "Version: 1\n" \
                  "Chain ID: 1\n" \
                  f"Nonce: {self.nonce}\n" \
                  f"Issued At: {self.reformat_timestamp()}\n" \
                  f"Expiration Time: {self.reformat_timestamp(int(time.time()) + 24 * 60 * 60)}\n" \
                  f"Not Before: {self.reformat_timestamp(int(time.time()) + 24 * 60 * 60)}"

        message_hash = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(message_hash, private_key=self.private)
        signature = signed_message["signature"].hex()

        payload = {"operationName": "SignIn",
                   "variables":
                       {"input":
                            {"address": self.address,
                             "message": message,
                             "signature": signature}},
                   "query": "mutation SignIn($input: Auth) {\n  signin(input: $input)\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print(response.json())
            self.token = response.json()['data']['signin']

    def MintName(self):


        while True:

            username = self.generate_username()

            payload = {"operationName":"IsUsernameExisting",
                       "variables":
                           {"username":username},
                       "query":"query IsUsernameExisting($username: String!) {\n  usernameExist(username: $username)\n}\n"}

            with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
                print(response.json())
                if response.json()['data']['usernameExist'] == False:
                    break

                time.sleep(2)

        payload = {"operationName": "UpdateProfile",
                   "variables":
                       {"input":
                            {"address": self.address,
                             "username": username,
                             "avatar": f"https://source.boringavatars.com/marble/120/{self.address}",
                             "displayNamePref": "USERNAME"}},
                   "query": "mutation UpdateProfile($input: UpdateProfileInput!) {\n  updateProfile(input: $input) {\n    code\n    message\n    __typename\n  }\n}\n"}

        SignIn = True
        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            try:
                if response.json()['errors'][0]['message'] == 'No auth input':
                    SignIn = False
                else:
                    pass
            except:
                pass

        if SignIn == False:

            message = "galxe.com wants you to sign in with your Ethereum account:\n"\
                       f"{self.address}\n\n"\
                       "Sign in with Ethereum to the app.\n\n"\
                       "URI: https://galxe.com\n"\
                       "Version: 1\n"\
                       "Chain ID: 1\n"\
                       f"Nonce: {self.nonce}\n"\
                       f"Issued At: {self.reformat_timestamp()}\n"\
                       f"Expiration Time: {self.reformat_timestamp(int(time.time())+24*60*60)}\n"\
                       f"Not Before: {self.reformat_timestamp(int(time.time())+24*60*60)}"

            message_hash = encode_defunct(text=message)
            signed_message = w3.eth.account.sign_message(message_hash, private_key=self.private)
            signature = signed_message["signature"].hex()

            payload = {"operationName":"SignIn",
                       "variables":
                           {"input":
                                {"address":self.address,
                                 "message":message,
                                 "signature": signature}},
                       "query":"mutation SignIn($input: Auth) {\n  signin(input: $input)\n}\n"}

            with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
                print(response.json())
                self.token = response.json()['data']['signin']

        self.session.headers.update({'authorization': self.token})

        payload = {"operationName": "UpdateProfile",
                   "variables":
                       {"input":
                            {"address": self.address,
                             "username": username,
                             "avatar": f"https://source.boringavatars.com/marble/120/{self.address}",
                             "displayNamePref": "USERNAME"}},
                   "query": "mutation UpdateProfile($input: UpdateProfileInput!) {\n  updateProfile(input: $input) {\n    code\n    message\n    __typename\n  }\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print(response.json())
            if response.json() == {"data":{"updateProfile":None}}:
                return 'Success'



    def AboutMe(self):

        payload = {"operationName":"BasicUserInfo",
                   "variables":
                       {"address":self.address,
                        "listSpaceInput":
                            {"first":30}},
                   "query":"query BasicUserInfo($address: String!, $listSpaceInput: ListSpaceInput!) {\n  addressInfo(address: $address) {\n    id\n    username\n    address\n    hasEmail\n    avatar\n    solanaAddress\n    aptosAddress\n    hasEvmAddress\n    hasSolanaAddress\n    hasAptosAddress\n    hasTwitter\n    hasGithub\n    hasDiscord\n    email\n    twitterUserID\n    twitterUserName\n    githubUserID\n    githubUserName\n    passport {\n      status\n      pendingRedactAt\n      id\n      __typename\n    }\n    isVerifiedTwitterOauth2\n    isVerifiedDiscordOauth2\n    displayNamePref\n    discordUserID\n    discordUserName\n    subscriptions\n    isWhitelisted\n    isInvited\n    isAdmin\n    passportPendingRedactAt\n    spaces(input: $listSpaceInput) {\n      list {\n        ...SpaceBasicFrag\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SpaceBasicFrag on Space {\n  id\n  name\n  info\n  thumbnail\n  alias\n  links\n  isVerified\n  status\n  followersCount\n  __typename\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print(response.json())
            return response.json()

    def ConnectDiscord(self):

        # payload = {"redirectUrl":"https://trove.treasure.lol/treasuretag?edit=true"}
        self.session.headers.update({'authorization': self.discord_token})
        with self.session.get(f'https://discord.com/oauth2/authorize?client_id=947863296789323776&redirect_uri=https://galxe.com&response_type=code&scope=identify%20guilds%20guilds.members.read&prompt=consent&state=Discord_Auth;{self.address}', timeout=15) as response:

            with self.session.get(f'https://discord.com/api/v9/oauth2/authorize?client_id=947863296789323776&response_type=code&redirect_uri=https%3A%2F%2Fgalxe.com&scope=identify%20guilds%20guilds.members.read&state=Discord_Auth%3B{self.address}', timeout=15) as response:
                pass

            # url = response.json()['loginUrl']
            #
            # state = url.split('state=')[-1].split('&')[0]
            # client_id = url.split('client_id=')[-1].split('&')[0]

            discord_headers = {
                'authority': 'discord.com',
                'authorization': self.discord_token,
                'content-type': 'application/json',
                'referer': f'https://discord.com/oauth2/authorize?client_id=947863296789323776&redirect_uri=https%3A%2F%2Fgalxe.com&response_type=code&scope=identify%20guilds%20guilds.members.read&state=Discord_Auth%3B{self.address}',
                'x-super-properties': 'eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJydS1SVSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDkuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwOS4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE3NDA1MSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
            }

            payload = {"permissions":"0","authorize":True}

            with self.session.post(f'https://discord.com/api/v9/oauth2/authorize?client_id=947863296789323776&response_type=code&redirect_uri=https%3A%2F%2Fgalxe.com&scope=identify%20guilds%20guilds.members.read&state=Discord_Auth%3B{self.address}', json=payload, timeout=15, headers=discord_headers) as response:
                url = response.json()['location']

                self.code = url.split('code=')[-1].split('&')[0]

                with self.session.get(url, timeout=15) as response:
                    # print(f'{self.id} - Discord connected')
                    pass


        self.Authorize()
        self.session.headers.update({'authorization': self.token})

        payload = {"operationName":"VerifyDiscord",
                   "variables":
                       {"input":
                            {"address":self.address,
                             "parameter":"",
                             "token":self.code}},
                   "query":"mutation VerifyDiscord($input: VerifyDiscordAccountInput!) {\n  verifyDiscordAccount(input: $input) {\n    address\n    discordUserID\n    discordUserName\n    __typename\n  }\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print(response.json())


    def ConnectTwitter(self):

        self.Authorize()

        self.session.headers.update({'authorization': self.token})

        message = f'Verifying my Twitter account for my #GalxeID gid:{self.nonce} @Galxe \n\n galxe.com/galxeid '

        id_ = self.TwitterModel.Tweet(message)

        payload = {"operationName":"VerifyTwitterAccount",
                   "variables":
                       {"input":
                            {"address":self.address,
                             "tweetURL":f"https://twitter.com/screen_name/status/{id_}"}},
                   "query":"mutation VerifyTwitterAccount($input: VerifyTwitterAccountInput!) {\n  verifyTwitterAccount(input: $input) {\n    address\n    twitterUserID\n    twitterUserName\n    __typename\n  }\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:

            print(response.json())
            try:
                if response.json()['errors'][0]['message'] == 'No auth input':
                    print('Ошибка с привязкой твиттера')
            except:
                pass

    def CaptchaSolver(self, challenge, userAgent):
        def Capmonster():
            cap = capmonster_python.GeeTestTask('8e4fc64e0919bbe0f0cfd62cd745ecbd')

            payload = {
                "clientKey":"8e4fc64e0919bbe0f0cfd62cd745ecbd",
                "task":
                    {
                        "type":"GeeTestTaskProxyless",
                        "websiteURL":"https://galxe.com/polyhedra/campaign/GCZqpUS5FL",
                        "gt":"244bcb8b9846215df5af4c624a750db4",
                        "challenge": challenge,
                        "version": 4,
                        "initParameters": {
                            "client_type": "web",
                            "lang":"ru-ru"

                        }
                    },
                "userAgent": userAgent
            }

            taskId = requests.post('https://api.capmonster.cloud/createTask', json=payload).json()
            print(taskId)


            # a = cap.create_task('https://galxe.com/polyhedra/campaign/GCZqpUS5FL', '244bcb8b9846215df5af4c624a750db4', callenge, version=4)
            try:
                result = cap.join_task_result(taskId['taskId'])
            except:
                traceback.print_exc()
                result = 'Captcha Error'

            return result

        def rucaptcha():
            payload = {
                "key": "1f543e9ed1c27fcdac48fb26be3ae6e4",
                "method": "geetest_v4",
                "captcha_id": "244bcb8b9846215df5af4c624a750db4",
                "pageurl": "https://galxe.com/polyhedra/campaign/GCZqpUS5FL",
                "json": 1
            }

            dd = requests.post('http://2captcha.com/in.php', json=payload).json()
            # print(dd)

            while True:

                d = requests.get(f'http://2captcha.com/res.php?key=1f543e9ed1c27fcdac48fb26be3ae6e4&action=get&id={dd["request"]}').text

                print(d)
                if 'OK' in d:
                    break
                time.sleep(5)

            return json.loads(d.split('|')[-1])



        # result = Capmonster()
        result = rucaptcha()


        print(result)
        return result

    def solve_captcha(self):
        try:
            payload = {
                "key": self.cap_key,
                "method": "geetest_v4",
                "captcha_id": "244bcb8b9846215df5af4c624a750db4",
                "pageurl": "https://galxe.com/polyhedra/campaign/GCZqpUS5FL",
                "json": 1
            }

            dd = requests.post('http://2captcha.com/in.php', json=payload).json()

            while True:

                d = requests.get(
                    f'http://2captcha.com/res.php?key=1f543e9ed1c27fcdac48fb26be3ae6e4&action=get&id={dd["request"]}').text

                if 'OK' in d:
                    break
                time.sleep(5)

            return json.loads(d.split('|')[-1])
        except:
            logger.error(f'{self.index}: Captcha error')

    def claim(self, campaign_name, campaign_id):
        try:
            cap_data = self.solve_captcha()

            payload = {
                'operationName': 'PrepareParticipate',
                'query': 'mutation PrepareParticipate($input: PrepareParticipateInput!) {\n  prepareParticipate(input: $input) {\n    allow\n    disallowReason\n    signature\n    nonce\n    mintFuncInfo {\n      funcName\n      nftCoreAddress\n      verifyIDs\n      powahs\n      cap\n      __typename\n    }\n    extLinkResp {\n      success\n      data\n      error\n      __typename\n    }\n    metaTxResp {\n      metaSig2\n      autoTaskUrl\n      metaSpaceAddr\n      forwarderAddr\n      metaTxHash\n      reqQueueing\n      __typename\n    }\n    solanaTxResp {\n      mint\n      updateAuthority\n      explorerUrl\n      signedTx\n      verifyID\n      __typename\n    }\n    aptosTxResp {\n      signatureExpiredAt\n      tokenName\n      __typename\n    }\n    tokenRewardCampaignTxResp {\n      signatureExpiredAt\n      verifyID\n      __typename\n    }\n    loyaltyPointsTxResp {\n      TotalClaimedPoints\n      __typename\n    }\n    __typename\n  }\n}\n',
                'variables': {
                    'input': {
                        'address': self.address,
                        'campaignID': campaign_id,
                        'captcha': {
                            'captchaOutput': cap_data['captcha_output'],
                            'genTime': cap_data['gen_time'],
                            'lotNumber': cap_data['lot_number'],
                            'passToken': cap_data['pass_token']
                        },
                        'chain': 'ETHEREUM',
                        'mintCount': 1,
                        'signature': ''
                    }
                }
            }

            with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
                # print(response.json())
                data = response.json()['data']['prepareParticipate']
                if data['allow']:
                    logger.success(f'{self.index}: {campaign_name} | Successfully claimed')
                else:
                    logger.error(f'{self.index}: {campaign_name} | {data["disallowReason"]}')
        except:
            logger.error(f'{self.index}: {campaign_name} | Claim error')


    def generate_username(self):
        # Генерируем случайную длину никнейма от 6 до 10 символов
        length = random.randint(6, 10)
        # Генерируем случайный никнейм из букв и цифр
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return username

    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )



if __name__ == '__main__':

    # Twitter('cc412d61fa83bd89a0a2fbb66d8ce34119d9897d',
    #         '13e00dc21aa88e69288188616e29bed45ffdbdce58672e5b2437082e36b04837fcdf35711a829acb9ff1aae2282b8e418bccbf7ed2962907e6b9f0773820a0780fae5b6ae82624395e4124c2f32d2511',
    #         {'http': 'http://jzoshphm:ui3t2docv6xy@104.239.73.20:6563', 'https': 'http://jzoshphm:ui3t2docv6xy@104.239.73.20:6563'}).Tweet('GM Guys')
    # input()
    #
    #
    #
    # friends = []
    #
    # proxy = ''
    #


    data = {
        # Socials
        # 'follower': ['https://galxe.com/polyhedra/campaign/GCMtWUEW5E', 1611184634418823169],
        # 'discord': 'https://galxe.com/polyhedra/campaign/GCFeWUEck4',
        # 'polyhedra-quote-tweet': 'https://galxe.com/polyhedra/campaign/GCFwmUXopr',
        # 'zkBridge-quote-tweet': 'https://galxe.com/polyhedra/campaign/GCW7sUEAyS',
        # 'polyhedra-retweets': ['https://galxe.com/polyhedra/campaign/GCkmEUN9KB', 1663906700582170626],
        # Main
        'Greenfield Testnet Tutorial NFT Mint': ['https://galxe.com/polyhedra/campaign/GCDKiUNoG1', 1665665972370550785],
        'BNB Chain Luban Upgrade NFT Mint': ['https://galxe.com/polyhedra/campaign/GCHdyUQygV', 1668169901377486850],
        'BNB Chain Luban Upgrade NFT Cross Chain': ['https://galxe.com/polyhedra/campaign/GCbRyUQEER', 0],
        'opBNB NFT Mint': ['https://galxe.com/polyhedra/campaign/GCjrpUSkbq', 1670794025824133124],
        'opBNB NFT Cross Chain': ['https://galxe.com/polyhedra/campaign/GCRxpUShLa', 0],
        'Mainnet Alpha NFT Core Dao Edition Mint': ['https://galxe.com/polyhedra/campaign/GCZqpUS5FL', 1671157876067565568],
        'Mainnet Alpha NFT Core Dao Edition Cross Chain': ['https://galxe.com/polyhedra/campaign/GCgqfUSzBZ', 0],
        'BSC/Polygon zkMessenger With zk Light Client': ['https://galxe.com/polyhedra/campaign/GCDTWUWt4p', 1649217088664530946],
        'zkLightClient NFT Mint': ['https://galxe.com/polyhedra/campaign/GCWQSUNvRa', 1663906700582170626],
        'zkLightClient NFT Cross-Chain': ['https://galxe.com/polyhedra/campaign/GCeoSUNgbg', 0],
        # Pandra
        # 'CodeConqueror': ['https://galxe.com/polyhedra/campaign/GCN55UezHH', 1678639611692695552],
        # 'PixelProwler': ['https://galxe.com/polyhedra/campaign/GCZb5Ueoss', 0],
        # 'MelodyMaven': ['https://galxe.com/polyhedra/campaign/GCZv5Ue14g', 0],
        # 'EcoGuardian': ['https://galxe.com/polyhedra/campaign/GCZ7tU7LYP', 0]
    }
    proxy = ''
    address = ''
    private = ''

    acc = AccountG(proxy=proxy,
                   address=address,
                   private=private,
                   auth_token="",
                   csrf="",
                   discord_token="",
                   capKey=""
                   )


    # acc.MintName()


    acc.Authorize()
    # acc_info = acc.AboutMe()
    #
    # if acc_info['data']['addressInfo']['hasTwitter'] == False:
    #     acc.ConnectTwitter()
    # if acc_info['data']['addressInfo']['hasDiscord'] == False:
    #     acc.ConnectDiscord()
    # if acc_info['data']['addressInfo']['username'] == '':
    #     acc.MintName()

    # acc_info = acc.AboutMe()

    try:
        shutil.rmtree('dataDir1')
    except:
        pass

    # print([PW.campaignName[3:-4]])


    acc.claim(d, data[i][0].split('/')[-1])




        # input()




        # Polyhedra Twitter Retweets
        # acc.TwitterModel.Retweet(1663906700582170626)
        # PW.Polyhedra_Retweets()

        # Polyhedra DiscordMember
        # acc.DiscordModel.JoinServer('WkjUe5tfZP')
        # status = acc.DiscordModel.AcceptTerms()
        # if status == True:
        #     print('Успешно зашел на сервер')
        #     PW.Polyhedra_DiscordMember()
        # else:
        #     print('Зайти на сервер не получилось')
        #
        # # Polyhedra Twitter Follow
        # acc.TwitterModel.Follow(1611184634418823169)
        # PW.Polyhedra_Follow()
        #
        # # Polyhedra Quote Tweet
        # acc.TwitterModel.Follow(1611184634418823169)
        # acc.TwitterModel.Tweet(f'#zkbridge https://twitter.com/PolyhedraZK/status/1658111159139020806 {random.choice(friends)}')
        # PW.Polyhedra_QuoteTweet()
        #
        # # Polyhedra Quote Tweet 2
        # acc.TwitterModel.Tweet(
        #     f'https://twitter.com/PolyhedraZK/status/1655948436406157312 ')
        # PW.Polyhedra_QuoteTweet2()
        #
        # # Polyhedra zkLightClient NFT Cross-Chain
        # acc.TwitterModel.Retweet(1663906700582170626)
        # PW.zkLightClientNFTCrossChain()
        #
        # # Polyhedra zkLightClient NFT Mint
        # # acc.TwitterModel.Retweet(1663906700582170626) Если ретвит уже сделан
        # PW.zkLightClientNFTMint()
        #
        # # Polyhedra Greenfield Testnet Tutorial NFT Mint
        # acc.TwitterModel.Retweet(1665665972370550785)
        # PW.GreenfieldTestnetTutorialNFTMint()
        #
        # # Polyhedra BNB Chain Luban Upgrade NFT Mint
        # acc.TwitterModel.Retweet(1668169901377486850)
        # PW.BNBChainLubanUpgradeNFTMint()
        #
        # # BNB Chain Luban Upgrade NFT Cross Chain
        # # acc.TwitterModel.Retweet(1668169901377486850) Если ретвит уже сделан
        # PW.BNBChainLubanUpgradeNFTCrossChain()
        #
        # # opBNB NFT Mint
        # acc.TwitterModel.Retweet(1670794025824133124)
        # PW.opBNBNFTMint()
        #
        # # opBNB NFT Cross Chain
        # # acc.TwitterModel.Retweet(1670794025824133124) Если ретвит уже сделан
        # PW.opBNBNFTCrossChain()
        #
        # # BSC/Polygon zkMessenger With zk Light Client
        # acc.TwitterModel.Retweet(1649217088664530946)
        # acc.TwitterModel.Follow(1611184634418823169)
        # PW.BSCPolygonzkMessengerWithzkLightClient()
        #
        PW.close()

    except:
        traceback.print_exc()



