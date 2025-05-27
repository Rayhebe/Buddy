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
        await self.highrise.walk_to(Position(14.5 , 0.25 , 3.5, "FrontRight"))
             
    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        # Only the bot prints the message in the console
        print(f"{user.username} (ID: {user.id})")

        # Announce the user has joined the room publicly
        await self.highrise.chat(f"{user.username} joined to find a Buddy!")

        # Send welcome whispers to the user
        await self.highrise.send_whisper(user.id, f"❤️Welcome [{user.username}]! Use: [!emote list] or [1-97] for dances & emotes.")
        await self.highrise.send_whisper(user.id, f"❤️Use: [/help] for more information.")
        await self.highrise.send_whisper(user.id, f"❤Type F4 or floor number to teleport 🤍.")

        # Send emotes
        await self.highrise.send_emote("dance-hipshake")
        await self.highrise.send_emote("emote-lust", user.id)

       # React with a heart emoji
        await self.highrise.react("clap",user.id)
        
    async def on_chat(self, user: User, message: str) -> None:
        print(f"{user.username}: {message}")  

        if message.startswith("/shield"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username} 🛡 You Used The Shield 🛡")

        if message.startswith("whiskey") or      message.startswith("whisky") or      message.startswith("Whiskey") or             message.startswith("drink") or             message.startswith("Drink") or message.startswith("!whiskey"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username}  Whiskey: because adulting is hard and sometimes you need a little liquid encouragement! 🥃")

        if message.startswith("beer") or  message.startswith("Beer") or  message.startswith("alcohol") or message.startswith("Alcohol") or  message.startswith("!beer") or message.startswith("!Drunk"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username}  on the house drive safe 🍺")

        if message.startswith("wine") or  message.startswith("redwine") or  message.startswith("red wine") or message.startswith("plonk") or  message.startswith("Plonk") or message.startswith("vino"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username}  Ah, red wine—fancy!🍷 Trying to look sophisticated, or just hoping for purple teeth?🍷")
        
        if message.startswith("champagne") or  message.startswith("vodka") or  message.startswith("Vodka") or message.startswith("Champagne") or  message.startswith("celebration") or message.startswith("celebrate"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username}  Ah, “Let’s raise a glass to celebrate the good times and the friends who make them unforgettable.”🍸🎉")
      
       
        if message.startswith("cocktail") or  message.startswith("mixed") or  message.startswith("mojito") or message.startswith("Potion") or  message.startswith("tonic") or message.startswith("julep"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username}  “Cheers to the moments that turn into memories, one drink at a time.🥂")
                                          
         
        if message.startswith("Water") or message.startswith("water") or message.startswith("thirsty") or message.startswith("Thirsty") or  message.startswith("dry") or message.startswith("Dry"):
           await self.highrise.react("heart",user.id)
           await self.highrise.send_whisper(user.id,f"@{user.username}  You could say, “Ah, water—because staying hydrated is the real adventure!”🚰💧")
                      
            
        if        message.startswith("/tele") or              message.startswith("/tp") or              message.startswith("/fly") or     message.startswith("!tele") or      message.startswith("!tp") or     message.startswith("!fly"):
          if user.username == "iced_yu" or user.username == "FallonXOXO" or user.username == "RayMG":            await self.teleporter(message)

        if        message.startswith("/") or              message.startswith("-") or              message.startswith(".") or          message.startswith("!"):
            await self.command_handler(user, message)
          
        if message.startswith("!emoteall"):
          await self.highrise.send_whisper(user.id,"Fashion All , Wrong All , Cutey All , Superpose All , Punk All , Tiktok2 All, Tiktok8 All , Tiktok9 All , Tiktok10 All , Gagging All , Blackpink All , Creepy All , Revelation All , Bashful All , Arabesque All , Party All")

        if message.startswith("!emoteall"):
          await self.highrise.send_whisper(user.id,"Pose3 All , Pose7 All , Pose5 All , Pose1 All , Enthused All , Pose8 All , Sing All , Teleport All , Telekinesis All , Casual All , Icecream All , Watch All")

        if message.startswith("!emoteall"):
          await self.highrise.send_whisper(user.id,"Zombie All , Celebrate All , Kiss All , Bow All , Snowangel All , Confused All , Charging All , Wei All , Cursing All , Greedy All , Russian All , Shop All , Model All , Ren All , Tiktok4 All , Snake All , Uwu All")

        if        message.startswith("-floor1") or message.startswith("!floor1") or message.startswith("-floor 1") or message.startswith("Floor 1") or message.startswith("Floor1") or message.startswith("/floor1") or    message.startswith("floor1") or message.startswith("-1") or    message.startswith("floor1") or message.startswith("f1") or message.startswith("f 1") or message.startswith("floor1") or message.startswith("F1")  or   message.startswith("floor 1") or message.startswith("!floor 1"):
          await self.highrise.teleport(user.id, Position(3.5 , 0.0 , 7.0 ))

        if        message.startswith("-floor3") or message.startswith("!floor3") or message.startswith("-floor 3") or message.startswith("Floor 3") or message.startswith("Floor3") or message.startswith("/floor3") or    message.startswith("floor3") or message.startswith("-3") or    message.startswith("floor3") or message.startswith("f3") or message.startswith("f 3") or message.startswith("floor3") or message.startswith("F3")  or   message.startswith("floor 3") or message.startswith("!floor 3"):
          await self.highrise.teleport(user.id, Position(15.0 , 15.2 , 9.5))

        if        message.startswith("-floor4") or message.startswith("!floor4") or message.startswith("-floor 4") or message.startswith("Floor 4") or message.startswith("Floor4") or message.startswith("/floor4") or    message.startswith("floor4") or message.startswith("-4") or    message.startswith("floor4") or message.startswith("f4") or message.startswith("f 4") or message.startswith("floor4") or message.startswith("F4")  or   message.startswith("floor 4") or message.startswith("!floor 4"):
          await self.highrise.teleport(user.id, Position(16.0 , 20.0 , 5.5))
            
        if        message.startswith("-floor2") or message.startswith("!floor2") or message.startswith("-floor 2") or message.startswith("Floor 2") or message.startswith("Floor2") or message.startswith("/floor2") or    message.startswith("floor2") or message.startswith("-2") or    message.startswith("floor2") or message.startswith("f2") or message.startswith("f 2") or message.startswith("floor2") or message.startswith("F2")  or   message.startswith("floor 2") or message.startswith("!floor 2"):
          await self.highrise.teleport(user.id, Position(10.5 , 8.0 , 3.5))
            
        if message.startswith("!emoteall"):
          await self.highrise.send_whisper(user.id,"Skating All , Time All , Gottago All  , Scritchy All , Bitnervous All , Jingle All , Curtsy All , Hot All , Hyped All ,Sleigh All , Surprise All, Repose All , Kawaii All , Touch All , Gift All , Pushit All , Tiktok All , Smooch All , Launch All")
          
        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
            await self.highrise.send_whisper(user.id,"!angry ,!thumbsup , !cursing , !flex , !gagging , !celebrate , !blackpink , !tiktok2 , !tiktok9 , !pennywise , !russian , !shop , !enthused , !singing ,!wrong , !guitar , !pinguin , !astronaut , !saunter , !flirt , !creepy , !watch , !revelation")
          
        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
            await self.highrise.send_whisper(user.id,"!tiktok10 ,!tiktok8 , !cutey , !pose3 , !pose5 , !pose1 , !pose8 , !pose7  !pose9 , !cute , !superpose , !frog , !snake , !energyball , !maniac , !teleport , !float , !telekinesi , !fight , !wei , !fashion , !boxer , !bashful , !arabesque , !party")
          
        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
            await self.highrise.send_whisper(user.id,"!confused , !charging , !snowangel , !hot , !snowball , !curtsy , !bow ,!model , !greedy , !tired , !shy , !wave , !hello , !lau ,!yes , !sad , !no , !kiss , !casual , !ren , !sit , !punk , !zombie , !gravity , !icecream ,!uwu , !sayso , !star")

        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
          await self.highrise.send_whisper(user.id,"!skating , !bitnervous , !scritchy , !timejump , !gottago , !jingle , !hyped , !sleigh , !surprise , !repose , !kawaii , !touch , !gift , !pushit , !tiktok , !salute , !attention , !smooch , !launch")
          
        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
            await self.highrise.send_whisper(user.id,"/angry ,/thumbsup , /cursing , /flex , /gagging , /celebrate , /blackpink , /tiktok2 , /tiktok9 , /pennywise , /russian , /shop , /enthused , /singing , /wrong , /guitar , /pinguin , /astronaut , /saunter , /flirt , /creepy , /watch , /revelation")
          
        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
            await self.highrise.send_whisper(user.id,"/tiktok10 , /tiktok8 , /cutey , /pose3 , /pose5 , /pose1 , /pose8 , /pose7  /pose9 , /cute , /superpose , /frog , /snake , /energyball , /maniac , /teleport , /float , /telekinesi , /fight , /wei , /fashion , /boxer , /bashful , /arabesque , /party")
          
        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
            await self.highrise.send_whisper(user.id,"/confused , /charging , /snowangel , /hot , /snowball , /curtsy , /bow ,/model , /greedy , /lust , /tired , /shy , /wave , /hello , /lau , /yes , /sad , /no , /kiss , /casual , /ren ,   /sit , /punk , /zombie , /gravity , /icecream ,/uwu , /sayso , /star")

        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
          await self.highrise.send_whisper(user.id,"/skating , /bitnervous , /scritchy , /timejump , /gottago , /jingle , /hyped , /sleigh , /surprise , /repose , /kawaii /touch , /pushit , /gift , /tiktok , /salute , /attention , /smooch , /launch")
        
        if        message.startswith("/lista") or         message.startswith("/emote list") or message.startswith("!emoteall") or message.startswith("!emote list") or message.startswith("!lista"):
            await self.highrise.send_emote("dance-floss")

        if        message.startswith("/peoples") or      message.startswith("!peoples"):
            room_users = (await self.highrise.get_room_users()).content
            await self.highrise.chat(f"There are {len(room_users)} people in the room  ")
            await self.highrise.send_emote("dance-floss")
                     
        if             message.startswith("!emotes") or message.startswith("/emotes"):
            await self.highrise.send_emote("emote-robot")
            await self.highrise.send_whisper(user.id,f"emotes available from number 1 to 97")

        if        message.startswith("Help") or      message.startswith("/help") or      message.startswith("!help") or message.startswith("help"):
            await self.highrise.chat(f"/lista | /pessoas | /emotes | | /marry me? | /play /fish /userinfo @ | !emoteall | !tele @ | !summon @ | !kick @ | !tele z,y,x | !tele @ z,y,x | ")
            await self.highrise.chat(f"[Emote] All | !emote all [Emote]")        
            await self.highrise.chat(f"{user.username} all activation codes must be used >> ! or/")
            await self.highrise.send_emote("dance-floss")
          
            
        if        message.startswith("/tp") or      message.startswith("!tp") or      message.startswith("tele") or          message.startswith("Tp") or          message.startswith("Tele") or  message.startswith("!tele"):
          target_username =         message.split("@")[-1].strip()
          await                     self.teleport_to_user(user, target_username)

        if                            message.startswith("Summon") or         message.startswith("Summom") or         message.startswith("!summom") or        message.startswith("/summom") or        message.startswith("/summon") or  message.startswith("!summon"):
          if user.username == "FallonXOXO" or user.username == "Its.Melly.Moo.XoXo" or user.username == "Shaun_Knox" or user.username == "sh1n1gam1699" or user.username == "Dreamy._.KY" or user.username == "hidinurbasement" or user.username == "@emping" or user.username == "_irii_" or user.username == "RayBM":
           target_username = message.split("@")[-1].strip()
           await self.teleport_user_next_to(target_username, user)
              
        if message.startswith("!kick"):
          if user.username == "FallonXOXO" or user.username == "RayBM":
              pass
          else:
              await self.highrise.chat("🤍.")
              return
          #separete message into parts
          parts = message.split()
          #check if message is valid "kick @username"
          if len(parts) != 2:
              await self.highrise.chat("🤍.")
              return
          #checks if there's a @ in the message
          if "@" not in parts[1]:
              username = parts[1]
          else:
              username = parts[1][1:]
          #check if user is in room
          room_users = (await self.highrise.get_room_users()).content
          for room_user, pos in room_users:
              if room_user.username.lower() == username.lower():
                  user_id = room_user.id
                  break
          if "user_id" not in locals():
              await self.highrise.chat("user not found, please fix the code coordinate ")
              return
          #kick user
          try:
              await self.highrise.moderate_room(user_id, "kick")
          except Exception as e:
              await self.highrise.chat(f"{e}")
              return
          #send message to chat
          await self.highrise.chat(f"{username} He was banned from the room!!")
          await check_and_start_emote_loop(user, message, self.highrise)

    async def teleport(self, user: User, position: Position):
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"Caught Teleport Error: {e}")

    async def teleport_to_user(self, user: User, target_username: str) -> None:
        try:
            room_users = await self.highrise.get_room_users()
            for target, position in room_users.content:
                if target.username.lower() == target_username.lower():
                    z = position.z
                    new_z = z - 1
                    await self.teleport(user, Position(position.x, position.y, new_z, position.facing))
                    break
        except Exception as e:
            print(f"An error occurred while teleporting to {target_username}: {e}")

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
          
    async def teleporter(self, message: str)-> None:
        """
            Teleports the user to the specified user or coordinate
            Usage: /teleport <username> <x,y,z>
                                                                """
        #separates the message into parts
        #part 1 is the command "/teleport"
        #part 2 is the name of the user to teleport to (if it exists)
        #part 3 is the coordinates to teleport to (if it exists)
        try:
            command, username, coordinate = message.split(" ")
        except:
            
            return
        
        #checks if the user is in the room
        room_users = (await self.highrise.get_room_users()).content
        for user in room_users:
            if user[0].username.lower() == username.lower():
                user_id = user[0].id
                break
        #if the user_id isn't defined, the user isn't in the room
        if "user_id" not in locals():
            
            return
            
        #checks if the coordinate is in the correct format (x,y,z)
        try:
            x, y, z = coordinate.split(",")
        except:
          
            return
        
        #teleports the user to the specified coordinate
        await self.highrise.teleport(user_id = user_id, dest = Position(float(x), float(y), float(z)))

    async def command_handler(self, user: User, message: str):
        parts = message.split(" ")
        command = parts[0][1:]
        functions_folder = "functions"
        # Check if the function exists in the module
        for file_name in os.listdir(functions_folder):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]  # Remove the '.py' extension
                module_path = os.path.join(functions_folder, file_name)
                
                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if the function exists in the module
                if hasattr(module, command) and callable(getattr(module, command)):
                    function = getattr(module, command)
                    await function(self, user, message)
        
        # If no matching function is found
        return        

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"{user.username} whispered: {message}")

        # Handle private messages for RayBM and botmes
        if user.username.lower() == "raybm" or user.username.lower() == "botmes":
            await self.highrise.chat(message)
            print(f"Broadcasted private message to the room: {message}")

        # ... (Your existing logic for other commands)

        if        message.startswith("tele") or              message.startswith("/tp") or              message.startswith("/fly") or     message.startswith("!tele") or      message.startswith("!tp") or     message.startswith("!fly"):
          if user.username == "FallonXOXO" or user.username == "Its.Melly.Moo.XoXo" or user.username == "sh1n1gam1699" or user.username == "Abbie_38" or user.username == "hidinurbasement" or user.username == "@emping" or user.username == "BabygirlFae"  or user.username == "RayBM":
            await self.teleporter(message)

        if        message.startswith("/") or              message.startswith("-") or              message.startswith(".") or          message.startswith("!"):
            await self.command_handler(user, message)

        if                            message.startswith("Summon") or         message.startswith("Summom") or         message.startswith("!summom") or        message.startswith("/summom") or        message.startswith("/summon") or  message.startswith("!summon"):
          if user.username == "FallonXOXO" or user.username == "Shaun_Knox" or user.username == "@Its.Melly.Moo.XoXo" or user.username == "@RayBM" or user.username == "Dreamy._.KY":
           target_username = message.split("@")[-1].strip()
           await self.teleport_user_next_to(target_username, user)

    async def on_user_move(self, user: User, pos: Position) -> None:
        print (f"{user.username} moved to {pos}")

    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        print(f"{user.username} emoted: {emote_id}")
