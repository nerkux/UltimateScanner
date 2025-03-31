from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.types import FSInputFile
import asyncio
import subprocess
from modules.keyboards import *
from modules.states import *
import http3
import random
import validators

# CONSTANTS

bot = Bot(token="token")
dp = Dispatcher()
logs = "logchatid"

def init():

    # ASYNC CONSTANTS

    nmap_image = FSInputFile("media/nmap.jpg")
    whois_image = FSInputFile("media/whois.png")
    nikto_image = FSInputFile("media/nikto.jpg")
    fuzz_image = FSInputFile("media/fuzz.png")
    chef_image = FSInputFile("media/chef.png")
    methods = ["toHex", "toBase64"]


    # MESSAGE_MENU

    @dp.message(Command("start", "menu"))
    async def cmd_start(message: types.Message, state: FSMContext):
        animation = FSInputFile("media/cat_start.gif")
        if types.Message:
            await bot.send_animation(message.chat.id, animation=animation,
            caption=f"Приветствуем, <b>{message.from_user.full_name}!</b>",
            parse_mode=ParseMode.HTML, reply_markup=kb.as_markup())  

    # NMAP

    @dp.callback_query(F.data == "nmap")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        await bot.send_photo(callback.message.chat.id, photo=nmap_image, caption=f"<b>Nmap</b> 👁\nВведите адрес сканируемого ресурса (IP или URL с указанием протокола) eg. https://", parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
        await state.set_state(BuildNmap.writing_ip)

    @dp.message(BuildNmap.writing_ip)
    async def ip_handler(message: types.Message, state: FSMContext):
        if validators.url(message.text) == True or validators.ipv4(message.text) == True and message.text != "127.0.0.1":
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            await bot.send_photo(message.from_user.id, photo=nmap_image, caption=f"<b>Nmap</b> 👁\nАдрес: {message.text}\nВведите параметры сканирования", parse_mode=ParseMode.HTML, reply_markup=nmap_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            # possibly checker ? ---
            await state.set_state(BuildNmap.writing_params)
            await state.update_data(adress=message.text, params="")
        else:
            await bot.send_message(message.chat.id, f"<b>Инвалид url ♿️</b>\n\nНе пытайся обмануть меня, Джонни)", parse_mode=ParseMode.HTML)
            await state.set_state(BuildNmap.writing_ip)

    @dp.message(BuildNmap.writing_params)
    async def nmap_param(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or ":" in message.text or "/" in message.text or "#" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            await bot.send_message(message.chat.id, f"<b>⛔️ Запрещено использовать спецсимволы!</b>\nВведите действительные параметры сканирования", parse_mode=ParseMode.HTML)
            await state.set_state(BuildNmap.writing_params)
        else:
            data = await state.get_data(); adress = data["adress"]; params = data["params"]
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            await bot.send_photo(message.from_user.id, photo=nmap_image, caption=f"<b>Nmap</b> 👁\nАдрес: {adress}\nПараметры: {message.text}", parse_mode=ParseMode.HTML, reply_markup=nmap_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{adress}\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            await state.update_data(params=message.text)

    @dp.callback_query(F.data == "start_nmap")
    async def start_nmap(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); adress = data["adress"].removeprefix("https://").replace("/", ""); params = data["params"]
        my_state = await state.get_state()
        if my_state != "BuildNmap:scanning":
            await state.set_state(BuildNmap.scanning)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            await bot.send_message(callback.message.chat.id, f"<b>🔎 Запускаю сканирование Nmap...</b>\n\nАдрес: {adress}\nПараметры: {params}\n\n<i>Это может занять несколько минут</i>", parse_mode=ParseMode.HTML)
            full_command = f"nmap {adress} {params}"
            result = subprocess.Popen(full_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            a = result.communicate()
            await bot.send_message(callback.message.chat.id, f"☑️ <b>Сканирование завершено!</b>\n⠀\n<blockquote>{''.join(a)}</blockquote>", parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildNmap:scanning":
            await bot.send_message(callback.message.chat.id, f"<b>⚠️ Сканирование уже запущено!</b>\nПожалуйста, подождите", parse_mode=ParseMode.HTML)

    # WHOIS

    @dp.callback_query(F.data == "whois")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        await bot.send_photo(callback.message.chat.id, photo=whois_image, caption=f"<b>Whois</b> 🔎\nВведите адрес сканируемого ресурса (IP или URL без указания протокола)", parse_mode=ParseMode.HTML)
        await state.set_state(BuildWhois.writing_ip)

    @dp.message(BuildWhois.writing_ip)
    async def ip_handler(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or ":" in message.text or "#" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            await bot.send_message(message.chat.id, f"<b>⛔️ Запрещено использовать спецсимволы!</b>\nВведите действительные параметры сканирования", parse_mode=ParseMode.HTML)
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
            await bot.send_message(callback.message.chat.id, f"<b>🔎 Запускаю сканирование Whois...</b>\n\nАдрес: {adress}\n\n<i>Это может занять несколько минут</i>", parse_mode=ParseMode.HTML)
            client = http3.AsyncClient()
            r = await client.get(f"http://ip-api.com/json/{adress}")
            builded = f"""Status: {r.json()["status"]}\nCountry: {r.json()["country"]}\nCountry code: {r.json()["countryCode"]}\nRegion name: {r.json()["regionName"]}\nCity: {r.json()["city"]}\nZip code: {r.json()["zip"]}\nLat: {r.json()["lat"]}\nLon: {r.json()["lon"]}\nTimezone: {r.json()["timezone"]}\nISP: {r.json()["isp"]}"""
            await bot.send_message(callback.message.chat.id, f"☑️ <b>Сканирование завершено!</b>\n⠀\n<blockquote>{builded}</blockquote>", parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildWhois:scanning":
            await bot.send_message(callback.message.chat.id, f"<b>⚠️ Сканирование уже запущено!</b>\nПожалуйста, подождите", parse_mode=ParseMode.HTML)
    
    # NIKTO

    @dp.callback_query(F.data == "nikto")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        await bot.send_photo(callback.message.chat.id, photo=nikto_image, caption=f"<b>Nikto</b> 🥷\nВведите адрес сканируемого ресурса (IP или URL c указанием протокола) eg. https://", parse_mode=ParseMode.HTML)
        await state.set_state(BuildNikto.writing_ip)

    @dp.message(BuildNikto.writing_ip)
    async def nikto_ip_handler(message: types.Message, state: FSMContext):
        if validators.url(message.text) == True or validators.ipv4(message.text) == True and message.text != "127.0.0.1":
            builded = message.text.removeprefix("https://")
            if "&" in builded or "|" in builded or ":" in builded or "#" in builded or chr(92) in builded or ";" in builded or ".py" in builded or ".json" in builded: 
                await bot.send_message(message.chat.id, f"<b>⛔️ Запрещено использовать спецсимволы!</b>\nВведите действительные параметры сканирования", parse_mode=ParseMode.HTML)
                await state.set_state(BuildNikto.writing_ip)
            else:
                await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
                await bot.send_photo(message.from_user.id, photo=nikto_image, caption=f"<b>Nikto</b> 🥷\nАдрес: {message.text}", parse_mode=ParseMode.HTML, reply_markup=nikto_kb.as_markup())
                await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
                await state.clear()
                await state.update_data(adress=message.text)
        else:
            await bot.send_message(message.chat.id, f"<b>Инвалид url ♿️</b>\nНе пытайся обмануть меня, Джонни", parse_mode=ParseMode.HTML)
            await state.set_state(BuildNikto.writing_ip)

    @dp.callback_query(F.data == "start_nikto")
    async def start_whois(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data(); adress = data["adress"]
        my_state = await state.get_state()
        if my_state != "BuildNikto:scanning":
            await state.set_state(BuildNikto.scanning)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            await bot.send_message(callback.message.chat.id, f"<b>🔎 Запускаю сканирование Nikto...</b>\nАдрес: {adress}\n\n<i>Это может занять несколько минут</i>", parse_mode=ParseMode.HTML)
            full_command = f"nikto -h {adress} -ssl -maxtime 30"
            nikto = subprocess.Popen(full_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            builded = nikto.communicate()
            await bot.send_message(callback.message.chat.id, f"☑️ <b>Сканирование завершено!</b>\n⠀\n<blockquote>{''.join(builded)}</blockquote>", parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildNikto:scanning":
            await bot.send_message(callback.message.chat.id, f"<b>⚠️ Сканирование уже запущено!</b>\nПожалуйста, подождите", parse_mode=ParseMode.HTML)

    # FUZZER

    @dp.callback_query(F.data == "fuzz")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        await bot.send_photo(callback.message.chat.id, photo=fuzz_image, caption=f"<b>Fuzzer</b> 🎯\nВведите адрес ресурса для фаззинга (IP или URL без https://)", parse_mode=ParseMode.HTML)
        await state.set_state(BuildFuzz.writing_ip)

    @dp.message(BuildFuzz.writing_ip)
    async def fuzzer_ip_handler(message: types.Message, state: FSMContext):
        if validators.url(message.text) == True or validators.ipv4(message.text) == True and message.text != "127.0.0.1":
            builded = message.text.removeprefix("https://").replace("/", "")
            if "&" in builded or "|" in builded or ":" in builded or "#" in builded or chr(92) in builded or ";" in builded or ".py" in builded or ".json" in builded: 
                await bot.send_message(message.chat.id, f"<b>⛔️ Запрещено использовать спецсимволы!</b>\nВведите действительные параметры сканирования", parse_mode=ParseMode.HTML)
                await state.set_state(BuildFuzz.writing_ip)
            else:
                await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
                await bot.send_photo(message.from_user.id, photo=fuzz_image, caption=f"<b>Fuzzer</b> 🎯\nАдрес: {message.text}", parse_mode=ParseMode.HTML, reply_markup=fuzz_kb.as_markup())
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
            await bot.send_message(callback.message.chat.id, f"<b>🔎 Запускаю фаззинг...</b>\n\nАдрес: {adress}\n\n<i>Это может занять несколько минут</i>", parse_mode=ParseMode.HTML)
            filename = f"{callback.message.chat.id}_{adress}_{random.randint(0, 9999999)}.log"
            full_command = f" wfuzz -w 'other/subdomains.txt' --sc 400,200 -f 'cache/{filename}' https://{adress}/FUZZ"
            fuzzer = subprocess.Popen(full_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            trigger = fuzzer.communicate()
            message_str = ""
            f = open(f"cache/{filename}", "r", encoding="utf-8")
            lines = f.read()
            f.close()
            await bot.send_message(callback.message.chat.id, f"☑️ <b>Сканирование завершено!</b>\n⠀\n<blockquote>{lines}</blockquote>", parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildFuzz:scanning":
            await bot.send_message(callback.message.chat.id, f"<b>⚠️ Сканирование уже запущено!</b>\n\nПожалуйста, подождите", parse_mode=ParseMode.HTML)

    # CyberChef

    @dp.callback_query(F.data == "chef")
    async def nmap_callback(callback: types.CallbackQuery, state: FSMContext):
        clapped = ""
        for i in methods:
            clapped+=f"{i}\n"
        await bot.send_photo(callback.message.chat.id, photo=chef_image, caption=f"<b>CyberChef</b> 👨‍🍳\nВведите желаемый метод преобразования:\n\n<blockquote><b>Доступные методы:</b>\n\n{clapped}</blockquote>", parse_mode=ParseMode.HTML)
        await state.set_state(BuildChef.writing_method)

    @dp.message(BuildChef.writing_method)
    async def cheff_method_handler(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            await bot.send_message(message.chat.id, f"<b>⛔️ Запрещено использовать спецсимволы!</b>\n\ведите действительные параметры сканирования", parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.writing_method)
        else:
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            await bot.send_photo(message.from_user.id, photo=chef_image, caption=f"<b>CyberChef</b> 👨‍🍳\nМетод: {message.text}\nВведите текст для преобразования", parse_mode=ParseMode.HTML, reply_markup=return_kb.as_markup())
            await bot.send_message(logs, f"<i>#лог #запрос</i>\n\n<blockquote>🧑‍💻 Юзер:\n<i>{message.from_user.full_name}\n@{message.from_user.username}</i></blockquote>\n\n<blockquote>Запрос:\n{message.text}</blockquote>", parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.writing_cipher)
            await state.update_data(chef_method=message.text)

    @dp.message(BuildChef.writing_cipher)
    async def chef_cipher(message: types.Message, state: FSMContext):
        if "&" in message.text or "|" in message.text or chr(92) in message.text or ";" in message.text or ".py" in message.text or ".json" in message.text: 
            await bot.send_message(message.chat.id, f"<b>⛔️ Запрещено использовать спецсимволы!</b>\nВведите действительные параметры сканирования", parse_mode=ParseMode.HTML)
            await state.set_state(BuildChef.writing_cipher)
        else:
            data = await state.get_data(); chef_method = data["chef_method"]
            await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1])
            await bot.send_photo(message.from_user.id, photo=chef_image, caption=f"<b>CyberChef</b> 👨‍🍳\nМетод: {chef_method}\nТекст для преобразования: {message.text}", parse_mode=ParseMode.HTML, reply_markup=chef_kb.as_markup())
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
            await bot.send_message(callback.message.chat.id, f"<b>⚙️ Запускаю преобразование текста...</b>\n\nМетод: {method}\nЗашифрованынй текст: {cipher}\n\n<i>Это может занять несколько минут</i>", parse_mode=ParseMode.HTML)
            # job
            request = {"input": cipher, "recipe": [{"op": method}]}
            chef_client = http3.AsyncClient()
            r = await chef_client.post("http://localhost:3000/bake", json=request)
            builded = eval(r.text)["value"]
            await bot.send_message(callback.message.chat.id, f"☑️ <b>Преобразование завершено!</b>\n⠀\n<blockquote>{''.join(builded)}</blockquote>", parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=return_kb.as_markup())
            await state.clear()
        elif my_state == "BuildChef.working":
            await bot.send_message(callback.message.chat.id, f"<b>⚠️ Преобразование уже запущено!</b>\n\nПожалуйста, подождите", parse_mode=ParseMode.HTML)

    # CALLBACK_MENU

    @dp.callback_query(F.data == 'home')
    async def return_home(callback: types.CallbackQuery):
        animation = FSInputFile("media/cat_start.gif")
        await bot.send_animation(callback.message.chat.id, animation=animation, caption=f"Приветствуем, <b>{callback.from_user.full_name}!</b>", parse_mode=ParseMode.HTML, reply_markup=kb.as_markup())  

    
    async def main():
        await dp.start_polling(bot)

    if __name__ == "__main__":
        asyncio.run(main())


init()


