import asyncio
import random
import re
import logging
import time
import psutil
import os
import warnings
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import FloodWaitError
from telethon.tl.functions.users import GetFullUserRequest

# Suppress ALL warnings and errors completely
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.CRITICAL)
logging.getLogger('telethon').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.disable(logging.CRITICAL)

# ==================== CONFIG ====================
API_ID = 27896193
API_HASH = "38a5463cb8bf980d4519fba0ced298c2"
MAIN_OWNER = 5286579067
GLOBAL_SUDO_USERS = []
AUTO_JOIN_LINK = "https://t.me/TheVillainActive"

# ==================== SESSIONS ====================
SESSIONS = [
    {
        "session_string": "1BVtsOIUBu2u76Y3x2wkvFk1_Ktf23V1QIHrYjcymePz3JyLHpwDVs9VMMHxHi0_NSFQhkHCclq6TvpnIrleDWoqNtw1g0v_BiQNZhP2jHC5zUlpxd4t08cGQRUnem7-4yYsJxmzaDSKO9XWTtI7dZ--yUv5uLdE_uAXN5alevKi_jDiQRq8TelQwg9rvV9GTbbsdOTi_zonwwObrgcHPvHOYCGgEY7ibEGemkfd_QZAkOVOuxiljMGmC4QZ68kBQYXY3RM7pi_qwjSTOFRjLOkPrmRJCc8MVI3lscQlTYcLUSHreEzeTJ9zuWw-NbdDfYHaTw8TAm49nix03_RfpadFNgh0RjR8=",
        "owner": 1888914657,
    },
    {
        "session_string": "1BVtsOIUBu2Y20vYpEzgrUmto5tzD3zwOFR7nLtP8kC_9SY7ZKbRqua1hSWI9TG0YTdkYWPgnGIfx8wTVJHM6IpyJ8zBrw_lGgxhQBmvYiX6nB0HJ1IMr2QNvGp54-qxkxBXDsVvVG7qXDrEUBonUw5tFmuvfKZgwLpV6w3yTmATmZJgA82K1UXVaMmoJmkYHmBSikx7e7dBMvZBAqdZJ_65E5HihfgkdiAnSxp1geoV-SuIQroCGc4yT54RJeR4YSljS4Gc2t39aHrLYVwmu0zKziVB7mn4rUMmDly3-YcW1u20IR8y3JlADn0W-Bh1IiJYJp3ADM3Lo0IDSJVldUtlKl5cP0bo=",
        "owner": 1217902673,
    },
    {
        "session_string": "1BVtsOIUBu2Oz8zlkx1yQn4UiWRlDkyNDjMbuavaQaBUVdvJ9N6-f4gtUgm4acFfI-YJ8UPohHp5DIY-arlzPAseCafN4yBX9Nc2K_yJqUqKNOdLh1-IXBTiEHIQbhLbB-HJbs_mNux_jdQxsez0wNwN8I-hZOW_3msjAiTlXexGpyRBFudLiD1JrvPbeA83knhS_ZaH8BLOM7F5oY8kuElramH9Xjw19-lSvATben6_tBfMBk_yIe76LdWIkT91hOz9yqimA6ycWNMrLONYk2BeXUcxam4cQtUcvAND3Y_QG4Mucru56rWmqh8cAEc3zXzCxAq1tQLMnUXP_OnfhkIKmHeuvQQw=",
        "owner": 1779115399,
    },
    {
        "session_string": "1BVtsOIUBu4psZUT2o1SXwjGDKidxzBo7OO62AW1gPZlUjtgQoJV7YsGaNclNBvCInrL5rGWeKIP_iMLzKl5fYnc5-7iWectoBlz6jYenVjajz7qZbINfW2yrFdJw7qua1Q0eVthkfznjgVCFm-jJIxPkyrrg50XCHSymoveQ9IGp2sR9pYN_sAQD94zyYozAWAlnbnLcrw4t4uSpXLvfrIRv8uN_g0Psb18i4ePwFNIRQ5wZg-ePVB7tAH2I4hqMu9myySNtAU0pFFo2anBS-cH12NAikhwlBlqR7MiOyo6qr0DmL8pt2vCBm8RbrSlWCkVk5OF6NrXaNvVVdDzTROHRBfMC4iw=",
        "owner": 1347612918,
    },
    {
        "session_string": "1BVtsOIUBu3qRz355jIaEIe5NJcmIdXklbHVRfcbTmX4j5rm9sAWeBXC8CY9aprQg4ueSNLmNZhnpsCj19gHJoVNurJvPdT9csXiMcseWhH6oNwqv0jlad3_rMvpXEp_XmJDGgJOmWhyt2xUOAAMboekzYhIdgrQY4c3sVa4eAuGlG3b5nQJVpxPLg0fZAA8HTToOWW8-6-TrnQFiuq_9BKlcS3i5d5TgW6_xd4M6WJ7QviPtkMHXtnWbd4JpETQ-NGmknW7NYrkSGbW3OtS9KlpkYWdX06g2beOHhT7TrXGSuDED6gzS1vRqh0XyX_IOmfR4mOdUAplhFXEvkxvcW86H6zIs8Nc=",
        "owner": 6268855785,
    },
]

# ==================== ABUSE LIST ====================
abuse_roast = [
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗔𝗧𝗛𝗜 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗥𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗔𝗚 𝗟𝗚𝗔 𝗞𝗔𝗥 𝟱𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗘𝗧𝗥𝗢𝗟 𝗗𝗔𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗔𝗧𝗛𝗜 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗥𝗨𝗡𝗚𝗔 𝗔𝗨𝗥 𝗝𝗔𝗕 𝗪𝗢 𝗠𝗔𝗥𝗘𝗚𝗜 𝗧𝗢 𝗨𝗦𝗞𝗜 𝗟𝗔𝗦𝗛 𝗞𝗢 𝗚𝗔𝗔𝗡𝗩 𝗠𝗘𝗜𝗡 𝟱𝟬 𝗞𝗨𝗧𝗧𝗢 𝗞𝗘 𝗦𝗔𝗠𝗡𝗘 𝗡𝗔𝗡𝗚𝗔 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗔𝗚 𝗟𝗚𝗔 𝗞𝗔𝗥 𝟱𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗘𝗧𝗥𝗢𝗟 𝗗𝗔𝗔𝗟𝗨𝗡𝗚𝗔 𝗔𝗨𝗥 𝗝𝗔𝗟𝗧𝗘 𝗛𝗨𝗘 𝗨𝗦𝗞𝗢 𝟭𝟬𝟬 𝗔𝗗𝗠𝗜𝗢𝗡 𝗞𝗘 𝗕𝗜𝗖𝗛 𝗖𝗛𝗢𝗗𝗪𝗔𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗚𝗔𝗗𝗗𝗛𝗢𝗡 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔 𝗞𝗔𝗥 𝗨𝗦𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗖𝗛𝗔𝗖𝗛𝗨𝗡𝗗𝗥𝗘 𝗣𝗔𝗟𝗨𝗡𝗚𝗔 𝗔𝗨𝗥 𝗧𝗨 𝗗𝗘𝗞𝗛𝗧𝗔 𝗥𝗔𝗛𝗘𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝗦𝗔𝗗𝗔𝗞 𝗣𝗘 𝟭𝟬𝟬 𝗧𝗥𝗨𝗖𝗞𝗢 𝗦𝗘 𝗞𝗨𝗖𝗛𝗟𝗪𝗔 𝗞𝗔𝗥 𝗣𝗜𝗦 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 𝗔𝗨𝗥 𝗨𝗦𝗞𝗔 𝗞𝗘𝗖𝗛𝗨𝗣 𝗕𝗡𝗔 𝗞𝗔𝗥 𝗧𝗨𝗝𝗛𝗘 𝗣𝗜𝗟𝗔𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗠𝗘𝗧𝗥𝗢 𝗧𝗥𝗔𝗜𝗡 𝗖𝗛𝗔𝗟𝗔 𝗞𝗔𝗥 𝗨𝗦𝗞𝗢 𝗘𝗞𝗦𝗣𝗥𝗘𝗦𝗪𝗘𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗚𝗔𝗡𝗗 𝗠𝗘𝗜𝗡 𝗘𝗜𝗙𝗙𝗘𝗟 𝗧𝗢𝗪𝗘𝗥 𝗚𝗛𝗨𝗦𝗔 𝗞𝗔𝗥 𝗨𝗦𝗞𝗢 𝗣𝗔𝗥𝗜𝗦 𝗞𝗔 𝗧𝗢𝗨𝗥𝗜𝗦𝗧 𝗦𝗣𝗢𝗧 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟱𝟬𝟬𝟬 𝗕𝗔𝗖𝗖𝗛𝗘 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗨𝗡𝗞𝗔 𝗖𝗛𝗜𝗟𝗗𝗥𝗘𝗡 𝗣𝗔𝗥𝗞 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗦𝗨𝗔𝗥 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗣𝗜𝗚 𝗙𝗔𝗥𝗠 𝗞𝗛𝗢𝗟 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟱𝟬 𝗞𝗠 𝗟𝗔𝗠𝗕𝗔 𝗖𝗛𝗢𝗥𝗔 𝗞𝗔𝗥 𝗞𝗘 𝗨𝗦𝗠𝗘𝗜𝗡 𝗛𝗜𝗡𝗗𝗠𝗔𝗛𝗔𝗦𝗔𝗚𝗔𝗥 𝗗𝗨𝗕𝗢 𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗖𝗥𝗢𝗖𝗢𝗗𝗜𝗟𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗠𝗚𝗠 𝗖𝗥𝗢𝗖 𝗣𝗔𝗥𝗞 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝗚𝗔𝗡𝗚𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗛𝗜𝗡𝗗𝗨𝗦𝗧𝗔𝗡 𝗞𝗢 𝗣𝗔𝗩𝗜𝗧𝗥𝗔 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬𝟬 𝗩𝗢𝗟𝗧 𝗞𝗔 𝗞𝗔𝗥𝗥𝗘𝗡𝗧 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗕𝗝𝗟𝗜 𝗚𝗥𝗜𝗗𝗗 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗕𝗔𝗥𝗨𝗗 𝗞𝗘 𝗕𝗢𝗠𝗕 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗛𝗜𝗥𝗢𝗦𝗛𝗜𝗠𝗔 𝗥𝗶𝗽𝗲 𝗸𝗮𝗿 𝗱𝗮𝗹𝘂𝗻𝗴𝗮",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗦𝗔𝗠𝗢𝗦𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗦𝗔𝗠𝗢𝗦𝗔 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗞𝗛𝗢𝗟 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬 𝗠𝗔𝗡𝗭𝗜𝗟 𝗕𝗨𝗜𝗟𝗗𝗜𝗡𝗚 𝗕𝗡𝗔 𝗞𝗔𝗥 𝟱𝟬𝟬𝟬 𝗟𝗢𝗚𝗢 𝗞𝗢 𝗥𝗘𝗛𝗡𝗘 𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬 𝗣𝗟𝗔𝗡𝗘 𝗟𝗔𝗡𝗗 𝗞𝗥𝗪𝗔 𝗞𝗔𝗥 𝗜𝗡𝗧𝗘𝗥𝗡𝗔𝗧𝗜𝗢𝗡𝗔𝗟 𝗔𝗜𝗥𝗣𝗢𝗥𝗧 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗜𝗡𝗞 𝗟𝗨𝗕𝗘 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗜𝗡𝗗𝗜𝗔 𝗞𝗜 𝗦𝗔𝗥𝗜 𝗥𝗔𝗡𝗗𝗜𝗬𝗢 𝗞𝗢 𝗙𝗥𝗘𝗘 𝗗𝗘 𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗟𝗔𝗧𝗛𝗜 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗨𝗦𝗞𝗔 𝗚𝗔𝗡𝗗 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗥𝗔 𝗞𝗥 𝗗𝗨𝗡𝗚𝗔 𝗞𝗜 𝗨𝗦𝗠𝗘𝗜𝗡 𝟭𝟬𝟬 𝗔𝗗𝗠𝗜 𝗘𝗞 𝗦𝗔𝗧𝗛 𝗚𝗛𝗨𝗦 𝗝𝗔𝗬𝗘𝗡𝗚𝗘",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗗𝗚𝗥𝗘𝗘 𝗣𝗘 𝗚𝗔𝗥𝗠 𝗞𝗥 𝗞𝗘 𝗦𝗧𝗘𝗘𝗟 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗠𝗘𝗜𝗡 𝗣𝗜𝗚𝗛𝗟𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬𝟬 𝗖𝗛𝗘𝗘𝗡𝗜 𝗞𝗘 𝗠𝗮𝘇𝗱𝘂𝗿 𝗱𝗮𝗮𝗹 𝗸𝗮𝗿 𝗚𝗿𝗲𝗮𝘁 𝗪𝗮𝗹𝗹 𝗼𝗳 𝗖𝗵𝗶𝗻𝗮 𝗯𝗻𝗮 𝗱𝗮𝗹𝘂𝗻𝗴𝗮",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗞𝗠 𝗟𝗔𝗠𝗕𝗔 𝗥𝗔𝗭𝗭 𝗪𝗜𝗥𝗘 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗣𝗨𝗥𝗘 𝗜𝗡𝗗𝗜𝗔 𝗞𝗢 𝗕𝗜𝗝𝗟𝗜 𝗦𝗨𝗣𝗟𝗬 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗦𝗨𝗥𝗔𝗡𝗚 𝗞𝗛𝗢𝗗 𝗞𝗔𝗥 𝗗𝗘𝗟𝗛𝗜 𝗠𝗘𝗧𝗥𝗢 𝗞𝗢 𝗘𝗫𝗧𝗘𝗡𝗗 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗖𝗛𝗨𝗛𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗘𝗫𝗣𝗘𝗥𝗜𝗠𝗘𝗡𝗧 𝗟𝗔𝗕 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬 𝗠𝗜𝗡ＡＲ 𝗕𝗡𝗔 𝗞𝗔𝗥 𝗗𝗨𝗕𝗔𝗜 𝗠𝗘𝗜𝗡 𝗕𝗨𝗥𝗝 𝗞𝗛𝗔𝗟𝗜𝗙𝗔 𝗦𝗘 𝗖𝗢𝗠𝗣𝗘𝗧𝗜𝗧𝗜𝗢𝗡 𝗞𝗥𝗪𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗔𝗦𝗦𝗜𝗡𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗦𝗔𝗛𝗔𝗥𝗔 𝗥𝗘𝗚𝗜𝗦𝗧𝗔𝗡 𝗞𝗢 𝗛𝗔𝗥𝗔 𝗕𝗛𝗥𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗕𝗛𝗘𝗗 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗢𝗦𝗧𝗥𝗘𝗟𝗜𝗬𝗔 𝗞𝗔 𝗦𝗛𝗘𝗘𝗣 𝗙𝗔𝗥𝗠 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗗𝗙 𝗠𝗢𝗕𝗜𝗟𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗪𝗔𝗟𝗧𝗘𝗥 𝗪𝗛𝗜𝗧𝗘 𝗞𝗜 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗗𝗔𝗥𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗧𝗛𝗘𝗞𝗘 𝗪𝗔𝗟𝗢𝗞 𝗞𝗢 𝗠𝗨𝗙𝗧 𝗠𝗘𝗜𝗡 𝗣𝗜𝗟𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗞𝗚 𝗦𝗢𝗡𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗚𝗢𝗟𝗗 𝗚ＹＭ 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗠𝗢𝗕𝗜𝗟𝗘 𝗧𝗢𝗪𝗘𝗥 𝗟𝗚𝗔 𝗞𝗔𝗥 𝟱𝗚 𝗡𝗘𝗧𝗪𝗢𝗥𝗞 𝗖𝗢𝗩𝗘𝗥𝗔𝗚𝗘 𝗗𝗘 𝗗𝗔𝗟𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘 𝗖𝗛𝗔𝗞𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗧 𝗞𝗔 𝗞𝗛𝗢𝗢𝗡 𝗞𝗔𝗥 𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘 𝗞𝗘𝗟𝗘 𝗞𝗘 𝗖𝗛𝗜𝗟𝗞𝗘",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗟𝗘𝗧𝗜 𝗠𝗘𝗥𝗜 𝗟𝗨𝗡𝗗 𝗕𝗔𝗗𝗘 𝗠𝗔𝗦𝗧𝗜 𝗦𝗘",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗢 𝗠𝗘𝗡𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗕𝗢𝗛𝗢𝗧 𝗦𝗔𝗦𝗧𝗘 𝗦𝗘",
    "𝗧𝗘𝗥𝗘 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗠𝗔𝗗𝗔𝗥𝗖𝗛𝗢𝗗",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗟𝗘𝗞𝗘 𝗕𝗛𝗔𝗚 𝗝𝗔𝗔𝗨𝗡𝗚𝗔",
    "𝗞𝗜𝗗𝗭 𝗠𝗔𝗗𝗔𝗥𝗖𝗛𝗢𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘",
    "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗠𝗘 𝗥𝗘𝗛𝗧𝗔 𝗛𝗘 𝗦𝗔𝗡𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔",
    "𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗠𝗨𝗝𝗛𝗞𝗢 𝗣𝗔𝗣𝗔 𝗞𝗬𝗢𝗨𝗡𝗞𝗜 𝗠𝗘𝗡𝗘 𝗕𝗔𝗡𝗔𝗗𝗜𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧",
    "𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗢𝗧𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗣𝗨𝗥𝗔 𝗙𝗔𝗔𝗗 𝗗𝗜𝗔 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗔𝗕𝗕 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝 😆💦🤤",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗘𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗔 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗧𝗢 𝗠𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗕𝗔𝗡𝗚𝗔𝗬𝗜 𝗔𝗕𝗕 𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗖𝗛𝗢𝗗𝗧𝗔 𝗙𝗜𝗥𝗦𝗘 ♥️💦😆😆😆😆",
    "𝗛𝗔𝗥𝗜 𝗛𝗔𝗥𝗜 𝗚𝗛𝗔𝗔𝗦 𝗠𝗘 𝗝𝗛𝗢𝗣𝗗𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 🤣🤣💋💦",
    "𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗘 𝗕𝗔𝗔𝗣 𝗞𝗢 𝗕𝗛𝗘𝗝 𝗧𝗘𝗥𝗔 𝗕𝗔𝗦𝗞𝗔 𝗡𝗛𝗜 𝗛𝗘 𝗣𝗔𝗣𝗔 𝗦𝗘 𝗟𝗔𝗗𝗘𝗚𝗔 𝗧𝗨",
    "𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗠𝗘 𝗕𝗢𝗠𝗕 𝗗𝗔𝗟𝗞𝗘 𝗨𝗗𝗔 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔‌𝗔‌𝗞𝗘 𝗟𝗔𝗪𝗗𝗘",
    "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗧𝗥𝗔𝗜𝗡 𝗠𝗘 𝗟𝗘𝗝𝗔𝗞𝗘 𝗧𝗢𝗣 𝗕𝗘𝗗 𝗣𝗘 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 🤣🤣💋💋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗔𝗞𝗘 𝗡𝗨𝗗𝗘𝗦 𝗚𝗢𝗢𝗚𝗟𝗘 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗘𝗪𝗗𝗘 👻🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗩𝗜𝗗𝗘𝗢 𝗕𝗔𝗡𝗔𝗞𝗘 𝗫𝗡𝗫𝗫.𝗖𝗢𝗠 𝗣𝗘 𝗡𝗘𝗘𝗟𝗔𝗠 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗞𝗨𝗧𝗧𝗘 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦💋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗔𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗢 𝗣𝗢𝗥𝗡𝗛𝗨𝗕.𝗖𝗢𝗠 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 🤣💋💦",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗘𝗞𝗢 𝗖𝗛𝗔𝗞𝗞𝗢 𝗦𝗘 𝗣𝗜𝗟𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 🤣🤣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗙𝗔𝗔𝗗𝗞𝗘 𝗥𝗔𝗞𝗗𝗜𝗔 𝗠𝗔‌𝗔‌𝗞𝗘 𝗟𝗢𝗗𝗘 𝗝𝗔𝗔 𝗔𝗕𝗕 𝗦𝗜𝗟𝗪𝗔𝗟𝗘 👄👄",
    "𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗨𝗡𝗗 𝗞𝗔𝗔𝗟𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗟𝗘𝗧𝗜 𝗠𝗘𝗥𝗜 𝗟𝗨𝗡𝗗 𝗕𝗔𝗗𝗘 𝗠𝗔𝗦𝗧𝗜 𝗦𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗢 𝗠𝗘𝗡𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗕𝗢𝗛𝗢𝗧 𝗦𝗔𝗦𝗧𝗘 𝗦𝗘",
    "𝗕𝗘𝗧𝗘 𝗧𝗨 𝗕𝗔𝗔𝗣 𝗦𝗘 𝗟𝗘𝗚𝗔 𝗣𝗔𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘 𝗡𝗔𝗡𝗚𝗔 💦💋",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗔𝗚𝗟𝗜 𝗕𝗔𝗔𝗥 𝗔𝗣𝗡𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗧 𝗢𝗥 𝗠𝗘𝗥𝗘 𝗠𝗢𝗧𝗘 𝗟𝗨𝗡𝗗 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥",
    "𝗖𝗛𝗔𝗟 𝗕𝗘𝗧𝗔 𝗧𝗨𝗝𝗛𝗘 𝗠𝗔‌𝗔‌𝗙 𝗞𝗜𝗔 🤣 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝",
    "𝗦𝗛𝗔𝗥𝗔𝗠 𝗞𝗔𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗞𝗜𝗧𝗡𝗔 𝗚𝗔𝗔𝗟𝗜𝗔 𝗦𝗨𝗡𝗪𝗔𝗬𝗘𝗚𝗔 𝗔𝗣𝗡𝗜 𝗠𝗔‌𝗔‌𝗔 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗘 𝗨𝗣𝗘𝗥",
    "𝗔𝗕𝗘 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗔𝗨𝗞𝗔𝗧 𝗡𝗛𝗜 𝗛𝗘𝗧𝗢 𝗔𝗣𝗡𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥 𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔",
    "𝗞𝗜𝗗𝗭 𝗠𝗔‌𝗔‌𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗧𝗘𝗥𝗥 𝗟𝗜𝗬𝗘 𝗕𝗛𝗔𝗜 𝗗𝗘𝗗𝗜𝗬𝗔",
    "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗗𝗘𝗞𝗞𝗘 𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 🤣🤣💦💋",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗠𝗘 𝗥𝗘𝗛𝗧𝗔 𝗛𝗘 𝗦𝗔𝗡𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗢𝗥 𝗕𝗔𝗡𝗔 𝗗𝗜𝗔 𝗥𝗔𝗡𝗗 🤤🤣",
    "𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗠𝗨𝗝𝗛𝗞𝗢 𝗣𝗔𝗣𝗔 𝗞𝗬𝗢𝗨𝗡𝗞𝗜 𝗠𝗘𝗡𝗘 𝗕𝗔𝗡𝗔𝗗𝗜𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧 🤣🤣",
    "𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗠𝗘 𝗦𝗨𝗔𝗥 𝗞𝗔 𝗟𝗢𝗨𝗗𝗔 𝗢𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘‌𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨‌𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗢𝗗𝗔",
    "𝗖𝗛𝗔𝗟 𝗖𝗛𝗔𝗟 𝗔𝗣𝗡𝗜 𝗠𝗔‌𝗔‌𝗞𝗜 𝗖𝗛𝗨𝗖𝗛𝗜𝗬𝗔 𝗗𝗜𝗞𝗔",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗔𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗜𝗔 𝗡𝗔𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗛𝗘 𝗕𝗔𝗗𝗜 𝗦𝗘𝗫𝗬 𝗨𝗦𝗞𝗢 𝗣𝗜𝗟𝗔𝗞𝗘 𝗖𝗛𝗢𝗢𝗗𝗘𝗡𝗚𝗘 𝗣𝗘𝗣𝗦𝗜",
    "2 𝗥𝗨𝗣𝗔𝗬 𝗞𝗜 𝗣𝗘𝗣𝗦𝗜 𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗦𝗔𝗕𝗦𝗘 𝗦𝗘𝗫𝗬 💋💦",
    "𝗧𝗘𝗥𝗜 𝗠𝗔‌𝗔‌𝗞𝗢 𝗖𝗛𝗘𝗘𝗠𝗦 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗠𝗔𝗗𝗘𝗥𝗖𝗛𝗢𝗢𝗗 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦🤣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗔𝗧𝗛𝗜 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗥𝗨𝗡𝗚𝗔 💀🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗔𝗚 𝗟𝗚𝗔 𝗞𝗔𝗥 𝟱𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗘𝗧𝗥𝗢𝗟 𝗗𝗔𝗔𝗟𝗨𝗡𝗚𝗔 🔥👊",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗚𝗔𝗗𝗗𝗛𝗢𝗡 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔 𝗞𝗔𝗥 𝗨𝗦𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗖𝗛𝗔𝗖𝗛𝗨𝗡𝗗𝗥𝗘 𝗣𝗔𝗟𝗨𝗡𝗚𝗔 🐀💢",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝗦𝗔𝗗𝗔𝗞 𝗣𝗘 𝟭𝟬𝟬 𝗧𝗥𝗨𝗖𝗞𝗢 𝗦𝗘 𝗞𝗨𝗖𝗛𝗟𝗪𝗔 𝗞𝗔𝗥 𝗣𝗜𝗦 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🚛💀",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗠𝗘𝗧𝗥𝗢 𝗧𝗥𝗔𝗜𝗡 𝗖𝗛𝗔𝗟𝗔 𝗞𝗔𝗥 𝗨𝗦𝗞𝗢 𝗘𝗞𝗦𝗣𝗥𝗘𝗦𝗪𝗘𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🚇💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗚𝗔𝗡𝗗 𝗠𝗘𝗜𝗡 𝗘𝗜𝗙𝗙𝗘𝗟 𝗧𝗢𝗪𝗘𝗥 𝗚𝗛𝗨𝗦𝗔 𝗞𝗔𝗥 𝗨𝗦𝗞𝗢 𝗣𝗔𝗥𝗜𝗦 𝗞𝗔 𝗧𝗢𝗨𝗥𝗜𝗦𝗧 𝗦𝗣𝗢𝗧 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🗼🍑",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟱𝟬𝟬𝟬 𝗕𝗔𝗖𝗖𝗛𝗘 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗨𝗡𝗞𝗔 𝗖𝗛𝗜𝗟𝗗𝗥𝗘𝗡 𝗣𝗔𝗥𝗞 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 👶🎪",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗦𝗨𝗔𝗥 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗣𝗜𝗚 𝗙𝗔𝗥𝗠 𝗞𝗛𝗢𝗟 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🐷🐽",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟱𝟬 𝗞𝗠 𝗟𝗔𝗠𝗕𝗔 𝗖𝗛𝗢𝗥𝗔 𝗞𝗔𝗥 𝗞𝗘 𝗨𝗦𝗠𝗘𝗜𝗡 𝗛𝗜𝗡𝗗𝗠𝗔𝗛𝗔𝗦𝗔𝗚𝗔𝗥 𝗗𝗨𝗕𝗢 𝗗𝗨𝗡𝗚𝗔 🌊🚤",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗖𝗥𝗢𝗖𝗢𝗗𝗜𝗟𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗠𝗚𝗠 𝗖𝗥𝗢𝗖 𝗣𝗔𝗥𝗞 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🐊🐊",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝗚𝗔𝗡𝗚𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗛𝗜𝗡𝗗𝗨𝗦𝗧𝗔𝗡 𝗞𝗢 𝗣𝗔𝗩𝗜𝗧𝗥𝗔 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🌊🕉️",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬𝟬 𝗩𝗢𝗟𝗧 𝗞𝗔 𝗞𝗔𝗥𝗥𝗘𝗡𝗧 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗕𝗝𝗟𝗜 𝗚𝗥𝗜𝗗𝗗 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 ⚡🔌",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗕𝗔𝗥𝗨𝗗 𝗞𝗘 𝗕𝗢𝗠𝗕 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗛𝗜𝗥𝗢𝗦𝗛𝗜𝗠𝗔 𝟮.𝟬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 💣💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗦𝗔𝗠𝗢𝗦𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗦𝗔𝗠𝗢𝗦𝗔 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗞𝗛𝗢𝗟 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🥟🏭",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬 𝗠𝗔𝗡𝗭𝗜𝗟 𝗕𝗨𝗜𝗟𝗗𝗜𝗡𝗚 𝗕𝗡𝗔 𝗞𝗔𝗥 𝟱𝟬𝟬𝟬 𝗟𝗢𝗚𝗢 𝗞𝗢 𝗥𝗘𝗛𝗡𝗘 𝗗𝗨𝗡𝗚𝗔 🏢🏙️",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬 𝗣𝗟𝗔𝗡𝗘 𝗟𝗔𝗡𝗗 𝗞𝗥𝗪𝗔 𝗞𝗔𝗥 𝗜𝗡𝗧𝗘𝗥𝗡𝗔𝗧𝗜𝗢𝗡𝗔𝗟 𝗔𝗜𝗥𝗣𝗢𝗥𝗧 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 ✈️🛫",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗜𝗡𝗞 𝗟𝗨𝗕𝗘 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗜𝗡𝗗𝗜𝗔 𝗞𝗜 𝗦𝗔𝗥𝗜 𝗥𝗔𝗡𝗗𝗜𝗬𝗢 𝗞𝗢 𝗙𝗥𝗘𝗘 𝗗𝗘 𝗗𝗨𝗡𝗚𝗔 💗💦",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗟𝗔𝗧𝗛𝗜 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗨𝗦𝗞𝗔 𝗚𝗔𝗡𝗗 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗥𝗔 𝗞𝗥 𝗗𝗨𝗡𝗚𝗔 𝗞𝗜 𝗨𝗦𝗠𝗘𝗜𝗡 𝟭𝟬𝟬 𝗔𝗗𝗠𝗜 𝗘𝗞 𝗦𝗔𝗧𝗛 𝗚𝗛𝗨𝗦 𝗝𝗔𝗬𝗘𝗡𝗚𝗘 🍑👥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗗𝗚𝗥𝗘𝗘 𝗣𝗘 𝗚𝗔𝗥𝗠 𝗞𝗥 𝗞𝗘 𝗦𝗧𝗘𝗘𝗟 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗠𝗘𝗜𝗡 𝗣𝗜𝗚𝗛𝗟𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🔥🏭",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬𝟬 𝗖𝗛𝗜𝗡𝗜 𝗞𝗘 𝗠𝗔𝗭𝗗𝗨𝗥 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗚𝗥𝗘𝗔𝗧 𝗪𝗔𝗟𝗟 𝗢𝗙 𝗖𝗛𝗜𝗡𝗔 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧱🇨🇳",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗞𝗠 𝗟𝗔𝗠𝗕𝗔 𝗥𝗔𝗭𝗭 𝗪𝗜𝗥𝗘 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗣𝗨𝗥𝗘 𝗜𝗡𝗗𝗜𝗔 𝗞𝗢 𝗕𝗜𝗝𝗟𝗜 𝗦𝗨𝗣𝗟𝗬 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 ⚡🇮🇳",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗦𝗨𝗥𝗔𝗡𝗚 𝗞𝗛𝗢𝗗 𝗞𝗔𝗥 𝗗𝗘𝗟𝗛𝗜 𝗠𝗘𝗧𝗥𝗢 𝗞𝗢 𝗘𝗫𝗧𝗘𝗡𝗗 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🚇🕳️",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗖𝗛𝗨𝗛𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗘𝗫𝗣𝗘𝗥𝗜𝗠𝗘𝗡𝗧 𝗟𝗔𝗕 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🐁🔬",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬 𝗠𝗜𝗡𝗔𝗥 𝗕𝗡𝗔 𝗞𝗔𝗥 𝗗𝗨𝗕𝗔𝗜 𝗠𝗘𝗜𝗡 𝗕𝗨𝗥𝗝 𝗞𝗛𝗔𝗟𝗜𝗙𝗔 𝗦𝗘 𝗖𝗢𝗠𝗣𝗘𝗧𝗜𝗧𝗜𝗢𝗡 𝗞𝗥𝗪𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🏗️🇦🇪",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗔𝗦𝗦𝗜𝗡𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗦𝗔𝗛𝗔𝗥𝗔 𝗥𝗘𝗚𝗜𝗦𝗧𝗔𝗡 𝗞𝗢 𝗛𝗔𝗥𝗔 𝗕𝗛𝗥𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🏜️💧",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗕𝗛𝗘𝗗 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗢𝗦𝗧𝗥𝗘𝗟𝗜𝗬𝗔 𝗞𝗔 𝗦𝗛𝗘𝗘𝗣 𝗙𝗔𝗥𝗠 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🐑🇦🇺",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗗𝗙 𝗠𝗢𝗕𝗜𝗟𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗪𝗔𝗟𝗧𝗘𝗥 𝗪𝗛𝗜𝗧𝗘 𝗞𝗜 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧪⚗️",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗗𝗔𝗥𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗧𝗛𝗘𝗞𝗘 𝗪𝗔𝗟𝗢𝗞 𝗞𝗢 𝗠𝗨𝗙𝗧 𝗠𝗘𝗜𝗡 𝗣𝗜𝗟𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🍻🥃",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗞𝗚 𝗦𝗢𝗡𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗚𝗢𝗟𝗗 𝗚𝗬𝗠 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🏋️‍♂️🥇",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗠𝗢𝗕𝗜𝗟𝗘 𝗧𝗢𝗪𝗘𝗥 𝗟𝗚𝗔 𝗞𝗔𝗥 𝟱𝗚 𝗡𝗘𝗧𝗪𝗢𝗥𝗞 𝗖𝗢𝗩𝗘𝗥𝗔𝗚𝗘 𝗗𝗘 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 📱📶",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘 𝗖𝗛𝗔𝗞𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗧 𝗞𝗔 𝗞𝗛𝗢𝗢𝗡 𝗞𝗔𝗥 𝗗𝗨𝗡𝗚𝗔 🔪🩸",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘 𝗞𝗘𝗟𝗘 𝗞𝗘 𝗖𝗛𝗜𝗟𝗞𝗘 🍌🧻",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗟𝗘𝗧𝗜 𝗠𝗘𝗥𝗜 𝗟𝗨𝗡𝗗 𝗕𝗔𝗗𝗘 𝗠𝗔𝗦𝗧𝗜 𝗦𝗘 🍆💦",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗢 𝗠𝗘𝗡𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗕𝗢𝗛𝗢𝗧 𝗦𝗔𝗦𝗧𝗘 𝗦𝗘 🍑💢",
    "𝗧𝗘𝗥𝗘 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗠𝗔𝗗𝗔𝗥𝗖𝗛𝗢𝗗 👊🤬",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗟𝗘𝗞𝗘 𝗕𝗛𝗔𝗚 𝗝𝗔𝗔𝗨𝗡𝗚𝗔 🏃💨",
    "𝗞𝗜𝗗𝗭 𝗠𝗔𝗗𝗔𝗥𝗖𝗛𝗢𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 💀🔥",
    "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 🦚💃",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗠𝗘 𝗥𝗘𝗛𝗧𝗔 𝗛𝗘 𝗦𝗔𝗡𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 🏘️💢",
    "𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗠𝗨𝗝𝗛𝗞𝗢 𝗣𝗔𝗣𝗔 𝗞𝗬𝗢𝗨𝗡𝗞𝗜 𝗠𝗘𝗡𝗘 𝗕𝗔𝗡𝗔𝗗𝗜𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧 🤰🍼",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗢𝗧𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗣𝗨𝗥𝗔 𝗙𝗔𝗔𝗗 𝗗𝗜𝗔 𝗖𝗛𝗨𝗨𝗧𝗛 𝗔𝗕𝗕 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝 😆💦🤤",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗘𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗔 𝗕𝗘𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗧𝗢 𝗠𝗘𝗥𝗜 𝗥𝗔𝗡𝗗𝗜 𝗕𝗔𝗡𝗚𝗔𝗬𝗜 𝗔𝗕𝗕 𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗢 𝗖𝗛𝗢𝗗𝗧𝗔 𝗙𝗜𝗥𝗦𝗘 ♥️💦😆",
    "𝗛𝗔𝗥𝗜 𝗛𝗔𝗥𝗜 𝗚𝗛𝗔𝗔𝗦 𝗠𝗘 𝗝𝗛𝗢𝗣𝗗𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 🤣🤣💋💦",
    "𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗘 𝗕𝗔𝗔𝗣 𝗞𝗢 𝗕𝗛𝗘𝗝 𝗧𝗘𝗥𝗔 𝗕𝗔𝗦𝗞𝗔 𝗡𝗛𝗜 𝗛𝗘 𝗣𝗔𝗣𝗔 𝗦𝗘 𝗟𝗔𝗗𝗘𝗚𝗔 𝗧𝗨 👊😈",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨𝗧𝗛 𝗠𝗘 𝗕𝗢𝗠𝗕 𝗗𝗔𝗟𝗞𝗘 𝗨𝗗𝗔 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔𝗔𝗞𝗘 𝗟𝗔𝗪𝗗𝗘 💣💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗢 𝗧𝗥𝗔𝗜𝗡 𝗠𝗘 𝗟𝗘𝗝𝗔𝗞𝗘 𝗧𝗢𝗣 𝗕𝗘𝗗 𝗣𝗘 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 🚂💺",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗘 𝗡𝗨𝗗𝗘𝗦 𝗚𝗢𝗢𝗚𝗟𝗘 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗕𝗘𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗘𝗪𝗗𝗘 📸🌐",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗩𝗜𝗗𝗘𝗢 𝗕𝗔𝗡𝗔𝗞𝗘 𝗫𝗡𝗫𝗫.𝗖𝗢𝗠 𝗣𝗘 𝗡𝗘𝗘𝗟𝗔𝗠 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗞𝗨𝗧𝗧𝗘 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 🎥💻",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗢 𝗣𝗢𝗥𝗡𝗛𝗨𝗕.𝗖𝗢𝗠 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 📹🔞",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗥𝗔𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗘𝗞𝗢 𝗖𝗛𝗔𝗞𝗞𝗢 𝗦𝗘 𝗣𝗜𝗟𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗥𝗔𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 🤣🤣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗜 𝗖𝗛𝗨𝗨𝗧𝗛 𝗙𝗔𝗔𝗗𝗞𝗘 𝗥𝗔𝗞𝗗𝗜𝗔 𝗠𝗔𝗔𝗞𝗘 𝗟𝗢𝗗𝗘 𝗝𝗔𝗔 𝗔𝗕𝗕 𝗦𝗜𝗟𝗪𝗔𝗟𝗘 👄👄",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗨𝗡𝗗 𝗞𝗔𝗔𝗟𝗔 🖤🍆",
    "𝗕𝗘𝗧𝗘 𝗧𝗨 𝗕𝗔𝗔𝗣 𝗦𝗘 𝗟𝗘𝗚𝗔 𝗣𝗔𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘 𝗡𝗔𝗡𝗚𝗔 💦💋",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗔𝗚𝗟𝗜 𝗕𝗔𝗔𝗥 𝗔𝗣𝗡𝗜 𝗠𝗔𝗔𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗧 𝗢𝗥 𝗠𝗘𝗥𝗘 𝗠𝗢𝗧𝗘 𝗟𝗨𝗡𝗗 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗬𝗔 😂🍆",
    "𝗖𝗛𝗔𝗟 𝗕𝗘𝗧𝗔 𝗧𝗨𝗝𝗛𝗘 𝗠𝗔𝗔𝗙 𝗞𝗜𝗔 🤣 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝 👯‍♀️💋",
    "𝗦𝗛𝗔𝗥𝗔𝗠 𝗞𝗔𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗞𝗜𝗧𝗡𝗔 𝗚𝗔𝗔𝗟𝗜𝗔 𝗦𝗨𝗡𝗪𝗔𝗬𝗘𝗚𝗔 𝗔𝗣𝗡𝗜 𝗠𝗔𝗔 𝗕𝗘𝗛𝗘𝗡 𝗞𝗘 𝗨𝗣𝗘𝗥 📢👂",
    "𝗔𝗕𝗘 𝗥𝗔𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗔𝗨𝗞𝗔𝗧 𝗡𝗛𝗜 𝗛𝗘𝗧𝗢 𝗔𝗣𝗡𝗜 𝗥𝗔𝗡𝗗𝗜 𝗠𝗔𝗔𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥 𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔 😂😂",
    "𝗞𝗜𝗗𝗭 𝗠𝗔𝗔𝗗𝗔𝗥𝗖𝗛𝗢𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗧𝗘𝗥𝗥 𝗟𝗜𝗬𝗘 𝗕𝗛𝗔𝗜 𝗗𝗘𝗗𝗜𝗬𝗔 💀☠️",
    "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗗𝗘𝗞𝗞𝗘 𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 🤣🤣💦💋",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗠𝗘 𝗥𝗘𝗛𝗧𝗔 𝗛𝗘 𝗦𝗔𝗡𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗢𝗥 𝗕𝗔𝗡𝗔 𝗗𝗜𝗔 𝗥𝗔𝗡𝗗 🤤🤣",
    "𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗠𝗨𝗝𝗛𝗞𝗢 𝗣𝗔𝗣𝗔 𝗞𝗬𝗢𝗨𝗡𝗞𝗜 𝗠𝗘𝗡𝗘 𝗕𝗔𝗡𝗔𝗗𝗜𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧 🤣🤣",
    "𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗜 𝗖𝗛𝗨𝗨𝗧𝗛 𝗠𝗘 𝗦𝗨𝗔𝗥 𝗞𝗔 𝗟𝗢𝗨𝗗𝗔 𝗢𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗢𝗗𝗔 🐷🍆",
    "𝗖𝗛𝗔𝗟 𝗖𝗛𝗔𝗟 𝗔𝗣𝗡𝗜 𝗠𝗔𝗔𝗞𝗜 𝗖𝗛𝗨𝗖𝗛𝗜𝗬𝗔 𝗗𝗜𝗞𝗔 👀🍑",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗔𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗜𝗔 𝗡𝗔𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘 😂🔥",
    "2 𝗥𝗨𝗣𝗔𝗬 𝗞𝗜 𝗣𝗘𝗣𝗦𝗜 𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗦𝗔𝗕𝗦𝗘 𝗦𝗘𝗫𝗬 💋💦",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔𝗞𝗢 𝗖𝗛𝗘𝗘𝗠𝗦 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗠𝗔𝗗𝗘𝗥𝗖𝗛𝗢𝗢𝗗 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦🤣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗗𝗘𝗦𝗜 𝗚𝗛𝗘𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗗𝗔𝗜 𝗙𝗥𝗬𝗘𝗥 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🍳🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗟𝗢𝗛𝗔 𝗚𝗔𝗟𝗔 𝗞𝗔𝗥 𝗧𝗔𝗝𝗠𝗛𝗔𝗟 𝗞𝗔 𝗡𝗔𝗬𝗔 𝗠𝗜𝗡𝗔𝗥 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🏰⚒️",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗖𝗛𝗢𝗖𝗢𝗟𝗔𝗧𝗘 𝗦𝗬𝗥𝗨𝗣 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗢𝗖𝗢𝗟𝗔𝗧𝗘 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗞𝗛𝗢𝗟 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🍫🏭",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗚𝗔𝗡𝗗 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗕𝗢𝗧𝗧𝗟𝗘 𝗖𝗢𝗖𝗔 𝗖𝗢𝗟𝗔 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗢𝗟𝗔 𝗩𝗢𝗟𝗖𝗔𝗡𝗢 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🥤🌋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝟱𝟬𝟬 𝗚𝗛𝗢𝗗𝗢𝗡 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔 𝗞𝗔𝗥 𝗛𝗢𝗥𝗦𝗘 𝗣𝗢𝗪𝗘𝗥 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗼𝗿 𝗕𝗻𝗮 𝗗𝗮𝗹𝘂𝗻𝗴𝗮 🐎⚡",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗕𝗔𝗟𝗟𝗦 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗕𝗢𝗪𝗟𝗜𝗡𝗚 𝗔𝗟𝗟𝗘𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🎳⚪",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬 𝗠𝗘𝗧𝗘𝗥 𝗚𝗔𝗛𝗥𝗔 𝗚𝗔𝗗𝗗𝗛𝗔 𝗚𝗔𝗗 𝗞𝗔𝗥 𝗣𝗔𝗡𝗜 𝗪𝗔𝗟𝗔 𝗞𝗨𝗔𝗔𝗡 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🕳️💧",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗖𝗛𝗜𝗖𝗞𝗘𝗡 𝗟𝗢𝗟𝗟𝗜𝗣𝗢𝗣 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗞𝗘𝗡𝗧𝗨𝗖𝗞𝗬 𝗙𝗥𝗜𝗘𝗗 𝗖𝗛𝗜𝗖𝗞𝗘𝗡 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🍗🍗",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗦𝗛𝗔𝗠𝗣𝗢𝗢 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗛𝗘𝗔𝗗 & 𝗦𝗛𝗢𝗨𝗟𝗗𝗘𝗥𝗦 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧴🏭",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗚𝗔𝗡𝗗 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗣𝗜𝗭𝗭𝗔 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗗𝗢𝗠𝗜𝗡𝗢𝗭 𝗣𝗜𝗭𝗭𝗔 𝗢𝗨𝗧𝗟𝗘𝗧 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🍕🍕",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟱𝟬𝟬 𝗠𝗘𝗧𝗘𝗥 𝗟𝗔𝗠𝗕𝗔 𝗖𝗛𝗜𝗥𝗔 𝗟𝗚𝗔 𝗞𝗔𝗥 𝗦𝗨𝗥𝗨𝗡𝗚 𝗠𝗘𝗜𝗡 𝗛𝗔𝗪𝗔 𝗗𝗔𝗟𝗘 𝗗𝗨𝗡𝗚𝗔 🌬️🌀",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗠𝗢𝗕𝗜𝗟𝗘 𝗖𝗛𝗔𝗥𝗚𝗘𝗥 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗣𝗢𝗪𝗘𝗥 𝗕𝗔𝗡𝗞 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🔋📱",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟱𝟬𝟬 𝗞𝗚 𝗣𝗔𝗡𝗘𝗘𝗥 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗣𝗔𝗡𝗘𝗘𝗥 𝗣𝗔𝗞𝗢𝗥𝗔 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧀🥘",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗧𝗢𝗢𝗧𝗛𝗣𝗔𝗦𝗧𝗘 𝗧𝗨𝗕𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗢𝗟𝗚𝗔𝗧𝗘 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🪥🏭",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗞𝗢 𝟭𝟬𝟬𝟬 𝗗𝗚𝗥𝗘𝗘 𝗣𝗘 𝗚𝗔𝗥𝗠 𝗞𝗥 𝗞𝗘 𝗧𝗔𝗧𝗔 𝗦𝗧𝗘𝗘𝗟 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗠𝗘𝗜𝗡 𝗣𝗜𝗚𝗛𝗟𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🔥🏭",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬𝟬 𝗕𝗔𝗥𝗙𝗜 𝗞𝗘 𝗧𝗨𝗞𝗗𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗞𝗨𝗟𝗙𝗜 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🍦🍨",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗧𝗘𝗥𝗘 𝗣𝗜𝗧𝗖𝗛 𝗗𝗥𝗔𝗜𝗩𝗘𝗥 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗠𝗨𝗠𝗕𝗔𝗜 𝗠𝗘𝗜𝗡 𝗦𝗣𝗔 𝗦𝗘𝗡𝗧𝗘𝗥 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 💆‍♀️💅",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗞𝗘𝗥𝗢𝗦𝗘𝗡𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗝𝗟𝗔𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🔥⛽",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗬𝗨𝗥𝗔𝗡𝗜𝗬𝗠 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗡𝗨𝗖𝗟𝗘𝗔𝗥 𝗥𝗘𝗔𝗖𝗧𝗢𝗥 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 ☢️💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗦𝗘 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗟𝗔𝗩𝗔 𝗡𝗜𝗞𝗔𝗟 𝗞𝗔𝗥 𝗩𝗢𝗟𝗖𝗔𝗡𝗢 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🌋🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗕𝗜𝗖𝗛𝗖𝗛𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗕𝗜𝗖𝗛𝗖𝗛𝗨 𝗙𝗔𝗥𝗠 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🦂🏜️",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗠𝗜𝗥𝗖𝗛𝗜 𝗣𝗔𝗪𝗗𝗘𝗥 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗠𝗜𝗥𝗖𝗛𝗜 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🌶️🏭",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗦𝗔𝗡𝗣 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗦𝗡𝗔𝗞𝗘 𝗣𝗔𝗥𝗞 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🐍🐍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗧𝗡𝗧 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗗𝗛𝗔𝗠𝗔𝗞𝗔 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 💣💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗘𝗦𝗜𝗗 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗚𝗛𝗢𝗟𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧪💀",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗖𝟰 𝗘𝗫𝗣𝗟𝗢𝗦𝗜𝗩𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗨𝗗𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 💥💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗚𝗔𝗦𝗢𝗟𝗜𝗡𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗔𝗚 𝗟𝗚𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🔥⛽",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗗𝗬𝗡𝗔𝗠𝗜𝗧𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗕𝗟𝗔𝗦𝗧 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 💣💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗛𝗬𝗗𝗥𝗢𝗚𝗘𝗡 𝗣𝗘𝗥𝗢𝗫𝗜𝗗𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗕𝗟𝗘𝗔𝗖𝗛 𝗞𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧪⚪",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗠𝗘𝗥𝗖𝗨𝗥𝗬 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗝𝗭𝗛𝗥 𝗕𝗛𝗥 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 ☠️💀",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗜𝗧𝗥𝗘 𝗖𝗛𝗟𝗢𝗥𝗜𝗡𝗘 𝗚𝗔𝗦 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗚𝗔𝗦 𝗖𝗛𝗔𝗠𝗕𝗘𝗥 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 ☠️💨",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟱𝟬𝟬 𝗞𝗚 𝗣𝗟𝗔𝗦𝗧𝗜𝗖 𝗘𝗫𝗣𝗟𝗢𝗦𝗜𝗩𝗘 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗣𝗟𝗔𝗦𝗧𝗜𝗖 𝗙𝗔𝗖𝗧𝗢𝗥𝗬 𝗕𝗡𝗔 𝗗𝗔𝗟𝗨𝗡𝗚𝗔 🧪🏭"
    "🤩💥🔥🔥uL   TERI MUMMY KI CHUT MEI TERE LAND KO DAL KE KAAT DUNGA MADARCHOD 🔪😂🔥",
    "u@   SUN TERI MAA KA BHOSDA AUR TERI BAHEN KA BHI BHOSDA 👿😎👊",
    "😍👊💥up   TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA UNKE NO BOLNE PE BHI LAND GHUSA DUNGA",
    "uW   TUJHE DEKH KE TERI RANDI BAHEN PE TARAS ATA HAI MUJHE BAHEN KE LODEEEE 👿💥🤩🔥",
    "TOHAR MUMMY KI CHUT MEI PURI KI PURI KINGFISHER KI BOTTLE DAL KE TOD DUNGA ANDER HI 😱😂🤩uY   TERI MAA KO ITNA CHODUNGA KI SAPNE MEI BHI MERI CHUDAI YAAD KAREGI RANDI",
    "uF   SUN MADARCHOD JYADA NA UCHAL MAA CHOD DENGE EK MIN MEI ✅🤣🔥🤩",
    "ui   APNI AMMA SE PUCHNA USKO US KAALI RAAT MEI KAUN CHODNEE AYA THAAA! TERE IS PAPA KA NAAM LEGI 😂👿😳",
    " TERI MAA KE BHOSDA ITNA CHODUNGA KI TU CAH KE BHI WO MAST CHUDAI SE DUR NHI JA PAYEGAA 😏😏🤩😍",
    "uV   TOHAR BAHIN CHODU BBAHEN KE LAWDE USME MITTI DAL KE CEMENT SE BHAR DU 🏠🤢🤩💥",
    "SUN BE RANDI KI AULAAD TU APNI BAHEN SE SEEKH KUCH KAISE GAAND MARWATE HAI😏🤬🔥💥",
    "u|   TUJHE AB TAK NAHI SMJH AYA KI MAI HI HU TUJHE PAIDA KARNE WALA BHOSDIKEE APNI MAA SE PUCH RANDI KE BACHEEEE 🤩👊👤😍",
    "uM   TERI MAA KE BHOSDE MEI SPOTIFY DAL KE LOFI BAJAUNGA DIN BHAR 😍🎶🎶💥",
    "JUNGLE ME NACHTA HE MORE TERI MAAKI CHUDAI DEKKE SAB BOLTE ONCE MORE ONCE MORE 🤣🤣💦💋�I   GALI GALI ME REHTA HE SAND TERI MAAKO CHOD DALA OR BANA DIA RAND 🤤🤣�",
    "NABE RANDIKE BACHHE AUKAT NHI HETO APNI RANDI MAAKO LEKE AAYA MATH KAR HAHAHAHA�;KIDZ MADARCHOD TERI MAAKO CHOD CHODKE TERR LIYE BHAI DEDIYA",
    "MAA KAA BJSODAAA� MADARXHODDDz TERIUUI MAAA KAA BHSODAAAz-TERIIIIII BEHENNNN KO CHODDDUUUU MADARXHODDDDz NIKAL MADARCHODz RANDI KE BACHEz TERA MAA MERI FANz TERI SEXY BAHEN KI CHUT",
    "BETE TU BAAP SE LEGA PANGA TERI MAAA KO CHOD DUNGA KARKE NANGA 💦💋",
    "CHAL BETA TUJHE MAAF KIA 🤣 ABB APNI GF KO BHEJ",
    "NSHARAM KAR TERI BEHEN KA BHOSDA KITNA GAALIA SUNWAYEGA APNI MAAA BEHEN KE UPER�NABE RANDIKE BACHHE AUKAT NHI HETO APNI RANDI MAAKO LEKE AAYA MATH KAR HAHAHAHA",
    "TERE BEHEN K CHUT ME CHAKU DAAL KAR CHUT KA KHOON KAR DUGAuF   TERI VAHEEN NHI HAI KYA? 9 MAHINE RUK SAGI VAHEEN DETA HU 🤣🤣🤩uC   TERI MAA K BHOSDE ME AEROPLANEPARK KARKE UDAAN BHAR DUGA ✈️🛫uV   TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI💣",
    "uE   TERI MAA KA NAYA RANDI KHANA KHOLUNGA CHINTA MAT KAR 👊🤣🤣😳",
    "ub   TERA BAAP HU BHOSDIKE TERI MAA KO RANDI KHANE PE CHUDWA KE US PAISE KI DAARU PEETA HU 🍷🤩🔥",
    "u]   TERI BAHEN KI CHUT MEI APNA BADA SA LODA GHUSSA DUNGAA KALLAAP KE MAR JAYEGI 🤩😳😳🔥",
    "u   TOHAR MUMMY KI CHUT MEI PURI KI PURI KINGFISHER KI BOTTLE DAL KE TOD DUNGA ANDER HI 😱😂🤩",
    "uY   TERI MAA KO ITNA CHODUNGA KI SAPNE MEI BHI MERI CHUDAI YAAD KAREGI RANDI 🥳😍👊💥",
    "up   TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA UNKE NO BOLNE PE BHI LAND GHUSA DUNGA ANDER TAK 😎😎🤣🔥",
    "ui   TERI MUMMY KI CHUT KO ONLINE OLX PE BECHUNGA AUR PAISE SE TERI BAHEN KA KOTHA KHOL DUNGA 😎🤩😝😍",
    "ug   TERI MAA KE BHOSDA ITNA CHODUNGA KI TU CAH KE BHI WO MAST CHUDAI SE DUR NHI JA PAYEGAA 😏😏🤩😍",
    "uZ   SUN BE RANDI KI AULAAD TU APNI BAHEN SE SEEKH KUCH KAISE GAAND MARWATE HAI😏🤬🔥💥",
    "uZ   TERI MAA KA YAAR HU MEI AUR TERI BAHEN KA PYAAR HU MEI AJA MERA LAND CHOOS LE 🤩🤣💥",
    "u,   TERI BEHN KI CHUT ME KELE KE CHILKE 🤤🤤",
    "uZ   TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI💣💋"
    "TᏒᎥᎥᎥᎥᎥᎥᎥᎥᎥ mᎪᎪᎪᎪᎪ ᏦᎥᎥᎥᎥᎥᎥ xhuҬҬҬҬҬҬҬ ᎶᎪᏒᎪᎪm hᎪᎪᎪᎥ ᏒᎪᏁᎠᎥ 🤣😂︵‿︵‿︵‿︵‿︵‿█▄▄ ███ █▄▄♥️╣[-_-]╠♥️👅👅",
    "MADARCHOD.", "BENCHOD.", "DAFAN HOJA RANDI KE BACCHE.", "TU CHAKKA HAI.",
    "TERI MAA KO CHODUNGA.", "BHAG BE RANDI KE.", "TERI BEHEN KO BHI  CHHODUNGA.",
    "BHOSDIKE.", "RANDI KE PILLE.", "CHUTIYA.", "TERI MAA BEHEN EK KAR DUNGA.",
    "MUH MEIN LE MADARCHOD.", "DALLA HAI TU.", "RAPCHOD.", "LAND KA KIRAYEDAR.",
    "SPEED PAKAD BE.", "GANDU.", "TERA KHANDAN GB ROAD KA.", "CHAKKE KI AULAD.",
    "BAP SE LADEGA?", "TERI MAA RANDI."
    "🤬 Oye circuit ke reject version!",
    "😡 Tere jaise logon ke wajah se WiFi password badalte hain!",
    "👎 Tera sense of humor Windows error jaisa hai!",
    "GALI GALI NE SHOR HE TERI MAA RANDI CHOR HE 💋💋💦"
    "TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI💣💋",
    "TERI MAA KI GAAND ME SARIYA DAAL DUNGA MADARCHOD USI SARIYE PR TANG KE BACHE PAIDA HONGE 😱😱",
    "TERI MUMMY KI FANTASY HU LAWDE, TU APNI BHEN KO SMBHAAL 😈😈",
    "ERI MAA KI GAAND ME SARIYA DAAL DUNGA MADARCHOD USI SARIYE PR TANG KE BACHE PAIDA HONGE 😱😱",
    "TERI MAA KE GAAND MEI JHAADU DAL KE MOR 🦚 BANA DUNGAA 🤩🥵😱",
    "TERI MUMMY KI FANTASY HU LAWDE, TU APNI BHEN KO SMBHAAL 😈😈",
    "TERI MAA KA YAAR HU MEI AUR TERI BAHEN KA PYAAR HU MEI AJA MERA LAND CHOOS LE 🤩🤣💥",
    " TERI MAAKI CHUTH FAADKE RAKDIA MAAKE LODE JAA ABB SILWALE 👄👄",
    "TERI BHEN KI CHUT ME USERBOT LAGAAUNGA SASTE SPAM KE CHODE",
    "TERI BHEN KI CHUT ME USERBOT LAGAAUNGA SASTE SPAM KE CHODE",
    "GALI GALI ME REHTA HE SAND TERI MAAKO CHOD DALA OR BANA DIA RAND 🤤",
    "HAHAHAHA BACHHE TERI MAAAKO CHOD DIA NANGA KARKE",
    "TERI MAA KI CHUT MEI C++ STRING ENCRYPTION LAGA DUNGA BAHTI HUYI CHUT RUK JAYEGIIII😈🔥😍",
    "TERI RANDI MAA SE PUCHNA BAAP KA NAAM BAHEN KE LODEEEEE 🤩🥳😳",
    "TU AUR TERI MAA DONO KI BHOSDE MEI METRO CHALWA DUNGA MADARXHOD 🚇🤩😱🥶", 
    "TERI MAUSI KE BHOSDE MEI INDIAN RAILWAY 🚂💥😂",
    "TERA BAAP HU BHOSDIKE TERI MAA KO RANDI KHANE PE CHUDWA KE US PAISE KI DAARU PEETA HU 🍷🤩🔥",
    "MADARCHOD FIGHT KARE GA TERII MAAAA KAAAA BHOSDAAAAAAAA MAROOOOOOOOOO RANDIIIIIIIII KA PILLLLAAAAAAAAAAAAAAAAAAAAAA",
    "TERIIIIIIII MAAAAAAA KIIIIIIIIIII CHUTTTTTTTTTTTTTTTTTT",
    "BOSDKIIIIIIIIIIIIIIIIIIIIIIII MADARCHODDDDDDDDDDDDDDDDDDD",
    "TERI MAA KI CHUT ME CHANGES COMMIT KRUGA FIR TERI BHEEN KI CHUT AUTOMATICALLY UPDATE HOJAAYEGI🤖🙏🤔",
    "UTT JA MADARCHOD",
    "MUH MEIN LE LEEEE MERA LODAAAAAAAAAAAAAA ",
    "KHA GYA RE MADARCHOD",
    "MADARCHOD.", "BENCHOD.", "DAFAN HOJA RANDI KE BACCHE.", "TU CHAKKA HAI.",
    "TERI MAA KO CHODUNGA.", "BHAG BE RANDI KE.", "TERI BEHEN KO BHI  CHHODUNGA.",
    "BHOSDIKE.", "RANDI KE PILLE.", "CHUTIYA.", "TERI MAA BEHEN EK KAR DUNGA.",
    "MUH MEIN LE MADARCHOD.", "DALLA HAI TU.", "RAPCHOD.", "LAND KA KIRAYEDAR.",
    "SPEED PAKAD BE.", "GANDU.", "TERA KHANDAN GB ROAD KA.", "CHAKKE KI AULAD.",
    "BAP SE LADEGA?", "TERI MAA RANDI."
    "TERI TMKCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "BAPPPPPPPPPPPPPP HU MEIN TERAAAAAAAAAAAA",
    "TERE GAND FAT GYI MEINNE DEK LE ",
    "TERREEEEEEEEEEE MUH MEIN MERAAAAAAAAA LODAAAAAAAAAAAA",
    "TERI MAA KA NAYA RANDI KHANA KHOLUNGA CHINTA MAT KAR 👊🤣🤣😳",
    "CHAKKAAAAAAAAAAAAAAA HAI TUUUUUUUUUUUUUUUUUUUU BSDKKKKKKKKKKKKKKKK",
    "TᏒᎥᎥᎥᎥᎥᎥᎥᎥᎥ mᎪᎪᎪᎪᎪ ᏦᎥᎥᎥᎥᎥᎥ xhuҬҬҬҬҬҬҬ ᎶᎪᏒᎪᎪm hᎪᎪᎪᎥ ᏒᎪᏁᎠᎥ 🤣😂��‿︵‿︵‿︵‿︵‿█▄▄ ███ █▄▄♥️╣[-_-]╠♥️👅👅",
    "🤬 Oye circuit ke reject version!",
    "😡 Tere jaise logon ke wajah se WiFi password badalte hain!",
    "👎 Tera sense of humor Windows error jaisa hai!",
    "GALI GALI NE SHOR HE TERI MAA RANDI CHOR HE 💋💋💦"
    "TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI💣💋",
    "TERI MAA KI GAAND ME SARIYA DAAL DUNGA MADARCHOD USI SARIYE PR TANG KE BACHE PAIDA HONGE 😱😱",
    "TERI MUMMY KI FANTASY HU LAWDE, TU APNI BHEN KO SMBHAAL 😈😈",
    "ERI MAA KI GAAND ME SARIYA DAAL DUNGA MADARCHOD USI SARIYE PR TANG KE BACHE PAIDA HONGE 😱😱",
    "TERI MAA KE GAAND MEI JHAADU DAL KE MOR 🦚 BANA DUNGAA 🤩🥵😱",
    "TERI MUMMY KI FANTASY HU LAWDE, TU APNI BHEN KO SMBHAAL 😈😈",
    "TERI MAA KA YAAR HU MEI AUR TERI BAHEN KA PYAAR HU MEI AJA MERA LAND CHOOS LE 🤩🤣💥",
    " TERI MAAKI CHUTH FAADKE RAKDIA MAAKE LODE JAA ABB SILWALE 👄👄",
    "TERI BHEN KI CHUT ME USERBOT LAGAAUNGA SASTE SPAM KE CHODE",
    "TERI BHEN KI CHUT ME USERBOT LAGAAUNGA SASTE SPAM KE CHODE",
    "GALI GALI ME REHTA HE SAND TERI MAAKO CHOD DALA OR BANA DIA RAND 🤤",
    "HAHAHAHA BACHHE TERI MAAAKO CHOD DIA NANGA KARKE",
    "TERI MAA KI CHUT MEI C++ STRING ENCRYPTION LAGA DUNGA BAHTI HUYI CHUT RUK JAYEGIIII😈🔥😍",
    "TERI RANDI MAA SE PUCHNA BAAP KA NAAM BAHEN KE LODEEEEE 🤩🥳😳",
    "TU AUR TERI MAA DONO KI BHOSDE MEI METRO CHALWA DUNGA MADARXHOD 🚇🤩😱🥶", 
    "TERI MAUSI KE BHOSDE MEI INDIAN RAILWAY 🚂💥😂",
    "TERA BAAP HU BHOSDIKE TERI MAA KO RANDI KHANE PE CHUDWA KE US PAISE KI DAARU PEETA HU 🍷🤩🔥",
    "MADARCHOD FIGHT KARE GA TERII MAAAA KAAAA BHOSDAAAAAAAA MAROOOOOOOOOO RANDIIIIIIIII KA PILLLLAAAAAAAAAAAAAAAAAAAAAA",
    "TERIIIIIIII MAAAAAAA KIIIIIIIIIII CHUTTTTTTTTTTTTTTTTTT",
    "BOSDKIIIIIIIIIIIIIIIIIIIIIIII MADARCHODDDDDDDDDDDDDDDDDDD",
    "TERI MAA KI CHUT ME CHANGES COMMIT KRUGA FIR TERI BHEEN KI CHUT AUTOMATICALLY UPDATE HOJAAYEGI🤖🙏🤔",
    "UTT JA MADARCHOD",
    "MUH MEIN LE LEEEE MERA LODAAAAAAAAAAAAAA ",
    "KHA GYA RE MADARCHOD",
    "MADARCHOD.", "BENCHOD.", "DAFAN HOJA RANDI KE BACCHE.", "TU CHAKKA HAI.",
    "TERI MAA KO CHODUNGA.", "BHAG BE RANDI KE.", "TERI BEHEN KO BHI  CHHODUNGA.",
    "BHOSDIKE.", "RANDI KE PILLE.", "CHUTIYA.", "TERI MAA BEHEN EK KAR DUNGA.",
    "MUH MEIN LE MADARCHOD.", "DALLA HAI TU.", "RAPCHOD.", "LAND KA KIRAYEDAR.",
    "SPEED PAKAD BE.", "GANDU.", "TERA KHANDAN GB ROAD KA.", "CHAKKE KI AULAD.",
    "TOHAR MUMMY KI CHUT MEI PURI KI PURI KINGFISHER KI BOTTLE DAL KE TOD DUNGA ANDER HI 😱😂🤩uY",   
    "TERI MAA KO ITNA CHODUNGA KI SAPNE MEI BHI MERI CHUDAI YAAD KAREGI RANDI 🥳😍👊💥up",   
    "TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA UNKE NO BOLNE PE BHI LAND GHUSA DUNGA ANDER TAK 😎😎🤣🔥ui",   
    "TERI MUMMY KI CHUT KO ONLINE OLX PE BECHUNGA AUR PAISE SE TERI BAHEN KA KOTHA KHOL DUNGA 😎🤩😝😍ug",  
    "TERI MAA KE BHOSDA ITNA CHODUNGA KI TU CAH KE BHI WO MAST CHUDAI SE DUR NHI JA PAYEGAA 😏😏🤩😍uZ",  
    "SUN BE RANDI KI AULAAD TU APNI BAHEN SE SEEKH KUCH KAISE GAAND MARWATE HAI😏🤬🔥💥uZ",   
    "TERI MAA KA YAAR HU MEI AUR TERI BAHEN KA PYAAR HU MEI AJA MERA LAND CHOOS LE 🤩🤣💥r    r    r    u",   
    "TERI BEHN KI CHUT ME KELE KE CHILKE 🤤🤤uZ",   
    "TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI💣💋u6",   
    "TERI VAHEEN KO HORLICKS PEELAKE CHODUNGA MADARCHOD😚U",   
    "TERI VAHEEN KO APNE LUND PR ITNA JHULAAUNGA KI JHULTE JHULTE HI BACHA PAIDA KR DEGI 💦💋",
    "�@   SUAR KE PILLE TERI MAAKO SADAK PR LITAKE CHOD DUNGA 😂😆🤤",
    "�H   ABE TERI MAAKA BHOSDA MADERCHOOD KR PILLE PAPA SE LADEGA TU 😼😂🤤",
    "�8   GALI GALI NE SHOR HE TERI MAA RANDI CHOR HE 💋💋💦",
    "�A   ABE TERI BEHEN KO CHODU RANDIKE PILLE KUTTE KE CHODE 😂👻🔥",
    "�M   TERI MAAKO AISE CHODA AISE CHODA TERI MAAA BED PEHI MUTH DIA 💦💦💦💦",
    "�N   TERI BEHEN KE BHOSDE ME AAAG LAGADIA MERA MOTA LUND DALKE 🔥🔥💦😆😆",
    "�*RANDIKE BACHHE TERI MAAKO CHODU CHAL NIKAL�F",   
    "KITNA CHODU TERI RANDI MAAKI CHUTH ABB APNI BEHEN KO BHEJ 😆👻🤤�P",   
    "TERI BEHEN KOTO CHOD CHODKE PURA FAAD DIA CHUTH ABB TERI GF KO BHEJ 😆💦🤤�}",   
    "TERI GF KO ETNA CHODA BEHEN KE LODE TERI GF TO MERI RANDI BANGAYI ABB CHAL TERI MAAKO CHODTA FIRSE ♥️💦😆😆😆😆�<",   
    "HARI HARI GHAAS ME JHOPDA TERI MAAKA BHOSDA 🤣🤣💋💦�:", 
    "CHAL TERE BAAP KO BHEJ TERA BASKA NHI HE PAPA SE LADEGA TU�7",
    "TERI BEHEN KI CHUTH ME BOMB DALKE UDA DUNGA MAAKE LAWDE�V",  
    "TERI MAAKO TRAIN ME LEJAKE TOP BED PE LITAKE CHOD DUNGA SUAR KE PILLE 🤣🤣💋💋�D",   
    "TERI MAAAKE NUDES GOOGLE PE UPLOAD KARDUNGA BEHEN KE LAEWDE 👻🔥r    �Z",   
    "TERI BEHEN KO CHOD CHODKE VIDEO BANAKE XNXX.COM PE NEELAM KARDUNGA KUTTE KE PILLE 💦💋�O",   
    "TERI MAAAKI CHUDAI KO PORNHUB.COM PE UPLOAD KARDUNGA SUAR KE CHODE 🤣💋💦�Z",   
    "ABE TERI BEHEN KO CHODU RANDIKE BACHHE TEREKO CHAKKO SE PILWAVUNGA RANDIKE BACHHE 🤣🤣�B",  
    "TERI MAAKI CHUTH FAADKE RAKDIA MAAKE LODE JAA ABB SILWALE 👄👄�&TERI BEHEN KI CHUTH ME MERA LUND KAALA�S",
    "TERI BEHEN LETI MERI LUND BADE MASTI SE TERI BEHEN KO MENE CHOD DALA BOHOT SASTE SE�G",   
    "BETE TU BAAP SE LEGA PANGA TERI MAAA KO CHOD DUNGA KARKE NANGA 💦💋�",
    "BAP SE LADEGA?", "TERI MAA RANDI."
    "TERI TMKCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "BAPPPPPPPPPPPPPP HU MEIN TERAAAAAAAAAAAA",
    "TERE GAND FAT GYI MEINNE DEK LE ",
    "TERREEEEEEEEEEE MUH MEIN MERAAAAAAAAA LODAAAAAAAAAAAA",
    "TERI MAA KA NAYA RANDI KHANA KHOLUNGA CHINTA MAT KAR 👊🤣🤣😳",
    "CHAKKAAAAAAAAAAAAAAA HAI TUUUUUUUUUUUUUUUUUUUU BSDKKKKKKKKKKKKKKKK",
    "TOHAR MUMMY KI CHUT MEI PURI KI PURI KINGFISHER KI BOTTLE DAL KE TOD DUNGA ANDER HI 😱😂🤩uY", 
    "TERI MAA KO ITNA CHODUNGA KI SAPNE MEI BHI MERI CHUDAI YAAD KAREGI RANDI 🥳😍👊💥up",
   "TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA",
   "UNKE NO BOLNE PE BHI LAND GHUSA DUNGA ANDER TAK 😎😎🤣",
   "SUAR KE PILLE TERI MAAKO SADAK PR LITAKE CHOD DUNGA 😂😆🤤",
   "TERI ITEM KI GAAND ME LUND DAALKE,TERE JAISA EK OR NIKAAL DUNGA MADARCHOD🤘🏻🙌🏻☠️ uh",   
   "AUKAAT ME REH VRNA GAAND ME DANDA DAAL KE MUH SE NIKAAL DUNGA SHARIR BHI DANDE JESA DIKHEGA 🙄🤭🤭uW",   
   "TERI MUMMY KE SAATH LUDO KHELTE KHELTE USKE MUH ME APNA LODA DE DUNGA☝🏻☝🏻😬u",   
   "TERI VAHEEN KO APNE LUND PR ITNA JHULAAUNGA KI JHULTE JHULTE HI BACHA PAIDA KR DEGI👀👯 uG",   
   "TERI MAA KI CHUT MEI BATTERY LAGA KE POWERBANK BANA DUNGA 🔋 🔥🤩u_",   
   "TERI MAA KI CHUT MEI C++ STRING ENCRYPTION LAGA DUNGA BAHTI HUYI CHUT RUK JAYEGIIII😈🔥😍uE",   
   "TERI MAA KE GAAND MEI JHAADU DAL KE MOR 🦚 BANA DUNGAA 🤩🥵😱uT",   
   "TERI CHUT KI CHUT MEI SHOULDERING KAR DUNGAA HILATE HUYE BHI DARD HOGAAA😱🤮👺uF",
   "TERI MAA KO REDI PE BAITHAL KE USSE USKI CHUT BILWAUNGAA 💰 😵🤩ub",   
   "BHOSDIKE TERI MAA KI CHUT MEI 4 HOLE HAI UNME MSEAL LAGA BAHUT BAHETI HAI BHOFDIKE👊🤮🤢🤢u_",   
   "TERI BAHEN KI CHUT MEI BARGAD KA PED UGA DUNGAA CORONA MEI SAB OXYGEN LEKAR JAYENGE🤢🤩🥳uQ",   
   "TERI MAA KI CHUT MEI SUDO LAGA KE BIGSPAM LAGA KE 9999 FUCK LAGAA DU 🤩🥳🔥uD",   
   "TERI VAHEN KE BHOSDIKE MEI BESAN KE LADDU BHAR DUNGA🤩🥳🔥😈u",
   "TᏒᎥᎥᎥᎥᎥᎥᎥᎥᎥ mᎪᎪᎪᎪᎪ ᏦᎥᎥᎥᎥᎥᎥ xhuҬҬҬҬҬҬҬ ᎶᎪᏒᎪᎪm hᎪᎪᎪᎥ ᏒᎪᏁᎠᎥ 🤣😂︵‿︵‿︵‿︵‿︵‿█▄▄ ███ █▄▄♥️╣[-_-]╠♥️👅👅"
]

single_raid_msg = abuse_roast.copy()

# ==================== GLOBAL STATE ====================
clients = {}
delays = {}
rr_targets = {}
rr_counts = {}
raid_tasks = {}
fr_active = {}
fr_target_chat = {}
fr_target_msg_id = {}
fr_user_ids = {}
fr_full_text = {}
fr_mentions_list = {}
cs_active = {}
cs_auto_reply = {}
last_message_time = {}
start_time = datetime.now()
shutdown_flag = False
name_cache = {}

# ==================== HELPER FUNCTIONS ====================
def get_owner_by_index(index):
    if index < len(SESSIONS):
        return SESSIONS[index].get("owner")
    return None

def is_authorized(session_index, user_id):
    user_id = int(user_id)
    if user_id == MAIN_OWNER:
        return True
    if user_id in GLOBAL_SUDO_USERS:
        return True
    if user_id == get_owner_by_index(session_index):
        return True
    return False

async def anti_flood_wait(session_index):
    current_time = time.time()
    last_time = last_message_time.get(session_index, 0)
    time_diff = current_time - last_time
    
    if time_diff < 0.3:
        wait_time = random.uniform(2, 3)
        await asyncio.sleep(wait_time)
    
    last_message_time[session_index] = time.time()

async def get_user_real_name(client, user_id):
    """Get user's real name - aggressive fetching with multiple methods"""
    user_id = int(user_id)
    
    # Check cache
    if user_id in name_cache:
        return name_cache[user_id]
    
    name = None
    
    # METHOD 1: Try get_entity
    try:
        user = await client.get_entity(user_id)
        if user.first_name:
            name = user.first_name
        elif user.last_name:
            name = user.last_name
        elif user.username:
            name = f"@{user.username}"
    except:
        pass
    
    # METHOD 2: Try GetFullUserRequest
    if not name:
        try:
            full_user = await client(GetFullUserRequest(user_id))
            if full_user.user.first_name:
                name = full_user.user.first_name
            elif full_user.user.last_name:
                name = full_user.user.last_name
            elif full_user.user.username:
                name = f"@{full_user.user.username}"
        except:
            pass
    
    # METHOD 3: Try from dialogs
    if not name:
        try:
            async for dialog in client.iter_dialogs():
                if dialog.entity and hasattr(dialog.entity, 'id') and dialog.entity.id == user_id:
                    if hasattr(dialog.entity, 'first_name') and dialog.entity.first_name:
                        name = dialog.entity.first_name
                        break
                    elif hasattr(dialog.entity, 'title'):
                        name = dialog.entity.title
                        break
        except:
            pass
    
    # METHOD 4: Try from message history
    if not name:
        try:
            async for msg in client.iter_messages(None, from_user=user_id, limit=1):
                if msg.sender and msg.sender.first_name:
                    name = msg.sender.first_name
                    break
        except:
            pass
    
    # METHOD 5: Try to find in common groups
    if not name:
        try:
            async for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    try:
                        async for user in client.iter_participants(dialog.entity):
                            if user.id == user_id:
                                if user.first_name:
                                    name = user.first_name
                                elif user.last_name:
                                    name = user.last_name
                                break
                        if name:
                            break
                    except:
                        pass
        except:
            pass
    
    # Fallback: use ID as name (but still clickable)
    if not name:
        name = str(user_id)
    
    # Clean name
    name = re.sub(r'[\[\]\(\)\_\*\`\~\#\@]', '', name)
    if not name or name == "":
        name = str(user_id)
    
    # Cache it
    name_cache[user_id] = name
    return name

def make_clickable_mention(name, user_id):
    """Create clickable mention with tg://openmessage?user_id= format"""
    return f'<a href="tg://openmessage?user_id={user_id}">{name}</a>'

async def send_bulk_clickable_mentions(client, chat_id, user_ids, message_text, reply_to=None):
    """Send message with multiple CLICKABLE mentions - ALWAYS shows something clickable"""
    try:
        mentions = []
        for uid in user_ids:
            name = await get_user_real_name(client, uid)
            mentions.append(make_clickable_mention(name, uid))
        
        final_text = f"{message_text}\n\n{' '.join(mentions)}"
        
        if reply_to:
            await client.send_message(chat_id, final_text, parse_mode='html', reply_to=reply_to)
        else:
            await client.send_message(chat_id, final_text, parse_mode='html')
    except Exception as e:
        # Ultimate fallback - send IDs as clickable
        try:
            fallback_mentions = [make_clickable_mention(str(uid), uid) for uid in user_ids]
            final_text = f"{message_text}\n\n{' '.join(fallback_mentions)}"
            if reply_to:
                await client.send_message(chat_id, final_text, parse_mode='html', reply_to=reply_to)
            else:
                await client.send_message(chat_id, final_text, parse_mode='html')
        except:
            pass

async def delete_msg(msg):
    try:
        await msg.delete()
    except:
        pass

async def delete_msg_delay(msg, delay):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

async def safe_reply(event, text, delay=1):
    try:
        msg = await event.reply(text, parse_mode='html')
        asyncio.create_task(delete_msg_delay(msg, delay))
        return msg
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        msg = await event.reply(text, parse_mode='html')
        asyncio.create_task(delete_msg_delay(msg, delay))
        return msg
    except:
        return None

def get_uptime():
    uptime_sec = (datetime.now() - start_time).total_seconds()
    days = int(uptime_sec // 86400)
    hours = int((uptime_sec % 86400) // 3600)
    minutes = int((uptime_sec % 3600) // 60)
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

async def join_channel_with_discussion(client, target):
    try:
        from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
        from telethon.tl.functions.messages import ImportChatInviteRequest
        
        if 't.me/+' in target or 't.me/joinchat/' in target:
            hash_part = target.split('/')[-1].replace('+', '')
            await client(ImportChatInviteRequest(hash_part))
            return True, None, None
        else:
            entity = await client.get_entity(target)
            await client(JoinChannelRequest(entity))
            discussion_joined = False
            try:
                full = await client(GetFullChannelRequest(entity))
                if hasattr(full.full_chat, 'linked_chat_id') and full.full_chat.linked_chat_id:
                    try:
                        disc_entity = await client.get_entity(full.full_chat.linked_chat_id)
                        await client(JoinChannelRequest(disc_entity))
                        discussion_joined = True
                    except:
                        pass
            except:
                pass
            return True, discussion_joined, None
    except:
        return False, None, None

async def leave_channel(client, target):
    try:
        from telethon.tl.functions.channels import LeaveChannelRequest
        
        if target.isdigit():
            entity = await client.get_entity(int(target))
        else:
            entity = await client.get_entity(target)
        await client(LeaveChannelRequest(entity))
        return True, None
    except:
        return False, None

def stop_all_operations():
    for idx in list(clients.keys()):
        fr_active[idx] = False
        cs_active[idx] = False
        raid_tasks[idx] = False
        rr_targets[idx] = None
        if idx in rr_counts:
            rr_counts[idx] = {}
        if idx in cs_auto_reply:
            cs_auto_reply[idx] = {}
        if idx in fr_mentions_list:
            fr_mentions_list[idx] = []
        if idx in fr_user_ids:
            fr_user_ids[idx] = []

async def graceful_shutdown():
    global shutdown_flag
    shutdown_flag = True
    stop_all_operations()
    await asyncio.sleep(0.3)
    for idx, client in list(clients.items()):
        try:
            if client.is_connected():
                await client.disconnect()
        except:
            pass

# ==================== START SESSIONS ====================
async def start_sessions():
    for idx, data in enumerate(SESSIONS):
        session_str = data.get("session_string")
        if session_str:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            try:
                await client.start()
                me = await client.get_me()
                clients[idx] = client
                delays[idx] = 0.3
                rr_targets[idx] = None
                rr_counts[idx] = {}
                raid_tasks[idx] = False
                fr_active[idx] = False
                fr_target_chat[idx] = None
                fr_target_msg_id[idx] = None
                fr_user_ids[idx] = []
                fr_full_text[idx] = ""
                fr_mentions_list[idx] = []
                cs_active[idx] = False
                cs_auto_reply[idx] = {}
                last_message_time[idx] = 0
                
                print(f"[✓] Session {idx} (@{me.username or me.first_name}) | Owner: {data.get('owner')}")
                
                try:
                    if AUTO_JOIN_LINK:
                        await join_channel_with_discussion(client, AUTO_JOIN_LINK)
                        print(f"  └─ ✅ Auto-joined")
                except:
                    pass
                
                register_handlers(client, idx)
                
            except Exception as e:
                print(f"[✗] Session {idx} failed: {e}")

# ==================== HANDLERS ====================
def register_handlers(client, session_index):
    
    @client.on(events.NewMessage(pattern=r'^\.start$'))
    async def start_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        await safe_reply(event, "✅ <b>USERBOT ACTIVATED!</b>\n⚡ Speed: 0.3s\n🔥 Flood Protected\n📌 .help for commands", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.over$'))
    async def over_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        stop_all_operations()
        await safe_reply(event, "🛑 <b>ALL OPERATIONS STOPPED!</b>", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.ping$'))
    async def ping_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        start = time.time()
        msg = await event.reply("⚡")
        end = time.time()
        ping = int((end - start) * 1000)
        try:
            await msg.edit(f"⚡ <code>{ping}ms</code> | Speed: <code>{delays[session_index]}s</code>", parse_mode='html')
        except:
            pass
        asyncio.create_task(delete_msg_delay(msg, 5))
    
    @client.on(events.NewMessage(pattern=r'^\.stats$'))
    async def stats_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        ram_used = psutil.virtual_memory().used / (1024 ** 3)
        ram_total = psutil.virtual_memory().total / (1024 ** 3)
        uptime = get_uptime()
        await safe_reply(event, f"📊 <b>STATS</b>\n├ CPU: <code>{cpu}%</code>\n├ RAM: <code>{ram}%</code> ({ram_used:.1f}/{ram_total:.1f}GB)\n├ Uptime: <code>{uptime}</code>\n└ Speed: <code>{delays[session_index]}s</code>", 3)
    
    @client.on(events.NewMessage(pattern=r'^\.dly (\d+\.?\d*)$'))
    async def speed_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        dly = float(event.pattern_match.group(1))
        if dly < 0.1:
            dly = 0.1
        if dly > 10:
            dly = 10
        delays[session_index] = dly
        await safe_reply(event, f"⚡ Speed set to: <code>{dly}s</code>", 1)
    
    # ==================== .join ====================
    @client.on(events.NewMessage(pattern=r'^\.join (.+)$'))
    async def join_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        target = event.pattern_match.group(1).strip()
        msg = await event.reply(f"🔄 Joining...")
        
        success = 0
        fail = 0
        
        for idx, c in clients.items():
            success_join, _, _ = await join_channel_with_discussion(c, target)
            if success_join:
                success += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)
        try:
            await msg.edit(f"✅ Joined: <code>{success}</code>\n❌ Failed: <code>{fail}</code>", parse_mode='html')
        except:
            pass
        asyncio.create_task(delete_msg_delay(msg, 5))
    
    # ==================== .joinleft ====================
    @client.on(events.NewMessage(pattern=r'^\.joinleft (.+)$'))
    async def joinleft_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        target = event.pattern_match.group(1).strip()
        msg = await event.reply(f"🚪 Leaving...")
        
        success = 0
        fail = 0
        
        for idx, c in clients.items():
            success_leave, _ = await leave_channel(c, target)
            if success_leave:
                success += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)
        
        try:
            await msg.edit(f"✅ Left: <code>{success}</code>\n❌ Failed: <code>{fail}</code>", parse_mode='html')
        except:
            pass
        asyncio.create_task(delete_msg_delay(msg, 5))
    
    # ==================== .rr (Reply Raid) ====================
    @client.on(events.NewMessage(pattern=r'^\.rr(\d+)?(?:\s+(.+))?$'))
    async def rr_cmd_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        count = 5
        match = re.match(r'\.rr(\d+)', event.raw_text)
        if match:
            count = int(match.group(1))
            if count > 100:
                count = 100
        
        target_users = []
        
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            if reply and reply.sender_id:
                target_users = [reply.sender_id]
        else:
            parts = event.raw_text.split()
            if len(parts) > 1:
                for arg in parts[1:]:
                    if arg.isdigit():
                        target_users.append(int(arg))
                    elif arg.startswith('@'):
                        try:
                            entity = await client.get_entity(arg)
                            target_users.append(entity.id)
                        except:
                            pass
        
        if not target_users:
            await safe_reply(event, "❌ <b>Usage:</b> <code>.rr5 @username</code> or reply", 2)
            return
        
        if session_index not in rr_counts:
            rr_counts[session_index] = {}
        for uid in target_users:
            rr_counts[session_index][uid] = count
        rr_targets[session_index] = target_users
        
        await safe_reply(event, f"🎯 <b>RR{count} ACTIVATED!</b>\n👥 {len(target_users)} target(s)", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.stoprr$'))
    async def stoprr_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        rr_targets[session_index] = None
        if session_index in rr_counts:
            rr_counts[session_index] = {}
        await safe_reply(event, "✅ <b>RR Stopped!</b>", 1)
    
    # RR Listener
    @client.on(events.NewMessage(incoming=True))
    async def rr_listener(event):
        if shutdown_flag:
            return
        targets = rr_targets.get(session_index)
        if not targets:
            return
        
        sender = event.sender_id
        if not sender:
            return
        
        if sender in targets:
            count = rr_counts.get(session_index, {}).get(sender, 0)
            if count > 0:
                rr_counts[session_index][sender] = count - 1
                if rr_counts[session_index][sender] <= 0:
                    del rr_counts[session_index][sender]
                
                try:
                    await anti_flood_wait(session_index)
                    roast = random.choice(abuse_roast)
                    name = await get_user_real_name(client, sender)
                    mention = make_clickable_mention(name, sender)
                    await event.reply(f"{mention} {roast}", parse_mode='html')
                    await asyncio.sleep(delays.get(session_index, 0.3))
                except:
                    pass
    
    # ==================== .ra ====================
    @client.on(events.NewMessage(pattern=r'^\.ra(?:\s+(.+))?$'))
    async def ra_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        target = None
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            if reply and reply.sender_id:
                target = reply.sender_id
        elif event.pattern_match.group(1):
            arg = event.pattern_match.group(1).strip()
            if arg.isdigit():
                target = int(arg)
            elif arg.startswith('@'):
                try:
                    entity = await client.get_entity(arg)
                    target = entity.id
                except:
                    pass
        
        if not target:
            await safe_reply(event, "❌ <code>.ra @username</code> or reply", 2)
            return
        
        raid_tasks[session_index] = True
        name = await get_user_real_name(client, target)
        mention = make_clickable_mention(name, target)
        
        async def raid_loop():
            while raid_tasks.get(session_index, False) and not shutdown_flag:
                try:
                    await anti_flood_wait(session_index)
                    roast = random.choice(abuse_roast)
                    await event.respond(f"{mention} {roast}", parse_mode='html')
                    await asyncio.sleep(delays.get(session_index, 0.3))
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds + 2)
                except:
                    await asyncio.sleep(1)
        
        asyncio.create_task(raid_loop())
        await safe_reply(event, f"🔥 <b>RAID ACTIVATED!</b>\n🎯 {mention}\n⚡ Speed: <code>{delays.get(session_index, 0.3)}s</code>", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.stopra$'))
    async def stopra_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        raid_tasks[session_index] = False
        await safe_reply(event, "✅ <b>RAID Stopped!</b>", 1)
    
    # ==================== .fr - FINAL FIXED ====================
    @client.on(events.NewMessage(pattern=r'^\.fr'))
    async def fr_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        full_text = event.raw_text
        content = full_text[3:].strip()
        
        if not content:
            await safe_reply(event, "❌ <b>Format:</b>\n<code>.fr 7164221424 7005373305\\nYour message here...</code>\n\n💡 Use User IDs or @usernames!", 5)
            return
        
        lines = content.split('\n')
        first_line = lines[0] if lines else ""
        
        # Extract targets
        targets = []
        remaining_parts = []
        
        for part in first_line.split():
            if part.isdigit() and len(part) >= 5:
                targets.append(int(part))
            elif part.startswith('@'):
                try:
                    entity = await client.get_entity(part)
                    targets.append(entity.id)
                except:
                    remaining_parts.append(part)
            else:
                remaining_parts.append(part)
        
        # Build message
        message_text = ' '.join(remaining_parts)
        if len(lines) > 1:
            message_text += '\n' + '\n'.join(lines[1:])
        message_text = message_text.strip()
        
        if not targets:
            await safe_reply(event, "❌ No valid targets found!\n\nExamples:\n<code>.fr 7164221424 7005373305\\nYour message</code>\n<code>.fr @username1 @username2\\nYour message</code>", 5)
            return
        
        if not message_text:
            await safe_reply(event, "❌ Add message after targets on new line!", 3)
            return
        
        # Get target chat
        if event.reply_to_msg_id:
            target_chat = event.chat_id
            target_msg_id = event.reply_to_msg_id
            is_reply_mode = True
        else:
            target_chat = event.chat_id
            target_msg_id = None
            is_reply_mode = False
        
        # Stop previous FR
        if fr_active.get(session_index, False):
            fr_active[session_index] = False
            await asyncio.sleep(0.5)
        
        fr_active[session_index] = True
        fr_target_chat[session_index] = target_chat
        fr_target_msg_id[session_index] = target_msg_id
        fr_user_ids[session_index] = targets
        fr_full_text[session_index] = message_text
        
        # Get names for display
        print(f"\n📝 Fetching info for {len(targets)} users...")
        name_list = []
        
        for uid in targets:
            name = await get_user_real_name(client, uid)
            name_list.append(name)
            print(f"   ✓ {name}")
            await asyncio.sleep(0.1)
        
        preview_text = ", ".join(name_list[:3])
        if len(targets) > 3:
            preview_text += f" +{len(targets)-3} more"
        
        mode_text = "REPLY" if is_reply_mode else "DIRECT"
        speed = delays.get(session_index, 0.3)
        await safe_reply(event, f"🔥 <b>FR ACTIVATED!</b> ({mode_text})\n👥 Targets: {preview_text}\n⚡ Speed: <code>{speed}s</code>", 3)
        
        # FR Loop
        async def fr_loop():
            loop_count = 0
            while fr_active.get(session_index, False) and not shutdown_flag:
                try:
                    await anti_flood_wait(session_index)
                    
                    # Build mentions dynamically each loop (to handle any new cache entries)
                    mentions = []
                    for uid in targets:
                        name = await get_user_real_name(client, uid)
                        mentions.append(make_clickable_mention(name, uid))
                    
                    final_text = f"{message_text}\n\n{' '.join(mentions)}"
                    
                    if is_reply_mode and fr_target_msg_id.get(session_index):
                        try:
                            target_msg = await client.get_messages(fr_target_chat[session_index], ids=fr_target_msg_id[session_index])
                            if target_msg:
                                await target_msg.reply(final_text, parse_mode='html')
                            else:
                                await client.send_message(fr_target_chat[session_index], final_text, parse_mode='html')
                        except:
                            await client.send_message(fr_target_chat[session_index], final_text, parse_mode='html')
                    else:
                        await client.send_message(fr_target_chat[session_index], final_text, parse_mode='html')
                    
                    loop_count += 1
                    if loop_count % 10 == 0:
                        print(f"   📤 FR sent {loop_count} messages")
                    
                    await asyncio.sleep(delays.get(session_index, 0.3))
                except FloodWaitError as e:
                    print(f"   ⏳ Flood wait {e.seconds}s")
                    await asyncio.sleep(e.seconds + random.uniform(2, 5))
                except Exception as e:
                    print(f"   ⚠️ FR Error: {e}")
                    await asyncio.sleep(1)
        
        asyncio.create_task(fr_loop())
    
    @client.on(events.NewMessage(pattern=r'^\.stopfr$'))
    async def stopfr_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        fr_active[session_index] = False
        await safe_reply(event, "✅ <b>FR Stopped!</b>", 1)
    
    # ==================== .cs ====================
    @client.on(events.NewMessage(pattern=r'^\.cs'))
    async def cs_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        content = event.raw_text[3:].strip()
        
        if not content:
            await safe_reply(event, "❌ <code>.cs Your auto-reply message</code>", 1)
            return
        
        chat_id = event.chat_id
        
        if session_index not in cs_auto_reply:
            cs_auto_reply[session_index] = {}
        
        cs_auto_reply[session_index][chat_id] = content
        cs_active[session_index] = True
        
        await safe_reply(event, f"✅ <b>CS ACTIVATED!</b>\n💬 <code>{content[:50]}...</code>", 1)
    
    @client.on(events.NewMessage(pattern=r'^\.stopcs$'))
    async def stopcs_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        cs_active[session_index] = False
        if session_index in cs_auto_reply:
            cs_auto_reply[session_index] = {}
        await safe_reply(event, "✅ <b>CS Stopped!</b>", 1)
    
    # CS Listener
    @client.on(events.NewMessage(incoming=True))
    async def cs_listener(event):
        if shutdown_flag:
            return
        if not cs_active.get(session_index, False):
            return
        
        chat_id = event.chat_id
        if not chat_id:
            return
        
        if session_index in cs_auto_reply and chat_id in cs_auto_reply[session_index]:
            try:
                me = await client.get_me()
                if event.out or event.sender_id == me.id:
                    return
            except:
                pass
            
            reply_msg = cs_auto_reply[session_index][chat_id]
            try:
                await anti_flood_wait(session_index)
                name = await get_user_real_name(client, event.sender_id)
                mention = make_clickable_mention(name, event.sender_id)
                await event.reply(f"{mention} {reply_msg}", parse_mode='html')
                await asyncio.sleep(delays.get(session_index, 0.3))
            except:
                pass
    
    # ==================== .ta ====================
    @client.on(events.NewMessage(pattern=r'^\.ta (.+)$'))
    async def ta_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        if not event.is_group:
            await safe_reply(event, "❌ Groups only!", 1)
            return
        
        txt = event.pattern_match.group(1)
        chat = await event.get_input_chat()
        
        try:
            status = await event.reply("🔄 Fetching members...")
        except:
            status = await event.reply("🔄 Fetching members...")
        
        member_ids = []
        try:
            async for user in client.iter_participants(chat):
                if not user.deleted:
                    member_ids.append(user.id)
                    await asyncio.sleep(0.05)
        except:
            pass
        
        await status.edit(f"🔄 Tagging {len(member_ids)} members...")
        
        chunk_size = 10
        for i in range(0, len(member_ids), chunk_size):
            batch = member_ids[i:i+chunk_size]
            try:
                mentions = []
                for uid in batch:
                    name = await get_user_real_name(client, uid)
                    mentions.append(make_clickable_mention(name, uid))
                await client.send_message(event.chat_id, f"{' '.join(mentions)}\n\n{txt}", parse_mode='html')
                await asyncio.sleep(2)
            except:
                pass
        
        await status.edit(f"✅ Tagged <code>{len(member_ids)}</code> members", parse_mode='html')
        asyncio.create_task(delete_msg_delay(status, 5))
    
    # ==================== .pg ====================
    @client.on(events.NewMessage(pattern=r'^\.pg$'))
    async def pg_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        chat = await event.get_input_chat()
        try:
            msg = await event.reply("🧹 Purging...")
        except:
            msg = await event.reply("🧹 Purging...")
        
        try:
            me = await client.get_me()
            ids = []
            async for m in client.iter_messages(chat, from_user=me.id, limit=500):
                ids.append(m.id)
            if ids:
                await client.delete_messages(chat, ids)
            try:
                await msg.edit(f"✅ Purged <code>{len(ids)}</code> messages", parse_mode='html')
            except:
                pass
        except:
            try:
                await msg.edit("❌ Failed")
            except:
                pass
        asyncio.create_task(delete_msg_delay(msg, 3))
    
    # ==================== .sudo Commands ====================
    @client.on(events.NewMessage(pattern=r'^\.sudo (\d+)$'))
    async def sudo_add_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if event.sender_id != MAIN_OWNER:
            return
        uid = int(event.pattern_match.group(1))
        if uid not in GLOBAL_SUDO_USERS:
            GLOBAL_SUDO_USERS.append(uid)
            await safe_reply(event, f"✅ Added sudo: <code>{uid}</code>", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.delsudo (\d+)$'))
    async def sudo_remove_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if event.sender_id != MAIN_OWNER:
            return
        uid = int(event.pattern_match.group(1))
        if uid in GLOBAL_SUDO_USERS:
            GLOBAL_SUDO_USERS.remove(uid)
            await safe_reply(event, f"✅ Removed sudo: <code>{uid}</code>", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.sudolist$'))
    async def sudo_list_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        sudo_list = "\n".join([f"├ <code>{uid}</code>" for uid in GLOBAL_SUDO_USERS])
        await safe_reply(event, f"👑 <b>SUDO USERS</b>\n{sudo_list}\n└ <b>Total: {len(GLOBAL_SUDO_USERS)}</b>", 5)
    
    # ==================== .session & .sessions ====================
    @client.on(events.NewMessage(pattern=r'^\.session$'))
    async def session_info_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        me = await client.get_me()
        info = f"📱 <b>SESSION INFO</b>\n├ ID: <code>{me.id}</code>\n├ Name: {me.first_name or 'N/A'}\n├ Username: @{me.username if me.username else 'N/A'}\n└ Session: <code>{session_index}</code>"
        await safe_reply(event, info, 5)
    
    @client.on(events.NewMessage(pattern=r'^\.sessions$'))
    async def sessions_list_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        sessions_list = []
        for idx, c in clients.items():
            try:
                me = await c.get_me()
                sessions_list.append(f"├ Session {idx}: @{me.username or me.first_name}")
            except:
                sessions_list.append(f"├ Session {idx}: ❌ Offline")
        text = "📱 <b>ACTIVE SESSIONS</b>\n" + "\n".join(sessions_list) + f"\n└ <b>Total: {len(clients)}</b>"
        await safe_reply(event, text, 10)
    
    # ==================== .help ====================
    @client.on(events.NewMessage(pattern=r'^\.help$'))
    async def help_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        help_text = f"""<b>🔥 USERBOT COMMANDS</b>

<b>🎯 Raid Commands:</b>
├ <code>.fr 7164221424 7005373305</code> - Force Raid
│    └ Then write message on new line
│    💡 Use User IDs or @usernames!
├ <code>.ra @user</code> - Normal Raid
├ <code>.rr5 @user</code> - Reply Raid
├ <code>.cs msg</code> - Custom Auto Reply
├ <code>.ta msg</code> - Tag All Members

<b>⚙️ Settings:</b>
├ <code>.dly 0.5</code> - Set speed
├ <code>.ping</code> - Check latency
├ <code>.stats</code> - System stats

<b>🛑 Stop Commands:</b>
├ <code>.over</code> - STOP EVERYTHING
├ <code>.stopfr</code> - Stop FR
├ <code>.stopra</code> - Stop RAID
├ <code>.stoprr</code> - Stop RR
├ <code>.stopcs</code> - Stop CS

<b>👑 Sudo Commands:</b>
├ <code>.sudo id</code> - Add sudo
├ <code>.delsudo id</code> - Remove sudo
├ <code>.sudolist</code> - List sudo

<b>📱 Session Commands:</b>
├ <code>.session</code> - Current session
├ <code>.sessions</code> - All sessions

<b>🔧 Utility:</b>
├ <code>.join link</code> - Join
├ <code>.joinleft link</code> - Leave
├ <code>.pg</code> - Purge messages

⚡ Current Speed: <code>{delays.get(session_index, 0.3)}s</code>
💡 Click on any NAME/ID - profile will open via tg://openmessage?user_id=ID"""
        
        try:
            msg = await event.reply(help_text, parse_mode='html')
        except:
            msg = await event.reply(help_text, parse_mode='html')
        
        asyncio.create_task(delete_msg_delay(msg, 45))

# ==================== MAIN ====================
async def main():
    print("\n" + "="*60)
    print("   🔥 MULTI-SESSION USERBOT v12.0 - FINAL")
    print("="*60)
    print(f"   👑 OWNER: {MAIN_OWNER}")
    print(f"   📱 TOTAL SESSIONS: {len(SESSIONS)}")
    print(f"   ⚡ DEFAULT SPEED: 0.3s")
    print(f"   💯 CLICKABLE: <a href='tg://openmessage?user_id=ID'>NAME or ID</a>")
    print("="*60)
    
    await start_sessions()
    
    if clients:
        print("\n" + "="*60)
        print(f"   ✅ {len(clients)} SESSION(S) ACTIVE!")
        print("="*60)
        print("\n   📌 QUICK COMMANDS:")
        print("   ├ .help - Show all commands")
        print("   ├ .fr 7164221424 7005373305\\nmsg - Force Raid")
        print("   ├ .ra @user - Normal Raid")
        print("   ├ .rr5 @user - Reply Raid")
        print("   ├ .cs msg - Auto Reply")
        print("   └ .over - STOP EVERYTHING")
        print("="*60 + "\n")
        
        print("   🟢 BOT IS RUNNING...")
        print("   💡 Click on ANY mention - profile will open!")
        print("   💡 Format: <a href='tg://openmessage?user_id=ID'>NAME</a>")
        print("   📝 TYPE .help IN ANY CHAT\n")
        
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n\n   🛑 SHUTTING DOWN...")
            await graceful_shutdown()
            print("   👋 BYE!\n")
    else:
        print("\n   ❌ NO SESSIONS STARTED!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n   👋 STOPPED!")
    except Exception as e:
        print(f"\n   ❌ ERROR: {e}")
