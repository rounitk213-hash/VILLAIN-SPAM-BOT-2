import asyncio
import random
import re
import logging
import time
import psutil
import os
import warnings
from datetime import datetime
from collections import deque
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import FloodWaitError, RPCError
from telethon.tl.functions.users import GetFullUserRequest

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

# ==================== ABUSE LIST (shortened for space - keep your full list) ====================
abuse_roast = [
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝟭𝟬𝟬𝟬 𝗟𝗔𝗧𝗛𝗜 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗥𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗠𝗘𝗜𝗡 𝗔𝗚 𝗟𝗚𝗔 𝗞𝗔𝗥 𝟱𝟬𝟬 𝗟𝗜𝗧𝗔𝗥 𝗣𝗘𝗧𝗥𝗢𝗟 𝗗𝗔𝗔𝗟𝗨𝗡𝗚𝗔",
    # Keep all your original abuse lines here...
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
rate_limit_queues = {}  # FIXED: Proper rate limiting per session
start_time = datetime.now()
shutdown_flag = False
name_cache = {}
name_cache_time = {}

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

# FIXED: Better rate limiting without freezing
async def rate_limited_send(session_index, coro_func, *args, **kwargs):
    """Send with proper rate limiting - never freezes"""
    if session_index not in rate_limit_queues:
        rate_limit_queues[session_index] = asyncio.Queue()
        asyncio.create_task(rate_limit_worker(session_index))
    
    queue = rate_limit_queues[session_index]
    future = asyncio.Future()
    await queue.put((coro_func, args, kwargs, future))
    return await future

async def rate_limit_worker(session_index):
    """Worker that processes messages at optimal speed"""
    queue = rate_limit_queues[session_index]
    while not shutdown_flag:
        try:
            # Get next task with timeout
            task = await asyncio.wait_for(queue.get(), timeout=0.5)
        except asyncio.TimeoutError:
            continue
        
        coro_func, args, kwargs, future = task
        
        try:
            # Apply rate limit based on delay setting
            delay = delays.get(session_index, 0.2)
            if delay < 0.15:
                delay = 0.15  # Minimum 150ms to avoid floods
            
            result = await coro_func(*args, **kwargs)
            future.set_result(result)
            await asyncio.sleep(delay)
        except FloodWaitError as e:
            # Handle flood wait properly
            wait_time = e.seconds + random.uniform(1, 2)
            print(f"⚠️ Session {session_index} flood waiting {wait_time}s")
            await asyncio.sleep(wait_time)
            # Retry once
            try:
                result = await coro_func(*args, **kwargs)
                future.set_result(result)
            except Exception as retry_error:
                future.set_exception(retry_error)
        except Exception as e:
            future.set_exception(e)
        finally:
            queue.task_done()

async def send_message_safe(client, chat_id, message, parse_mode='html', reply_to=None):
    """Safe message sending with retry"""
    for attempt in range(3):
        try:
            if reply_to:
                return await client.send_message(chat_id, message, parse_mode=parse_mode, reply_to=reply_to)
            else:
                return await client.send_message(chat_id, message, parse_mode=parse_mode)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(0.5)
    return None

async def get_user_real_name(client, user_id):
    """Get user's real name with caching"""
    user_id = int(user_id)
    
    # Check cache with TTL (60 seconds)
    if user_id in name_cache and (time.time() - name_cache_time.get(user_id, 0)) < 60:
        return name_cache[user_id]
    
    name = None
    
    # Try multiple methods quickly
    for attempt in range(2):
        try:
            user = await client.get_entity(user_id)
            if user.first_name:
                name = user.first_name
                break
            elif user.last_name:
                name = user.last_name
                break
            elif user.username:
                name = f"@{user.username}"
                break
        except:
            pass
        
        if not name and attempt == 0:
            try:
                full_user = await client(GetFullUserRequest(user_id))
                if full_user.user.first_name:
                    name = full_user.user.first_name
                    break
                elif full_user.user.username:
                    name = f"@{full_user.user.username}"
                    break
            except:
                pass
    
    if not name:
        name = str(user_id)
    
    # Clean name
    name = re.sub(r'[\[\]\(\)\_\*\`\~\#\@]', '', name)[:50]
    if not name or name == "":
        name = str(user_id)
    
    # Cache it
    name_cache[user_id] = name
    name_cache_time[user_id] = time.time()
    return name

def make_clickable_mention(name, user_id):
    """Create clickable mention"""
    return f'<a href="tg://user?id={user_id}">{name}</a>'

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
        if 't.me/+' in target or 't.me/joinchat/' in target:
            hash_part = target.split('/')[-1].replace('+', '')
            await client(ImportChatInviteRequest(hash_part))
            return True, None, None
        else:
            entity = await client.get_entity(target)
            await client(JoinChannelRequest(entity))
            return True, None, None
    except:
        return False, None, None

async def leave_channel(client, target):
    try:
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

async def graceful_shutdown():
    global shutdown_flag
    shutdown_flag = True
    stop_all_operations()
    await asyncio.sleep(0.5)
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
                delays[idx] = 0.2  # FASTER DEFAULT
                rr_targets[idx] = None
                rr_counts[idx] = {}
                raid_tasks[idx] = False
                fr_active[idx] = False
                cs_active[idx] = False
                cs_auto_reply[idx] = {}
                last_message_time[idx] = 0
                rate_limit_queues[idx] = asyncio.Queue()
                
                print(f"[✓] Session {idx} (@{me.username or me.first_name})")
                
                # Auto-join in background (non-blocking)
                if AUTO_JOIN_LINK:
                    asyncio.create_task(join_channel_with_discussion(client, AUTO_JOIN_LINK))
                
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
        await safe_reply(event, "✅ <b>USERBOT ACTIVATED!</b>\n⚡ Super Speed Active!\n📌 .help for commands", 2)
    
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
        asyncio.create_task(delete_msg_delay(msg, 3))
    
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
        if dly < 0.15:
            dly = 0.15
        if dly > 10:
            dly = 10
        delays[session_index] = dly
        await safe_reply(event, f"⚡ Speed set to: <code>{dly}s</code>", 1)
    
    # ==================== .fr - FASTEST VERSION ====================
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
            await safe_reply(event, "❌ <b>Format:</b>\n<code>.fr 7164221424 7005373305\\nYour message here...</code>", 5)
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
            await safe_reply(event, "❌ No valid targets found!", 3)
            return
        
        if not message_text:
            await safe_reply(event, "❌ Add message after targets!", 3)
            return
        
        # Stop previous FR
        if fr_active.get(session_index, False):
            fr_active[session_index] = False
            await asyncio.sleep(0.3)
        
        fr_active[session_index] = True
        fr_target_chat[session_index] = event.chat_id
        fr_target_msg_id[session_index] = event.reply_to_msg_id if event.reply_to_msg_id else None
        fr_user_ids[session_index] = targets
        fr_full_text[session_index] = message_text
        
        # Show preview
        name_list = []
        for uid in targets[:5]:
            name = await get_user_real_name(client, uid)
            name_list.append(name)
        
        preview_text = ", ".join(name_list[:3])
        if len(targets) > 3:
            preview_text += f" +{len(targets)-3} more"
        
        speed = delays.get(session_index, 0.2)
        await safe_reply(event, f"🔥 <b>FR ACTIVATED!</b>\n👥 Targets: {preview_text}\n⚡ Speed: <code>{speed}s</code>", 2)
        
        # FR Loop with rate limiting
        async def fr_loop():
            loop_count = 0
            error_count = 0
            while fr_active.get(session_index, False) and not shutdown_flag:
                try:
                    # Build mentions
                    mentions = []
                    for uid in targets:
                        name = await get_user_real_name(client, uid)
                        mentions.append(make_clickable_mention(name, uid))
                    
                    final_text = f"{message_text}\n\n{' '.join(mentions)}"
                    
                    # Send with rate limiting
                    if fr_target_msg_id.get(session_index):
                        try:
                            await rate_limited_send(session_index, send_message_safe, client, 
                                                   fr_target_chat[session_index], final_text, 
                                                   parse_mode='html', reply_to=fr_target_msg_id[session_index])
                        except:
                            await rate_limited_send(session_index, send_message_safe, client,
                                                   fr_target_chat[session_index], final_text, parse_mode='html')
                    else:
                        await rate_limited_send(session_index, send_message_safe, client,
                                               fr_target_chat[session_index], final_text, parse_mode='html')
                    
                    loop_count += 1
                    error_count = 0
                    
                    if loop_count % 50 == 0:
                        print(f"📤 [{session_index}] FR sent {loop_count} messages")
                    
                except Exception as e:
                    error_count += 1
                    if error_count > 5:
                        print(f"⚠️ [{session_index}] FR error limit reached, stopping")
                        fr_active[session_index] = False
                        break
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
    
    # ==================== .ra - FAST RAID ====================
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
            count = 0
            while raid_tasks.get(session_index, False) and not shutdown_flag:
                try:
                    roast = random.choice(abuse_roast)
                    await rate_limited_send(session_index, send_message_safe, client,
                                           event.chat_id, f"{mention} {roast}", parse_mode='html')
                    count += 1
                except:
                    await asyncio.sleep(delays.get(session_index, 0.2))
        
        asyncio.create_task(raid_loop())
        await safe_reply(event, f"🔥 <b>RAID ACTIVATED!</b>\n🎯 {mention}\n⚡ Speed: <code>{delays.get(session_index, 0.2)}s</code>", 2)
    
    @client.on(events.NewMessage(pattern=r'^\.stopra$'))
    async def stopra_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        raid_tasks[session_index] = False
        await safe_reply(event, "✅ <b>RAID Stopped!</b>", 1)
    
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
        if not sender or sender not in targets:
            return
        
        count = rr_counts.get(session_index, {}).get(sender, 0)
        if count > 0:
            rr_counts[session_index][sender] = count - 1
            if rr_counts[session_index][sender] <= 0:
                del rr_counts[session_index][sender]
            
            roast = random.choice(abuse_roast)
            name = await get_user_real_name(client, sender)
            mention = make_clickable_mention(name, sender)
            
            await rate_limited_send(session_index, send_message_safe, client,
                                   event.chat_id, f"{mention} {roast}", 
                                   parse_mode='html', reply_to=event.id)
    
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
            name = await get_user_real_name(client, event.sender_id)
            mention = make_clickable_mention(name, event.sender_id)
            
            await rate_limited_send(session_index, send_message_safe, client,
                                   event.chat_id, f"{mention} {reply_msg}", 
                                   parse_mode='html', reply_to=event.id)
    
    # ==================== .ta (Tag All) ====================
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
        
        status = await event.reply("🔄 Fetching members...")
        
        member_ids = []
        try:
            async for user in client.iter_participants(chat):
                if not user.deleted:
                    member_ids.append(user.id)
                    await asyncio.sleep(0.03)  # Faster fetching
        except:
            pass
        
        await status.edit(f"🔄 Tagging {len(member_ids)} members...")
        
        chunk_size = 10  # Send in batches
        for i in range(0, len(member_ids), chunk_size):
            batch = member_ids[i:i+chunk_size]
            try:
                mentions = []
                for uid in batch:
                    name = await get_user_real_name(client, uid)
                    mentions.append(make_clickable_mention(name, uid))
                await send_message_safe(client, event.chat_id, f"{' '.join(mentions)}\n\n{txt}", parse_mode='html')
                await asyncio.sleep(1.5)  # Delay between batches
            except:
                pass
        
        await status.edit(f"✅ Tagged <code>{len(member_ids)}</code> members", parse_mode='html')
        asyncio.create_task(delete_msg_delay(status, 5))
    
    # ==================== .pg (Purge) ====================
    @client.on(events.NewMessage(pattern=r'^\.pg$'))
    async def pg_handler(event):
        if shutdown_flag:
            return
        await delete_msg(event.message)
        if not is_authorized(session_index, event.sender_id):
            return
        
        chat = await event.get_input_chat()
        msg = await event.reply("🧹 Purging...")
        
        try:
            me = await client.get_me()
            ids = []
            async for m in client.iter_messages(chat, from_user=me.id, limit=500):
                ids.append(m.id)
            if ids:
                await client.delete_messages(chat, ids)
            await msg.edit(f"✅ Purged <code>{len(ids)}</code> messages", parse_mode='html')
        except:
            await msg.edit("❌ Failed")
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
        text = f"👑 <b>SUDO USERS</b>\n{sudo_list if sudo_list else '├ None'}\n└ <b>Total: {len(GLOBAL_SUDO_USERS)}</b>"
        await safe_reply(event, text, 5)
    
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
        
        help_text = f"""<b>🔥 SUPER SPEED USERBOT</b>

<b>🎯 Raid Commands:</b>
├ <code>.fr @user1 @user2\\nYour message</code> - Force Raid (MULTI TARGET)
├ <code>.ra @user</code> - Normal Raid
├ <code>.rr5 @user</code> - Reply Raid (5x)
├ <code>.cs msg</code> - Custom Auto Reply
├ <code>.ta msg</code> - Tag All Members

<b>⚙️ Settings:</b>
├ <code>.dly 0.2</code> - Set speed (min 0.15s)
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
├ <code>.join link</code> - Join channel
├ <code>.joinleft link</code> - Leave channel
├ <code>.pg</code> - Purge messages

⚡ Current Speed: <code>{delays.get(session_index, 0.2)}s</code>"""
        
        msg = await event.reply(help_text, parse_mode='html')
        asyncio.create_task(delete_msg_delay(msg, 45))

# ==================== MAIN ====================
async def main():
    print("\n" + "="*60)
    print("   🔥 SUPER SPEED MULTI-SESSION USERBOT")
    print("="*60)
    print(f"   👑 OWNER: {MAIN_OWNER}")
    print(f"   📱 TOTAL SESSIONS: {len(SESSIONS)}")
    print(f"   ⚡ DEFAULT SPEED: 0.2s")
    print("="*60)
    
    await start_sessions()
    
    if clients:
        print("\n" + "="*60)
        print(f"   ✅ {len(clients)} SESSION(S) ACTIVE!")
        print("="*60)
        print("\n   📌 QUICK COMMANDS:")
        print("   ├ .help - Show all commands")
        print("   ├ .fr 7164221424\\nmsg - Force Raid")
        print("   ├ .ra @user - Normal Raid")
        print("   ├ .rr5 @user - Reply Raid")
        print("   ├ .cs msg - Auto Reply")
        print("   └ .over - STOP EVERYTHING")
        print("="*60 + "\n")
        
        print("   🟢 BOT IS RUNNING AT SUPER SPEED!")
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
