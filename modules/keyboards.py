from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from modules.states import *
import json

with open('settings.json') as f:
        settings = json.load(f)

kb = InlineKeyboardBuilder()
kb.add(types.InlineKeyboardButton(text="Nmap 👁", callback_data="nmap"))
kb.add(types.InlineKeyboardButton(text="Whois 🔎", callback_data="whois"))
kb.add(types.InlineKeyboardButton(text="Nikto 🥷", callback_data="nikto"))
kb.row(types.InlineKeyboardButton(text="Fuzzer 🎯", callback_data="fuzz"))
kb.add(types.InlineKeyboardButton(text="CyberChef 👨‍🍳", callback_data="chef"))
kb.row(types.InlineKeyboardButton(text="Тех. поддержка 👨‍💻", url=settings["owner"]))

nmap_kb = InlineKeyboardBuilder()
nmap_kb.row(types.InlineKeyboardButton(text="Начать сканирование 🛡", callback_data="start_nmap"))

whois_kb = InlineKeyboardBuilder()
whois_kb.row(types.InlineKeyboardButton(text="Начать сканирование 🛡", callback_data="start_whois"))

nikto_kb = InlineKeyboardBuilder()
nikto_kb.row(types.InlineKeyboardButton(text="Начать сканирование 🛡", callback_data="start_nikto"))

fuzz_kb = InlineKeyboardBuilder()
fuzz_kb.row(types.InlineKeyboardButton(text="Начать фаззинг 🛡", callback_data="start_fuzz"))

chef_kb = InlineKeyboardBuilder()
chef_kb.row(types.InlineKeyboardButton(text="Преобразовать ⚙️", callback_data="start_chef"))

return_kb = InlineKeyboardBuilder()
return_kb.row(types.InlineKeyboardButton(text="В главное меню 🏠", callback_data="home"))

contact_kb = InlineKeyboardBuilder()
contact_kb.row(types.InlineKeyboardButton(text="Связь с владельцем 🧰", url=settings["owner"]))
