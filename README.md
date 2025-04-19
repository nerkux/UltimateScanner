# Linux‑утилиты в Telegram‑боте

**Проект**: Обёртка для популярных консольных утилит Linux в виде Telegram‑бота  
**Автор**: @nerkux (участник Всероссийской олимпиады школьников)

---

## Описание

Данный проект объединяет несколько консольных утилит Linux (nmap, nikto, whois, fuzz‑сканер и т. д.) в одного удобного Telegram‑бота. Бот принимает команды от пользователя, запускает соответствующие инструменты на сервере и возвращает результаты прямо в чат.

---

## Функциональность

- Сканирование портов с помощью **nmap**  
- Поиск уязвимостей веб‑сервера через **nikto**  
- Сбор WHOIS‑информации домена  
- Fuzz‑тестирование HTTP‑эндпоинтов  
- Поддержка собственных списков субдоменов (`subdomains.txt`)  
- Кеширование результатов (`cache/`)  
- Интерактивные клавиатуры и состояния (модуль `modules/keyboards.py`, `modules/states.py`)  
- Шаблоны сообщений в формате JSON (`other/messages.json`)  
- Примеры запросов в `example.py`

---

## Требования

- Linux‑сервер (Debian/Ubuntu/CentOS и др.)  
- Python 3.8+  
- Установленные утилиты:
  - nmap
  - nikto
  - curl (или другая утилита для fuzz‑тестирования)
  - CyberChef-server running on 3000 port
- Telegram‑бот

---

## Установка

```
git clone https://github.com/nerkux/UltimateScanner
cd UltimateScanner
pip install -r requirements.txt
```
**Не забудьте обновить файл settings.json**

```
apt install docker.io -y
git clone https://github.com/gchq/CyberChef-server
cd CyberChef-server
docker build -t cyberchef-server .
docker run -it --rm --name=cyberchef-server -p 3000:3000 cyberchef-server &
python3 main.py
```

***Внимание!
На вашем хосте должны быть установлены такие утилиты как Nmap, Nikto и Wfuzz***
```
apt install nmap
apt install nikto
apt install wfuzz
```

