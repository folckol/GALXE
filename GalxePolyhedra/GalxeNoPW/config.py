import random


campaigns = [
    # 'greenfield',
    # 'luban-mint', 'luban-bridge',
    'opbnb-mint', 'opbnb-bridge',
    # 'core-mint', 'core-bridge',
    # 'zkLightClient-mint', 'zkLightClient-bridge',
    # 'CodeConqueror', 'PixelProwler', 'MelodyMaven', 'EcoGuardian',
    # 'follower',
    # 'discord',
    # 'polyhedra-quote-tweet',
    # 'zkBridge-quote-tweet',
    # 'polyhedra-retweets'
]

delay = random.randint(20, 40)
threads = 1
func = 'twitter'


data = {
    # Socials
    'follower': ['https://galxe.com/polyhedra/campaign/GCMtWUEW5E', 1611184634418823169],
    'discord': 'https://galxe.com/polyhedra/campaign/GCFeWUEck4',
    'polyhedra-quote-tweet': 'https://galxe.com/polyhedra/campaign/GCFwmUXopr',
    'zkBridge-quote-tweet': 'https://galxe.com/polyhedra/campaign/GCW7sUEAyS',
    'polyhedra-retweets': ['https://galxe.com/polyhedra/campaign/GCkmEUN9KB', 1663906700582170626],
    # Main
    'greenfield': ['https://galxe.com/polyhedra/campaign/GCDKiUNoG1', 1665665972370550785],
    'luban-mint': ['https://galxe.com/polyhedra/campaign/GCHdyUQygV', 1668169901377486850],
    'luban-bridge': ['https://galxe.com/polyhedra/campaign/GCbRyUQEER', 0],
    'opbnb-mint': ['https://galxe.com/polyhedra/campaign/GCjrpUSkbq', 1670794025824133124],
    'opbnb-bridge': ['https://galxe.com/polyhedra/campaign/GCRxpUShLa', 0],
    'core-mint': ['https://galxe.com/polyhedra/campaign/GCZqpUS5FL', 1671157876067565568],
    'core-bridge': ['https://galxe.com/polyhedra/campaign/GCgqfUSzBZ', 0],
    'zkMessenger': ['https://galxe.com/polyhedra/campaign/GCDTWUWt4p', 1649217088664530946],
    'zkLightClient-mint': ['https://galxe.com/polyhedra/campaign/GCWQSUNvRa', 1663906700582170626],
    'zkLightClient-bridge': ['https://galxe.com/polyhedra/campaign/GCeoSUNgbg', 0],
    # Pandra
    'CodeConqueror': ['https://galxe.com/polyhedra/campaign/GCN55UezHH', 1678639611692695552],
    'PixelProwler': ['https://galxe.com/polyhedra/campaign/GCZb5Ueoss', 0],
    'MelodyMaven': ['https://galxe.com/polyhedra/campaign/GCZv5Ue14g', 0],
    'EcoGuardian': ['https://galxe.com/polyhedra/campaign/GCZ7tU7LYP', 0]
}
