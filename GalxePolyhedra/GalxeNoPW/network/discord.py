import requests
import base64
import json
import re

import capmonster_python

from network.network_helper import NetworkHelper


class Discord(NetworkHelper):

    def __init__(self, token, proxy, cap_key):

        self.cap = capmonster_python.HCaptchaTask(cap_key)
        self.token = token
        self.proxy = proxy

        self.session = self._make_scraper()
        self.ua = self.random_user_agent()
        self.session.user_agent = self.ua
        self.session.proxies = self.proxy
        self.super_properties = self.build_xsp(self.ua)

        self.cfruid, self.dcfduid, self.sdcfduid = self.fetch_cookies(self.ua)
        self.fingerprint = self.get_fingerprint()

    def join_server(self, invite):

        rer = self.session.post("https://discord.com/api/v9/invites/" + invite, headers={"authorization": self.token})

        if "200" not in str(rer):
            site = "a9b5fb07-92ff-493f-86fe-352a2803b3df"
            tt = self.cap.create_task("https://discord.com/api/v9/invites/" + invite, site)
            captcha = self.cap.join_task_result(tt)
            captcha = captcha["gRecaptchaResponse"]

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

            if "200" in str(rej):
                return 'Successfully Join 0', self.super_properties
            if "200" not in str(rej):
                return 'Failed Join'

        else:
            with self.session.post("https://discord.com/api/v9/invites/" + invite, headers={"authorization": self.token}) as response:
                pass
            return 'Successfully Join 1', self.super_properties

    def acept_terms(self):
        response = self.session.put('https://discord.com/api/v9/guilds/1060795343983366144/requests/@me', payload={"version":"2023-04-04T06:47:21.620000+00:00","form_fields":[{"automations":None,"description":None,"field_type":"TERMS","label":"Read and agree to the server rules","required":True,"values":["No external links irrelevant to polyhedra or advertisements","No false/misleading information","No spamming","No offensive names or words","No discrimination","Be respectful"],"response":True}]})
        if response.json()["application_status"] == "APPROVED":
            return True
        else:
            return False

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
            return 1

    def get_fingerprint(self):
        try:
            fingerprint = self.session.get('https://discord.com/api/v9/experiments', proxies=self.proxy).json()['fingerprint']
            return fingerprint
        except:
            return 1
