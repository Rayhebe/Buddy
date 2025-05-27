import asyncio
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition
from highrise import Highrise, GetMessagesRequest
from functions.loop_emote import (
    check_and_start_emote_loop,
    handle_user_movement,
    emote_list
)
from functions.json import bot_location

# الكلمات المفتاحية لعرض قائمة الإيموتات
emote_keywords = {
    "emotelist", "emoteslist", "!emotes", "/emotes",
    "!emote", "/emote", "emotes", "emote",
    "emote list", "emotes list", "Emote", "Emotes",
    "Emote list", "Emotes list", "Emotelist",
    "!emotes list", "!emotelist", "!Emotes", "!Emote"
}

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}
        self.loop_emote_list = emote_list

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        if bot_location:
            try:
                await self.highrise.walk_to(Position(**bot_location))
                print("Bot moved to saved position.")
            except Exception as e:
                print("Error moving to saved position:", e)
        print("Bot is ready.")
        
    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        print(f"{user.username} (ID: {user.id})")
        await self.highrise.chat(f"{user.username} joined to find a Buddy !")
        await self.highrise.send_whisper(user.id, f"❤️Welcome [{user.username}]! Use: [!emote list] or [1-97] for dances & emotes.")
        await self.highrise.send_whisper(user.id, f"❤️Use: [/help] for more information.")
        await self.highrise.send_whisper(user.id, f"❤Type F3 F2 and F1 to teleport between the floor 🤍.")
        await self.highrise.send_emote("dance-hipshake")
        await self.highrise.send_emote("emote-lust", user.id)
        await self.highrise.react("heart", user.id)

    async def on_chat(self, user: User, message: str):
        print(f"[CHAT] {user.username}: {message}")

        # عرض قائمة الإيموتات عند تطابق الكلمة
        if message.lower().strip() in [k.lower() for k in emote_keywords]:
            try:
                emote_names = [aliases[0] for aliases, _, _ in self.loop_emote_list]
                emote_text = "Available Emotes:\n" + "\n".join(f"- {name}" for name in emote_names)
                await self.highrise.send_whisper(user.id, emote_text)
                return
            except Exception as e:
                print("Error sending emote list (chat):", e)

        # تشغيل الإيموتات التلقائية
        await check_and_start_emote_loop(self, user, message)

        # حفظ موقع البوت
        if message == "!sbot" and user.username == "RayBM":
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        bot_location["x"] = pos.x
                        bot_location["y"] = pos.y
                        bot_location["z"] = pos.z
                        bot_location["facing"] = pos.facing
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع البوت بنجاح: {bot_location}")
                        break
            except Exception as e:
                print("خطأ في حفظ موقع البوت:", e)

        # العودة للموقع المحفوظ
        if message == "!base":
            try:
                if bot_location:
                    await self.highrise.walk_to(Position(**bot_location))
            except Exception as e:
                print("خطأ في تنفيذ !base:", e)

        # أوامر الطوابق
        msg = message.lower().replace(" ", "")
        if msg in ("-floor1", "!floor1", "floor1", "/floor1", "f1", "-1"):
            await self.highrise.teleport(user.id, Position(9.5, 0.0, 16.5))
        elif msg in ("-floor2", "!floor2", "floor2", "/floor2", "f2", "-2"):
            await self.highrise.teleport(user.id, Position(7.5, 9.5, 6.0))
        elif msg in ("-floor3", "!floor3", "floor3", "/floor3", "f3", "-3"):
            await self.highrise.teleport(user.id, Position(10.5, 20.0, 6.5))

    async def on_whisper(self, user: User, message: str):
        print(f"[WHISPER] {user.username}: {message}")

        # عرض قائمة الإيموتات عند الهمس
        if message.lower().strip() in [k.lower() for k in emote_keywords]:
            try:
                emote_names = [aliases[0] for aliases, _, _ in self.loop_emote_list]
                emote_text = "Available Emotes:\n" + "\n".join(f"- {name}" for name in emote_names)
                await self.highrise.send_whisper(user.id, emote_text)
                return
            except Exception as e:
                print("Error sending emote list (whisper):", e)

        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_stop(self):
        print("Bot stopped.")
