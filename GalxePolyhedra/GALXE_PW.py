import datetime
import os
import random
import time
from pathlib import Path
from typing import Generator

import pytest
import ua_generator
from playwright.sync_api import sync_playwright


def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(108, 114)
    firefox_version = random.randint(108, 114)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(9000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

class PWModel:

    def __init__(self, proxy):
        self.playwright = sync_playwright().start()

        EX_path = '10.32.0_0'
        user_data_dir = f"{os.getcwd()}\\dataDir1"

        self.userAgent = ua_generator.generate(device='desktop').text

        self.context = self.playwright.chromium.launch_persistent_context(user_data_dir,
                                                                          user_agent=self.userAgent,
                                                                     proxy={
            "server": f"{proxy.split(':')[0]}:{proxy.split(':')[1]}",
            "username": f"{proxy.split(':')[2]}",
            "password": f"{proxy.split(':')[3]}",
        },headless=False, devtools=False, args=[f'--load-extension={os.getcwd()}\\{EX_path}',
                                               f'--disable-extensions-except={os.getcwd()}\\{EX_path}'])

        print(f"{os.getcwd()}\\{EX_path}")

        # self.context = self.browser.new_context(user_agent=random.choice([
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
        # ]),
        # viewport={"width": random.randint(800, 1920), "height": random.randint(600, 1080)},
        # geolocation={"longitude": random.uniform(-180, 180), "latitude": random.uniform(-90, 90)},
        # locale="en-US")

        # headers = {
        #     "Authorization": AuthorizationToken,
        #     "User-Agent": UA
        # }
        # print(headers)
        # self.context.set_extra_http_headers(headers)


        self.page = self.context.new_page()

        # self.page.set_extra_http_headers(headers)

        self.page.set_default_timeout(60000)



    def Script(self, link, privateKey):
        # Открытие страницы Twitter
        self.page.goto('https://google.com')
        print(self.context.pages)

        self.MMPage = self.context.pages[-1]
        self.MMPage.wait_for_selector('input[id="onboarding__terms-checkbox"]').click()
        self.MMPage.wait_for_selector('button[data-testid="onboarding-create-wallet"]').click()
        self.MMPage.wait_for_selector('button[data-testid="metametrics-i-agree"]').click()
        self.MMPage.wait_for_selector('input[data-testid="create-password-new"]').fill('aADowdms9003dMIK')
        self.MMPage.wait_for_selector('input[data-testid="create-password-confirm"]').fill('aADowdms9003dMIK')
        self.MMPage.wait_for_selector('input[data-testid="create-password-terms"]').click()
        self.MMPage.wait_for_selector('button[data-testid="create-password-wallet"]').click()
        self.MMPage.wait_for_selector('button[data-testid="secure-wallet-later"]').click()
        self.MMPage.wait_for_selector('input[data-testid="skip-srp-backup-popover-checkbox"]').click()
        self.MMPage.wait_for_selector('button[data-testid="skip-srp-backup"]').click()
        self.MMPage.wait_for_selector('button[data-testid="onboarding-complete-done"]').click()
        self.MMPage.wait_for_selector('button[data-testid="pin-extension-next"]').click()
        self.MMPage.wait_for_selector('button[data-testid="pin-extension-done"]').click()
        # self.MMPage.wait_for_selector('button[class="button btn--rounded btn-primary"]').click()
        # self.MMPage.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
        self.MMPage.wait_for_timeout(3000)
        self.MMPage.wait_for_selector('button[data-testid="popover-close"]').click()
        self.MMPage.wait_for_timeout(1000)
        # try:
        #     self.MMPage.wait_for_selector('button[data-testid="popover-close"]').click()
        #     self.MMPage.wait_for_timeout(3000)
        # except:
        #     print('Не нужен селектор')
        #     pass

        self.MMPage.wait_for_selector('button[data-testid="account-menu-icon"]').click()
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/button[2]').click()
        self.MMPage.wait_for_selector('input[id="private-key-box"]').fill(privateKey)
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()

        # self.MMPage.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
        # self.MMPage.wait_for_selector('button[data-testid="account-menu-icon"]').click()
        # self.MMPage.wait_for_selector('button[data-testid="account-menu-icon"]').click()
        # self.MMPage.wait_for_selector('button[data-testid="account-menu-icon"]').click()

        self.page.bring_to_front()
        self.page.goto(link)

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div/button').click()
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[2]/div[2]/div')
        self.page.wait_for_timeout(1500)
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[2]/div[2]/div').click()
        self.MMPage.wait_for_timeout(2000)

        self.MMPage.goto('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        self.MMPage.wait_for_selector('button[class="button btn--rounded btn-primary"]').click()
        self.MMPage.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
        self.MMPage.wait_for_timeout(10000)
        self.MMPage.goto('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        self.MMPage.wait_for_selector('button[data-testid="page-container-footer-next"]').click()


        # self.page.wait_for_selector('xpath=//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]')
        # self.page.wait_for_selector('xpath=//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]')
        # self.page.wait_for_selector('xpath=//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]')
        # self.page.wait_for_selector('xpath=//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]')
        # self.page.wait_for_selector('xpath=//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]')
        # self.page.wait_for_selector('xpath=//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]')



        # self.page.wait_for_timeout(1000000)



        # self.page.eval_on_selector('css=body', 'this.scrollBy(0, 400)')

        # self.page.goto(f"chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html")
        # self.page.wait_for_load_state("load")



    def Test(self):



        self.link = None
        self.campaignName = None

        def intercept_response(response):
            if "https://gcaptcha4.geetest.com/load" in response.url:
                self.link = response.url


        self.page.on('response', intercept_response)

        self.page.wait_for_selector('.claim-button .btn-outter.width-max-100[color="primary"]', timeout=15000).click()

        while self.link == None:
            self.page.wait_for_timeout(1000)


        # self.page.wait_for_timeout(1000000)


    def Polyhedra_Retweets(self):

        self.page.goto('https://galxe.com/polyhedra/campaign/GCkmEUN9KB')

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-1"]/div[1]/div[2]/div/div[1]/div[2]/div/button').click()
        self.page.wait_for_timeout(10000)

        # self.page.wait_for_timeout(1000000)

    def Polyhedra_QuoteTweet(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCFwmUXopr')

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[2]/div[5]/div[2]/div/span/div/div/div/div/div/div/div[1]/div/div/button/div[2]/div/div/div/div[2]/button').click()
        self.page.wait_for_timeout(5000)

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[2]/div[5]/div[2]/div/span/div/div/div/div/div/div/div[1]/div/div/button/div[2]/div/div/div/div[1]/div/div/button').click()
        self.page.wait_for_timeout(5000)

        self.MMPage.goto('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        self.MMPage.wait_for_selector('button[data-testid="page-container-footer-next"]').click()

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div/button').click()
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')


        # self.page.wait_for_selector('div.clickable.refresh.icon').click()
        # self.page.wait_for_timeout(5000)

        # self.page.wait_for_selector(
        #     'xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div/button').click()
        # self.page.wait_for_timeout(10000)

    def Polyhedra_QuoteTweet2(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCW7sUEAyS')

        self.page.wait_for_selector('div.clickable.refresh.icon').click()
        self.page.wait_for_timeout(5000)

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button').click()
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')


    def Polyhedra_Follow(self):

        self.page.goto('https://galxe.com/polyhedra/campaign/GCMtWUEW5E')

        self.page.wait_for_selector(
            'xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[2]/div[5]/div[2]/div/span/div/div/div/div/div/div/div/div/div/button/div[2]/div/div/div/div[1]/div/div/button').click()
        self.page.wait_for_timeout(5000)
        self.page.wait_for_selector(
            'xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div/button').click()
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')

        # self.page.wait_for_timeout(1000000)

    def Polyhedra_DiscordMember(self):

        self.page.goto('https://galxe.com/polyhedra/campaign/GCFeWUEck4')

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[2]/div[5]/div[2]/div/span/div/div/div/div/div/div/div/div/div/button/div[2]/div/div/div/div[1]/div/div/button').click()
        self.page.wait_for_timeout(5000)
        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-0"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div/button').click()
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')

    def zkLightClientNFTCrossChain(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCeoSUNgbg')

        self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
        for button in self.page.query_selector_all('div.clickable.refresh.icon'):
            button.click()
            self.page.wait_for_timeout(7000)

    def zkLightClientNFTMint(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCWQSUNvRa')

        self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
        for button in self.page.query_selector_all('div.clickable.refresh.icon'):
            button.click()
            self.page.wait_for_timeout(7000)

    def GreenfieldTestnetTutorialNFTMint(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCDKiUNoG1')

        try:
            self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
            for button in self.page.query_selector_all('div.clickable.refresh.icon'):
                button.click()
                self.page.wait_for_timeout(7000)
        except:
            pass

        self.page.wait_for_selector('xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button').click()
        self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')

    def BNBChainLubanUpgradeNFTMint(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCHdyUQygV')
        try:
            self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
            for button in self.page.query_selector_all('div.clickable.refresh.icon'):
                button.click()
                self.page.wait_for_timeout(7000)
        except:
            pass

        try:
            self.page.wait_for_selector(
                'xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button', timeout=30).click()
            self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')
        except:
            print('Не удалось дождаться элемента получения награды')

    def BNBChainLubanUpgradeNFTCrossChain(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCbRyUQEER')

        try:
            self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
            for button in self.page.query_selector_all('div.clickable.refresh.icon'):
                button.click()
                self.page.wait_for_timeout(7000)
        except:
            pass

        try:
            self.page.wait_for_selector(
                'xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button', timeout=30).click()
            self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')
        except:
            print('Не удалось дождаться элемента получения награды')

    def opBNBNFTMint(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCjrpUSkbq')

        try:
            self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
            for button in self.page.query_selector_all('div.clickable.refresh.icon'):
                button.click()
                self.page.wait_for_timeout(7000)
        except:
            pass

        try:
            self.page.wait_for_selector(
                'xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button', timeout=30).click()
            self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')
        except:
            print('Не удалось дождаться элемента получения награды')

    def opBNBNFTCrossChain(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCRxpUShLa')

        try:
            self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
            for button in self.page.query_selector_all('div.clickable.refresh.icon'):
                button.click()
                self.page.wait_for_timeout(7000)

        except:
            pass

        try:
            self.page.wait_for_selector(
                'xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button', timeout=30).click()
            self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')
        except:
            print('Не удалось дождаться элемента получения награды')

        # self.page.wait_for_timeout(1000000)

    def BSCPolygonzkMessengerWithzkLightClient(self):
        self.page.goto('https://galxe.com/polyhedra/campaign/GCDTWUWt4p')

        try:
            self.page.wait_for_selector('div.clickable.refresh.icon', timeout=10)
            for button in self.page.query_selector_all('div.clickable.refresh.icon'):
                button.click()
                self.page.wait_for_timeout(7000)

        except:
            pass

        try:
            self.page.wait_for_selector(
                'xpath=//*[@id="ga-data-campaign-model-2"]/div[2]/div[2]/div/div[1]/div[2]/div/button', timeout=30).click()
            self.page.wait_for_selector('xpath=//*[@id="app"]/div[3]/div/div/div/div[1]/div[1]/div[1]')
        except:
            print('Не удалось дождаться элемента получения награды')

        # self.page.wait_for_timeout(1000000)


    def close(self):
        self.browser.close()
        self.playwright.stop()

if __name__ == '__main__':
    PW = PWModel('')

    try:
        PW.Script('https://galxe.com/polyhedra/campaign/GCkmEUN9KB',
                  '')
        PW.Test()

    except:
        input()

