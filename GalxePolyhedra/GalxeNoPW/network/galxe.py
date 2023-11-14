import logger
import string
from datetime import datetime
import warnings

from eth_account.messages import encode_defunct
from anticaptchaofficial.geetestproxyless import *
from web3.auto import w3

from network.twitter import Twitter
from network.discord import Discord
from network.network_helper import NetworkHelper
from pw_model import *

warnings.filterwarnings("ignore", category=DeprecationWarning)


def reformat_timestamp(timestamp=time.time()) -> str:
    dt = datetime.fromtimestamp(int(timestamp))
    formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return formatted_dt


class Galxe(NetworkHelper):

    def __init__(self, index, proxy, address, private, auth_token, csrf, discord_token, cap_key, acc_id):
        self.index = index
        self.private = private
        self.acc_id = acc_id
        self.cap_key = cap_key
        self.discord_token = discord_token

        self.address = address.lower()
        self.tw_auth_token = auth_token
        self.tw_csrf = csrf
        proxy = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        self.proxy = {'http': proxy, 'https': proxy}

        self.session = NetworkHelper._make_scraper()
        self.session.proxies = self.proxy
        self.session.user_agent = NetworkHelper.random_user_agent()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.nonce = self.get_nonce()

        self.twitter = Twitter(
            index=self.index,
            auth_token=self.tw_auth_token,
            csrf=self.tw_csrf,
            proxy=self.proxy
        )

        self.discord = Discord(
            token=self.discord_token,
            proxy=self.proxy,
            cap_key=self.cap_key
        )

        self.token = None
        self.code = None

    def claim(self, campaign_name, campaign_id):
        self.authorize()
        self.session.headers.update({'authorization': self.token})
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

    def authorize(self):
        try:
            message = "galxe.com wants you to sign in with your Ethereum account:\n" \
                      f"{self.address}\n\n" \
                      "Sign in with Ethereum to the app.\n\n" \
                      "URI: https://galxe.com\n" \
                      "Version: 1\n" \
                      "Chain ID: 1\n" \
                      f"Nonce: {self.nonce}\n" \
                      f"Issued At: {reformat_timestamp()}\n" \
                      f"Expiration Time: {reformat_timestamp(int(time.time()) + 24 * 60 * 60)}\n" \
                      f"Not Before: {reformat_timestamp(int(time.time()) + 24 * 60 * 60)}"

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
                self.token = response.json()['data']['signin']
        except:
            # traceback.print_exc()
            logger.error(f'{self.index}: Galxe authorization failed')

    def get_acc_info(self):

        payload = {"operationName": "BasicUserInfo",
                   "variables":
                       {"address": self.address,
                        "listSpaceInput":
                            {"first": 30}},
                   "query": "query BasicUserInfo($address: String!, $listSpaceInput: ListSpaceInput!) "
                            "{\n  addressInfo(address: $address) {\n    id\n    username\n    address\n    "
                            "hasEmail\n    avatar\n    solanaAddress\n    aptosAddress\n    hasEvmAddress\n    "
                            "hasSolanaAddress\n    hasAptosAddress\n    hasTwitter\n    hasGithub\n    hasDiscord\n    "
                            "email\n    twitterUserID\n    twitterUserName\n    githubUserID\n    githubUserName\n    "
                            "passport {\n      status\n      pendingRedactAt\n      id\n      __typename\n    }\n    "
                            "isVerifiedTwitterOauth2\n    isVerifiedDiscordOauth2\n    displayNamePref\n    "
                            "discordUserID\n    discordUserName\n    subscriptions\n    isWhitelisted\n    "
                            "isInvited\n    isAdmin\n    passportPendingRedactAt\n    spaces(input: $listSpaceInput) "
                            "{\n      list {\n        ...SpaceBasicFrag\n        __typename\n      }\n      "
                            "__typename\n    }\n    __typename\n  }\n}\n\nfragment SpaceBasicFrag on Space "
                            "{\n  id\n  name\n  info\n  thumbnail\n  alias\n  links\n  isVerified\n  status\n  "
                            "followersCount\n  __typename\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            return response.json()

    def connect_discord(self):
        self.session.headers.update({'authorization': self.discord_token})
        with self.session.get(f'https://discord.com/oauth2/authorize?client_id=947863296789323776&redirect_uri=https://galxe.com&response_type=code&scope=identify%20guilds%20guilds.members.read&prompt=consent&state=Discord_Auth;{self.address}', timeout=15) as response:
            with self.session.get(f'https://discord.com/api/v9/oauth2/authorize?client_id=947863296789323776&response_type=code&redirect_uri=https%3A%2F%2Fgalxe.com&scope=identify%20guilds%20guilds.members.read&state=Discord_Auth%3B{self.address}', timeout=15) as response:
                pass

            discord_headers = {
                'authority': 'discord.com',
                'authorization': self.discord_token,
                'content-type': 'application/json',
                'referer': f'https://discord.com/oauth2/authorize?client_id=947863296789323776&redirect_uri=https%3A%2F%2Fgalxe.com&response_type=code&scope=identify%20guilds%20guilds.members.read&state=Discord_Auth%3B{self.address}',
                'x-super-properties': 'eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJydS1SVSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDkuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwOS4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE3NDA1MSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
            }

            payload = {"permissions": "0", "authorize": True}

            with self.session.post(f'https://discord.com/api/v9/oauth2/authorize?client_id=947863296789323776&response_type=code&redirect_uri=https%3A%2F%2Fgalxe.com&scope=identify%20guilds%20guilds.members.read&state=Discord_Auth%3B{self.address}', json=payload, timeout=15, headers=discord_headers) as response:
                url = response.json()['location']

                self.code = url.split('code=')[-1].split('&')[0]

                with self.session.get(url, timeout=15) as response:
                    pass

        self.authorize()
        self.session.headers.update({'authorization': self.token})

        payload = {"operationName": "VerifyDiscord",
                   "variables":
                       {"input":
                            {"address": self.address,
                             "parameter": "",
                             "token": self.code}},
                   "query": "mutation VerifyDiscord($input: VerifyDiscordAccountInput!) "
                            "{\n  verifyDiscordAccount(input: $input) "
                            "{\n    address\n    discordUserID\n    discordUserName\n    __typename\n  }\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print('ConnectDiscord: ', response.json())
            print('--------------------------------------')

    def delete_twitter(self):
        try:
            self.authorize()

            self.session.headers.update({'authorization': self.token})

            payload = {"operationName": "DeleteSocialAccount",
                       "variables":
                           {"input": {"address": self.address,
                                      "type": "TWITTER"}},
                       "query": "mutation DeleteSocialAccount($input: DeleteSocialAccountInput!) {\n  deleteSocialAccount(input: $input) {\n    code\n    message\n    __typename\n  }\n}\n"}

            with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
                print(response.text)
                # try:
                #     if response.json()['errors'][0]['message'] == 'No auth input':
                #         logger.error(f'{self.index}: Twitter connection failed')
                #         return False
                # except:
                #     return True
        except:
            pass

    def verify(self, campaign_id, credential_id):
        authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

        headers = {
            # 'Content-Type': 'application/json',
            # 'Authorization': f'Bearer {authorization_token}',
            # 'x-csrf-token': self.tw_csrf,
            # 'cookie': f'auth_token={self.tw_auth_token}; ct0={self.tw_csrf}'
            'auth_token': self.tw_auth_token,
            'ct0': self.tw_csrf
        }

        self.session.headers.update(headers)

        self.authorize()
        self.session.headers.update({'authorization': self.token})

        # payload = {
        #     "operationName": "TwitterOauth2Status",
        #     "query": "query TwitterOauth2Status {\n  twitterOauth2Status {\n    oauthRateLimited\n    __typename\n  }\n}\n",
        #     "variables": {}
        # }
        #
        # with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
        payload = {"operationName": "VerifyCredentialCondition",
                   "query": "mutation VerifyCredentialCondition($input: VerifyCredentialGroupConditionInput!) {\n  verifyCondition(input: $input)\n}\n",
                   "variables":
                       {"input":
                            {"address": self.address,
                             "campaignId": campaign_id,
                             "conditionIndex": 0,
                             "credentialGroupId": credential_id}},
                   }
        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            print(response.text)

    def connect_twitter(self):
        try:
            self.authorize()

            self.session.headers.update({'authorization': self.token})

            message = f'Verifying my Twitter account for my #GalxeID gid:{self.nonce} @Galxe \n\n galxe.com/galxeid '

            id_ = self.twitter.tweet(message)

            payload = {"operationName": "VerifyTwitterAccount",
                       "variables":
                           {"input":
                                {"address": self.address,
                                 "tweetURL": f"https://twitter.com/screen_name/status/{id_}"}},
                       "query": "mutation VerifyTwitterAccount($input: VerifyTwitterAccountInput!) "
                                "{\n  verifyTwitterAccount(input: $input) {\n    address\n    twitterUserID\n    "
                                "twitterUserName\n    __typename\n  }\n}\n"}

            with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
                try:
                    if response.json()['errors'][0]['message'] == 'No auth input':
                        logger.error(f'{self.index}: Twitter connection failed')
                        return False
                except:
                    return True
        except:
            logger.error(f'{self.index}: Twitter connection failed')
            return False

    def get_nonce(self):
        payload = {"operationName": "RecentParticipation",
                   "variables":
                       {"address": self.address,
                        "participationInput":
                            {"first": 30,
                             "onlyGasless": False,
                             "onlyVerified": False}},
                   "query": "query RecentParticipation($address: String!, $participationInput: ListParticipationInput!)"
                            " {\n  addressInfo(address: $address) {\n    id\n    "
                            "recentParticipation(input: $participationInput) {\n      list {\n        id\n        "
                            "chain\n        tx\n        campaign {\n          id\n          name\n          "
                            "dao {\n            id\n            alias\n            __typename\n          }\n          "
                            "__typename\n        }\n        status\n        __typename\n      }\n      "
                            "__typename\n    }\n    __typename\n  }\n}\n"}

        with self.session.post('https://graphigo.prd.galaxy.eco/query', json=payload, timeout=10) as response:
            return response.json()['data']['addressInfo']['id']
