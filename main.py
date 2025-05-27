import asyncio
import random
import os
import importlib.util

from highrise import Highrise, BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition, GetMessagesRequest

# استيراد الدوال من ملفاتك
from functions.loop_emote import (
    check_and_start_emote_loop,
    handle_user_movement,
    emote_list
)
from functions.json import bot_location

class Bot(BaseBot):

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("working")
        await self.highrise.walk_to(Position(14.5, 0.25, 3.5, "FrontRight"))

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        print(f"{user.username} (ID: {user.id})")
        await self.highrise.chat(f"{user.username} joined to find a Buddy!")

        # رسائل الترحيب الخاصة
        await self.highrise.send_whisper(user.id, f"❤️Welcome [{user.username}]! Use: [!emote list] or [1-97] for dances & emotes.")
        await self.highrise.send_whisper(user.id, "❤️Use: [/help] for more information.")
        await self.highrise.send_whisper(user.id, "❤Type F4 or floor number to teleport 🤍.")

        # إيموتات ترحيبية
        await self.highrise.send_emote("dance-hipshake")
        await self.highrise.send_emote("emote-lust", user.id)
        await self.highrise.react("clap", user.id)

    async def on_chat(self, user: User, message: str) -> None:
        print(f"{user.username}: {message}")

        message_lower = message.lower()

        # أوامر خاصة للمشروبات
        if any(message_lower.startswith(drink) for drink in ["whiskey", "whisky", "drink", "!whiskey"]):
            await self.react_message(user, "Whiskey: because adulting is hard and sometimes you need a little liquid encouragement! 🥃")

        elif any(message_lower.startswith(beer) for beer in ["beer", "alcohol", "!beer", "!drunk"]):
            await self.react_message(user, "on the house drive safe 🍺")

        elif any(message_lower.startswith(wine) for wine in ["wine", "redwine", "red wine", "plonk", "vino"]):
            await self.react_message(user, "Ah, red wine—fancy!🍷 Trying to look sophisticated, or just hoping for purple teeth?🍷")

        elif any(message_lower.startswith(spirit) for spirit in ["champagne", "vodka", "celebration", "celebrate"]):
            await self.react_message(user, "Let’s raise a glass to celebrate the good times and the friends who make them unforgettable. 🍸🎉")

        elif any(message_lower.startswith(cocktail) for cocktail in ["cocktail", "mixed", "mojito", "potion", "tonic", "julep"]):
            await self.react_message(user, "Cheers to the moments that turn into memories, one drink at a time. 🥂")

        elif any(message_lower.startswith(water) for water in ["water", "thirsty", "dry"]):
            await self.react_message(user, "Ah, water—because staying hydrated is the real adventure! 🚰💧")

        # أمر الدرع
        elif message_lower.startswith("/shield"):
            await self.react_message(user, "🛡 You Used The Shield 🛡")

        # أوامر التنقل الخاصة
        elif any(message_lower.startswith(tp) for tp in ["/tele", "/tp", "/fly", "!tele", "!tp", "!fly"]):
            if user.username in ["iced_yu", "FallonXOXO", "RayMG"]:
                await self.teleporter(message)

        # أوامر الرموز التعبيرية
        elif message_lower in ["!emoteall"]:
            await self.send_emote_batches(user)

        # أوامر قائمة الإيموتات
        elif message_lower in ["!lista", "!emote list", "!list", "/lista", "/emote list", "/list"]:
            await self.send_emote_list(user, prefix="!" if message.startswith("!") else "/")

        # أوامر الأرضيات (الطوابق)
        elif any(message_lower.startswith(f) for f in ["f1", "floor1", "!floor1", "-floor1", "/floor1"]):
            await self.highrise.teleport(user.id, Position(3.5, 0.0, 7.0))

        elif any(message_lower.startswith(f) for f in ["f2", "floor2", "!floor2", "-floor2", "/floor2"]):
            await self.highrise.teleport(user.id, Position(10.5, 8.0, 3.5))

        elif any(message_lower.startswith(f) for f in ["f3", "floor3", "!floor3", "-floor3", "/floor3"]):
            await self.highrise.teleport(user.id, Position(15.0, 15.2, 9.5))

        elif any(message_lower.startswith(f) for f in ["f4", "floor4", "!floor4", "-floor4", "/floor4"]):
            await self.highrise.teleport(user.id, Position(16.0, 20.0, 5.5))

        # أوامر خاصة
        elif message_lower.startswith(("/", "-", ".", "!")):
            await self.command_handler(user, message)

    async def react_message(self, user: User, text: str) -> None:
        await self.highrise.react("heart", user.id)
        await self.highrise.send_whisper(user.id, f"@{user.username}  {text}")

    async def send_emote_batches(self, user: User) -> None:
        # اجعل هذه القائمة تختصر بعدد الأسطر. (هنا كمثال فقط)
        batches = [
            "Fashion All , Wrong All , Cutey All , Superpose All , Punk All",
            "Pose3 All , Pose7 All , Pose5 All , Pose1 All , Enthused All",
            "Zombie All , Celebrate All , Kiss All , Bow All , Snowangel All",
            "Skating All , Time All , Gottago All , Scritchy All , Bitnervous All"
        ]
        for line in batches:
            await self.highrise.send_whisper(user.id, line)

    async def send_emote_list(self, user: User, prefix: str = "!") -> None:
        # مثال تنظيمي لقائمة الإيموتات
        emote_lines = [
            f"{prefix}angry , {prefix}thumbsup , {prefix}cursing , {prefix}flex , {prefix}gagging , {prefix}celebrate",
            f"{prefix}pose1 , {prefix}pose2 , {prefix}superpose , {prefix}cute , {prefix}singing",
            f"{prefix}watch , {prefix}tiktok , {prefix}tiktok2 , {prefix}repose , {prefix}guitar",
            f"{prefix}icecream , {prefix}zombie , {prefix}kiss , {prefix}model , {prefix}sit"
        ]
        for line in emote_lines:
            await self.highrise.send_whisper(user.id, line)

    async def teleport_user_next_to(self, target_username: str, requester_user: User) -> None:
        try:
            # Get the position of the requester_user
            room_users = await self.highrise.get_room_users()
            requester_position = None
            for user, position in room_users.content:
                if user.id == requester_user.id:
                    requester_position = position
                    break

            # Find the target user and their position
            for user, position in room_users.content:
                if user.username.lower() == target_username.lower():
                    z = requester_position.z
                    new_z = z + 1  # Example: Move +1 on the z-axis (upwards)
                    await self.teleport(user, Position(requester_position.x, requester_position.y, new_z, requester_position.facing))
                    break
        except Exception as e:
            print(f"An error occurred while teleporting {target_username} next to {requester_user.username}: {e}")
)
       # ─────────────────────────────────────────────
# Teleport a user next to another
# نقل المستخدم بجانب مستخدم آخر
# ─────────────────────────────────────────────
async def teleport_user_next_to(self, target_username: str, requester_user: User) -> None:
    try:
        room_users = await self.highrise.get_room_users()
        requester_position = None

        for user, position in room_users.content:
            if user.id == requester_user.id:
                requester_position = position
                break

        for user, position in room_users.content:
            if user.username.lower() == target_username.lower():
                new_z = requester_position.z + 1
                await self.teleport(user, Position(requester_position.x, requester_position.y, new_z, requester_position.facing))
                break

    except Exception as e:
        print(f"Error teleporting {target_username} next to {requester_user.username}: {e}")


# ─────────────────────────────────────────────
# General teleport command handler
# معالجة أمر النقل العام
# ─────────────────────────────────────────────
async def teleporter(self, message: str) -> None:
    try:
        command, username, coordinate = message.split(" ")
    except:
        return

    room_users = (await self.highrise.get_room_users()).content
    user_id = None
    for user, _ in room_users:
        if user.username.lower() == username.lower():
            user_id = user.id
            break

    if not user_id:
        return

    try:
        x, y, z = coordinate.split(",")
    except:
        return

    await self.highrise.teleport(user_id=user_id, dest=Position(float(x), float(y), float(z)))


# ─────────────────────────────────────────────
# Handle dynamic command execution from / ! - .
# تنفيذ الأوامر من الملفات الخارجية بشكل ديناميكي
# ─────────────────────────────────────────────
async def command_handler(self, user: User, message: str):
    parts = message.split(" ")
    command = parts[0][1:]
    functions_folder = "functions"

    for file_name in os.listdir(functions_folder):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]
            module_path = os.path.join(functions_folder, file_name)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, command) and callable(getattr(module, command)):
                function = getattr(module, command)
                await function(self, user, message)
                return  # Stop after first matching function


# ─────────────────────────────────────────────
# Handle private whispers
# التعامل مع الهمسات الخاصة
# ─────────────────────────────────────────────
async def on_whisper(self, user: User, message: str) -> None:
    print(f"{user.username} whispered: {message}")

    # Allow RayBM and botmes to broadcast whispers
    if user.username.lower() in ["raybm", "botmes"]:
        await self.highrise.chat(message)
        print(f"Broadcasted whisper to room: {message}")

    # Handle teleport commands
    if message.lower().startswith(("tele", "/tp", "/fly", "!tele", "!tp", "!fly")):
        if user.username in [
            "FallonXOXO", "Its.Melly.Moo.XoXo", "sh1n1gam1699",
            "Abbie_38", "hidinurbasement", "@emping",
            "BabygirlFae", "RayBM"
        ]:
            await self.teleporter(message)

    # Handle dynamic commands from / ! - .
    if message.startswith(("/", "-", ".", "!")):
        await self.command_handler(user, message)

    # Handle summon requests
    if message.lower().startswith(("summon", "summom", "!summon", "!summom", "/summon", "/summom")):
        if user.username in [
            "FallonXOXO", "Shaun_Knox", "@Its.Melly.Moo.XoXo",
            "@RayBM", "Dreamy._.KY"
        ]:
            target_username = message.split("@")[-1].strip()
            await self.teleport_user_next_to(target_username, user)


# ─────────────────────────────────────────────
# Event: when a user moves
# الحدث: عندما يتحرك مستخدم
# ─────────────────────────────────────────────
async def on_user_move(self, user: User, pos: Position) -> None:
    print(f"{user.username} moved to {pos}")


# ─────────────────────────────────────────────
# Event: when a user performs an emote
# الحدث: عندما يقوم المستخدم بحركة تعبيرية
# ─────────────────────────────────────────────
async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
    print(f"{user.username} emoted: {emote_id}")
