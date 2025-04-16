from modules.lib import *

# CONSTANTS

bot = Bot(token="token")
dp = Dispatcher()

def init():

    # MESSAGES INIT

    with open('other/messages.json') as f:
        msg_text = json.load(f)

    # SETTINGS INIT

    with open('settings.json') as f:
        settings = json.load(f)
    logs = int(settings["log_channel"])
    if "," in settings["allowed_users"]:
        admins = settings["allowed_users"].split(", ")
    else:
        admins = settings["allowed_users"]

    # CONSTANTS

    nmap_image = FSInputFile("media/nmap.jpg")
    whois_image = FSInputFile("media/whois.png")
    nikto_image = FSInputFile("media/nikto.jpg")
    fuzz_image = FSInputFile("media/fuzz.png")
    chef_image = FSInputFile("media/chef.png")
    methods = ["toHex", "toBase64"]

    # CHECKER 
    
    async def checker(message: types.Message):
        if str(message.chat.id) not in admins:
            return False
        else:
            return True
        
    # MESSAGE MENU

    @dp.message(Command("start", "menu"))
    async def cmd_start(message: types.Message, state: FSMContext):
        if await checker(message) == True:
            animation = FSInputFile("media/cat_start.gif")
            if types.Message:
                greetings = eval(f"f'''{msg_text['greetings']}'''")
                await bot.send_animation(message.chat.id, animation=animation,
                caption= greetings,
                parse_mode=ParseMode.HTML, reply_markup=kb.as_markup())  

    # NMAP
    @dp.callback_query(F.data == "nmap")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        nmap_1 = eval(f"f'''{msg_text['nmap_1']}'''")
        await bot.send_photo(callback.message.chat.id, photo=nmap_image, caption=nmap_1, parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
        await state.set_state(BuildNmap.writing_ip)

    @dp.message(BuildNmap.writing_ip)
    async def ip_handler(message: types.Message, state: FSMContext):
        if validators.url(message.text) == True or validators.ipv4(message.text) == True and message.text != "127.0.0.1":
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            nmap_2 = eval(f"f'''{msg_text['nmap_2']}'''")
            await bot.send_photo(message.from_user.id, photo=nmap_image, caption=nmap_2, parse_mode=ParseMode.HTML, reply_markup=nmap_kb.as_markup())
            # possibly checker ? ---
            await state.set_state(BuildNmap.writing_params)
            await state.update_data(adress=message.text, params="")
        else:
            invalid = eval(f"f'''{msg_text['invalid']}'''")
            await bot.send_message(message.chat.id, invalid, parse_mode=ParseMode.HTML)
            await state.set_state(BuildNmap.writing_ip)

    @dp.message(BuildNmap.writing_params)
    async def nmap_param(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or ":" in message.text or "/" in message.text or "#" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            error = eval(f"f'''{msg_text['error']}'''")
            await bot.send_message(message.chat.id, error, parse_mode=ParseMode.HTML)
            await state.set_state(BuildNmap.writing_params)
        else:
            data = await state.get_data(); adress = data["adress"]; params = data["params"]
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            nmap_3 = eval(f"f'''{msg_text['nmap_3']}'''")
            await bot.send_photo(message.from_user.id, photo=nmap_image, caption=nmap_3, parse_mode=ParseMode.HTML, reply_markup=nmap_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{adress}\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            await state.update_data(params=message.text)

    @dp.callback_query(F.data == "start_nmap")
    async def start_nmap(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); adress = data["adress"].removeprefix("https://").replace("/", ""); params = data["params"]
        my_state = await state.get_state()
        if my_state != "BuildNmap:scanning":
            await state.set_state(BuildNmap.scanning)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            nmap_scan = eval(f"f'''{msg_text['nmap_scan']}'''")
            await bot.send_message(callback.message.chat.id, nmap_scan, parse_mode=ParseMode.HTML)
            full_command = f"nmap {adress} {params}"
            result = subprocess.Popen(full_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            a = result.communicate()
            nmap_complete = eval(f"f'''{msg_text['nmap_complete']}'''")
            await bot.send_message(callback.message.chat.id, nmap_complete, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildNmap:scanning":
            already_scanning = eval(f"f'''{msg_text['already_scanning']}'''")
            await bot.send_message(callback.message.chat.id, already_scanning, parse_mode=ParseMode.HTML)

    # WHOIS

    @dp.callback_query(F.data == "whois")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        whois_1 = eval(f"f'''{msg_text['whois_1']}'''")
        await bot.send_photo(callback.message.chat.id, photo=whois_image, caption=whois_1, parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
        await state.set_state(BuildWhois.writing_ip)

    @dp.message(BuildWhois.writing_ip)
    async def ip_handler(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or ":" in message.text or "#" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            error = eval(f"f'''{msg_text['error']}'''")
            await bot.send_message(message.chat.id, error, parse_mode=ParseMode.HTML)
            await state.set_state(BuildWhois.writing_ip)
        else:
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            await bot.send_photo(message.from_user.id, photo=whois_image, caption=f"<b>Whois</b> 🔎\nАдрес: {message.text}", parse_mode=ParseMode.HTML, reply_markup=whois_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            await state.clear()
            await state.update_data(adress=message.text)

    @dp.callback_query(F.data == "start_whois")
    async def start_whois(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); adress = data["adress"]
        my_state = await state.get_state()
        if my_state != "BuildWhois:scanning":
            await state.set_state(BuildWhois.scanning)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            whois_2 = eval(f"f'''{msg_text['whois_2']}'''")
            await bot.send_message(callback.message.chat.id, whois_2, parse_mode=ParseMode.HTML)
            client = http3.AsyncClient()
            r = await client.get(f"http://ip-api.com/json/{adress}")
            builded = f"""Status: {r.json()["status"]}\nCountry: {r.json()["country"]}\nCountry code: {r.json()["countryCode"]}\nRegion name: {r.json()["regionName"]}\nCity: {r.json()["city"]}\nZip code: {r.json()["zip"]}\nLat: {r.json()["lat"]}\nLon: {r.json()["lon"]}\nTimezone: {r.json()["timezone"]}\nISP: {r.json()["isp"]}"""
            whois_complete = eval(f"f'''{msg_text['whois_complete']}'''")
            await bot.send_message(callback.message.chat.id, whois_complete, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildWhois:scanning":
            already_scanning = eval(f"f'''{msg_text['already_scanning']}'''")
            await bot.send_message(callback.message.chat.id, already_scanning, parse_mode=ParseMode.HTML)
    
    # NIKTO

    @dp.callback_query(F.data == "nikto")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        nikto_1 = eval(f"f'''{msg_text['nikto_1']}'''")
        await bot.send_photo(callback.message.chat.id, photo=nikto_image, caption=nikto_1, parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
        await state.set_state(BuildNikto.writing_ip)

    @dp.message(BuildNikto.writing_ip)
    async def nikto_ip_handler(message: types.Message, state: FSMContext):
        if validators.url(message.text) == True or validators.ipv4(message.text) == True and message.text != "127.0.0.1":
            builded = message.text.removeprefix("https://")
            if "&" in builded or "|" in builded or ":" in builded or "#" in builded or chr(92) in builded or ";" in builded or ".py" in builded or ".json" in builded: 
                error = eval(f"f'''{msg_text['error']}'''")
                await bot.send_message(message.chat.id, error, parse_mode=ParseMode.HTML)
                await state.set_state(BuildNikto.writing_ip)
            else:
                await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
                nikto_2 = eval(f"f'''{msg_text['nikto_2']}'''")
                await bot.send_photo(message.from_user.id, photo=nikto_image, caption=nikto_2, parse_mode=ParseMode.HTML, reply_markup=nikto_kb.as_markup())
                await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
                await state.clear()
                await state.update_data(adress=message.text)
        else:
            invalid = eval(f"f'''{msg_text['invalid']}'''")
            await bot.send_message(message.chat.id, invalid, parse_mode=ParseMode.HTML)
            await state.set_state(BuildNikto.writing_ip)

    @dp.callback_query(F.data == "start_nikto")
    async def start_whois(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); adress = data["adress"]
        my_state = await state.get_state()
        if my_state != "BuildNikto:scanning":
            await state.set_state(BuildNikto.scanning)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            nikto_scan = eval(f"f'''{msg_text['nikto_scan']}'''")
            await bot.send_message(callback.message.chat.id, nikto_scan, parse_mode=ParseMode.HTML)
            full_command = f"nikto -h {adress} -ssl -maxtime 30"
            nikto = subprocess.Popen(full_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            builded = nikto.communicate()
            nikto_complete = eval(f"f'''{msg_text['nikto_complete']}'''")
            await bot.send_message(callback.message.chat.id, nikto_complete, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildNikto:scanning":
            already_scanning = eval(f"f'''{msg_text['already_scanning']}'''")
            await bot.send_message(callback.message.chat.id, already_scanning, parse_mode=ParseMode.HTML)

    # FUZZER

    @dp.callback_query(F.data == "fuzz")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        fuzzer_1 = eval(f"f'''{msg_text['fuzzer_1']}'''")
        await bot.send_photo(callback.message.chat.id, photo=fuzz_image, caption=fuzzer_1, parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
        await state.set_state(BuildFuzz.writing_ip)

    @dp.message(BuildFuzz.writing_ip)
    async def fuzzer_ip_handler(message: types.Message, state: FSMContext):
        if validators.url(message.text) == True or validators.ipv4(message.text) == True and message.text != "127.0.0.1":
            builded = message.text.removeprefix("https://").replace("/", "")
            if "&" in builded or "|" in builded or ":" in builded or "#" in builded or chr(92) in builded or ";" in builded or ".py" in builded or ".json" in builded: 
                error = eval(f"f'''{msg_text['error']}'''")
                await bot.send_message(message.chat.id, error, parse_mode=ParseMode.HTML)
                await state.set_state(BuildFuzz.writing_ip)
            else:
                await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
                fuzzer_2 = eval(f"f'''{msg_text['fuzzer_2']}'''")
                await bot.send_photo(message.from_user.id, photo=fuzz_image, caption=fuzzer_2, parse_mode=ParseMode.HTML, reply_markup=fuzz_kb.as_markup())
                await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
                await state.clear()
                await state.update_data(adress=message.text)

    @dp.callback_query(F.data == "start_fuzz")
    async def start_whois(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); adress = data["adress"].removeprefix("https://").replace("/", "")
        my_state = await state.get_state()
        if my_state != "BuildFuzz:scanning":
            await state.set_state(BuildFuzz.scanning)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            fuzzer_scan = eval(f"f'''{msg_text['fuzzer_scan']}'''")
            await bot.send_message(callback.message.chat.id, fuzzer_scan, parse_mode=ParseMode.HTML)
            filename = f"{callback.message.chat.id}_{adress}_{random.randint(0, 9999999)}.log"
            full_command = f" wfuzz -w 'other/subdomains.txt' --sc 400,200 -f 'cache/{filename}' https://{adress}/FUZZ"
            fuzzer = subprocess.Popen(full_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            trigger = fuzzer.communicate()
            message_str = ""
            f = open(f"cache/{filename}", "r", encoding="utf-8"); lines = f.read(); f.close()
            fuzzer_complete = eval(f"f'''{msg_text['fuzzer_complete']}'''")
            await bot.send_message(callback.message.chat.id, fuzzer_complete, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildFuzz:scanning":
            already_scanning = eval(f"f'''{msg_text['already_scanning']}'''")
            await bot.send_message(callback.message.chat.id, already_scanning, parse_mode=ParseMode.HTML)

    # CyberChef

    @dp.callback_query(F.data == "chef")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        clapped = ""
        for i in methods:
            clapped+=f"{i}\n"
        chef_1 = eval(f"f'''{msg_text['chef_1']}'''")
        await bot.send_photo(callback.message.chat.id, photo=chef_image, caption=chef_1, parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
        await state.set_state(BuildChef.writing_method)

    @dp.message(BuildChef.writing_method)
    async def cheff_method_handler(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            error = eval(f"f'''{msg_text['error']}'''")
            await bot.send_message(message.chat.id, error, parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.writing_method)
        else:
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            chef_2 = eval(f"f'''{msg_text['chef_2']}'''")
            await bot.send_photo(message.from_user.id, photo=chef_image, caption=chef_2, parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.writing_cipher)
            await state.update_data(chef_method=message.text)

    @dp.message(BuildChef.writing_cipher)
    async def chef_cipher(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            error = eval(f"f'''{msg_text['error']}'''")
            await bot.send_message(message.chat.id, error, parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.writing_cipher)
        else:
            data = await state.get_data(); chef_method = data["chef_method"]
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            chef_3 = eval(f"f'''{msg_text['chef_3']}'''")
            await bot.send_photo(message.from_user.id, photo=chef_image, caption=chef_3, parse_mode=ParseMode.HTML, reply_markup=chef_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{chef_method}\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.working)
            await state.update_data(cipher=message.text)

    @dp.callback_query(F.data == "start_chef")
    async def start_chef(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); method = data["chef_method"]; cipher=data["cipher"]
        my_state = await state.get_state()
        if my_state != "BuildChef.working":
            await state.set_state(BuildChef.working)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            chef_scan = eval(f"f'''{msg_text['chef_scan']}'''")
            await bot.send_message(callback.message.chat.id,chef_scan, parse_mode=ParseMode.HTML)
            # job
            request = {"input": cipher, "recipe": [{"op": method}]}
            chef_client = http3.AsyncClient()
            r = await chef_client.post("http://localhost:3000/bake", json=request)
            builded = eval(r.text)["value"]
            chef_complete = eval(f"f'''{msg_text['chef_complete']}'''")
            await bot.send_message(callback.message.chat.id, chef_complete, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildChef.working":
            already_scanning = eval(f"f'''{msg_text['already_scanning']}'''")
            await bot.send_message(callback.message.chat.id, already_scanning, parse_mode=ParseMode.HTML)

    # any message handler

    @dp.message()
    async def any_message_handler(message: types.Message):
        await asyncio.sleep(0.5)
        unknown = eval(f"f'''{msg_text['unknown']}'''")
        await message.reply(unknown, parse_mode=ParseMode.HTML)

    # CALLBACK_MENU

    @dp.callback_query(F.data == 'home')
    async def return_home(callback: types.CallbackQuery, state: FSMContext):
        await state.clear()
        animation = FSInputFile("media/cat_start.gif")
        greetings = eval(f"f'''{msg_text['greetings_callback']}'''")
        await bot.send_animation(callback.message.chat.id, animation=animation, caption=greetings, parse_mode=ParseMode.HTML, reply_markup=kb.as_markup())  

    
    async def main():
        await dp.start_polling(bot)

    if __name__ == "__main__":
        asyncio.run(main())


init()
