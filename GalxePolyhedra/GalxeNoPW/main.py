import shutil
import time
import random
import concurrent.futures

from logger import logger
from network.galxe import Galxe
from config import *


def create_lst(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def discord(index, galxe):
    logger.info(f'{index}: Executing...')

    acc_info = galxe.get_acc_info()

    if not acc_info['data']['addressInfo']['hasDiscord']:
        galxe.connect_discord()

    galxe.discord.join_server('WkjUe5tfZP')
    status = galxe.discord.acept_terms()

    if status:
        print('Успешно зашел на сервер')
        # pw.galxe_claim(campaign, data[campaign])
    else:
        print('Зайти на сервер не получилось')


def twitter(index, galxe, friends):
    logger.info(f'{index}: Executing...')

    acc_info = galxe.get_acc_info()

    if not acc_info['data']['addressInfo']['hasTwitter']:
        if not galxe.connect_twitter():
            return

    random.shuffle(campaigns)

    for campaign in campaigns:
        if campaign == 'follower':
            galxe.twitter.follow(data[campaign][1])
        elif campaign == 'zkBridge-quote-tweet':
            galxe.twitter.tweet(f'https://twitter.com/PolyhedraZK/status/1655948436406157312')
        elif campaign == 'polyhedra-quote-tweet':
            # galxe.twitter.follow(urls['follower'][1])
            galxe.twitter.tweet(
                f'#zkbridge https://twitter.com/PolyhedraZK/status/1658111159139020806 {random.choice(friends)}')
        else:
            galxe.twitter.retweet(data[campaign][1], campaign)
        time.sleep(delay)


def claimer(index, galxe):

    logger.info(f'{index}: Executing...')
    for campaign in campaigns:

        galxe.claim(campaign, data[campaign][0].split('/')[-1])


if __name__ == '__main__':

    keys = create_lst('files/private_keys.txt')
    addresses = create_lst('files/addresses.txt')
    proxy = create_lst('files/proxy.txt')
    friends = create_lst('files/friends.txt')
    tw_auth_tokens = create_lst('files/tw_auth_tokens.txt')
    tw_csrf_tokens = create_lst('files/tw_csrf_tokens.txt')
    discord_tokens = create_lst('files/discord_tokens.txt')

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(len(keys)):


            try:
                galxe = Galxe(
                    index=i + 1,
                    proxy=proxy[i],
                    address=addresses[i],
                    private=keys[i],
                    auth_token=tw_auth_tokens[i],
                    csrf=tw_csrf_tokens[i],
                    discord_token=discord_tokens[i],
                    cap_key="63d3cbb6a507096b5fe981cbeed98708",
                    acc_id=i
                )

                if func == 'twitter':
                    executor.submit(twitter, i + 1, galxe, friends)
                elif func == 'claimer':
                    executor.submit(claimer, i + 1, galxe)
                elif func == 'discord':
                    executor.submit(discord, i + 1, galxe)

                # galxe.delete_twitter()
                # galxe.connect_twitter()
                # time.sleep(delay)
            except:
                logger.error(f'{i + 1}: Unknown error')
