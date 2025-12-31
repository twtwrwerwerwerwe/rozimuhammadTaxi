import re
import asyncio
from telethon import TelegramClient, events

# =================== TELEGRAM API ===================
api_id = 28023612
api_hash = 'fe94ef46addc1b6b8253d5448e8511f0'
client = TelegramClient('taxi_session', api_id, api_hash)

# =================== SKIP CHAT ID ===================
SKIP_CHAT_IDS = {
    -1003398571650,
    -1002963614686
}

# =================== TARGET CHAT ID =================
TARGET_CHAT_IDS = [
    -1003398571650,
    -1002963614686
]

# =================== KEYWORDS (AS IS) ===============
KEYWORDS = [
    # odam bor
    'odam bor','odambor','odam bor ekan','odam bor edi','odam borakan',
    'bitta odam bor','ikkita odam bor','uchta odam bor',"to'rtta odam bor",'tortta odam bor',
    'komplek odam bor','komplekt odam bor','kompilek odam bor','kampilek odam bor',
    '1ta odam bor','2ta odam bor','3ta odam bor','4ta odam bor',
    'odam bor 1','odam bor 2','odam bor 3','odam bor 4',
    'rishtonga odam bor','toshkentga odam bor',"toshkendan farg'onaga odam bor",
    'тўрта одам бор','одам бор','комплект одам бор','компилект odam бор','кампилек одам бор',
    'towga 1kishi', 'toshkentga 1kishi', "farg'onaga 1kishi", 'rishtonga 1kishi', '1kishi bor',
    'towga 2kishi', 'toshkentga 2kishi', "farg'onaga 2kishi", 'rishtonga 2kishi', '2kishi bor',
    'towga 3kishi', 'toshkentga 3kishi', "farg'onaga 3kishi", 'rishtonga 3kishi', '3kishi bor',
    'towga 4kishi', 'toshkentga 4kishi', "farg'onaga 4kishi", 'rishtonga 4kishi', '4kishi bor',
    'машина бор','одам бор эди','одам бор экан','одам бор 1','одам бор 2','одам бор 3','одам бор 4',
    'битта одам бор','иккита одам бор','учта одам бор','комплек одам бор','1та одам бор','2та одам бор',
    '3та одам бор','4та одам бор', 'toshkentdan bir kishi', 'rishtonga bir kishi', '1 ta qiz bor', 'ayol kishi bor mashina sorashyabdi',
    'Chirchiqdan 1 kishi', 'Yangiyuldan 1 kishi', 'Zangiotadan 1 kishi', 'Qibraydan 1 kishi', '1 kishi bor',
    '2-ta odam bor', '2-kishi bor', '3-ta odam bor', '3-kishi bor', '4-ta odam bor', '4-kishi bor',
    '2-ta kishi bor', '3-ta kishi bor', '4-ta kishi bor', '2-ta ayolkishi bor', '3-ta ayolkishi bor', '4-ta ayolkishi bor', "odam.bor", 
    
    # mashina kerak
    'mashina kerak','mashina kere','mashina kerek','mashina kera','mashina keraa',
    'bagajli mashina kerak','bosh mashina kerak','bosh mashina bormi','boshi bormi',
    'mashina izlayapman','mashina topaman','mashina kerak edi',
    'машина керак','багажли машина керак','бош машина керак','машина кере','машina кераа',

    # pochta bor
    'pochta bor','pochta kerak','pochta ketadi','pochta olib ketadi','pochta bormi',
    'почта бор','почта кетади','почта керак','почта олиб кетади',
    'тошкентга почта бор','тошкентдан почта бор','риштонга почта бор','риштондан почта бор',

    # ketadi
    'ketadi','ketvotti','ketishi kerak',
    'кетяпт','кетвотди','кетади','кетишади','кетиши керак', "1kishi ekan", "2kishi ekan", "3kishi ekan", "4kishi ekan",
    "2 kishi ekan", "3 kishi ekan", "1 kishi ekan", "toshketga 1kishi", 

    # dostavka
    'dastavka bor','dostavka bor','dastafka','dastafka bor',
    'доставкa бор','даставка бор','доставка бор','доставкa керак',
    "Toshkentdan Rishtonga 1odam bor", '1odam bor', '1ta kamla', 'bitta kamlarga', '1ta kamlarga',
    '1 ta kamlarga', '2kiwimiz', "bagajga yuk bor", '2kishimiz', "2 kiwimiz", "2 kishimiz", "2kiwimiz", 
    "3kiwimiz", "3 kiwimiz", "3 kishimiz", "3kishimiz", "4kishimiz", "4kiwimiz", "4 kishimiz", "4 kiwimiz",
    "Toshkentga 1kishi", "Toshkenga 1kishi", "Rishtonga 1kishi", "Rishotondan 1kiwi", "poshta  bor", "moshina kerak",
    "ayollar bor mashina kerak", "ayollar bor moshina kerak", "Toshkentga 1ta odam bor", "1 ta qiz bola bor", "qiz bola bor",
    "1ta qiz bor", "1ta qiz bola bor", 'одам бор',
    'одам бор экан','одам бор эди','битта одам бор','иккита одам бор','учта одам бор','тўртта одам бор','1та одам бор','2та одам бор','3та одам бор','4та одам бор','одам бор 1','одам бор 2','одам бор 3','одам бор 4',

    'комплек одам бор','комплект одам бор','компилек одам бор','кампилек одам бор',

    'риштонга одам бор','тошкентга одам бор','тошкентдан фарғонага одам бор','тошкентга 1 киши','риштонга 1 киши','фарғонага 1 киши','1 киши бор','2 киши бор','3 киши бор','4 киши бор',
    'чирчиқдан 1 киши', 'янгийўлдан 1 киши', 'зангиотадан 1 киши', 'қибрайдан 1 киши',

    '1 та қиз бор', '1 та қиз бола бор', 'қиз бола бор', 'аёл киши бор машина сўрашяпти', 'аёллар бор машина керак',

    # mashina
    'машина керак', 'машина кере', 'машина керeк', 'багажли машина керак', 'машина излаяпман', 'мошина керак',

    # pochta / dostavka
    'почта бор', 'почта керак', 'почта олиб кетади', 'пошта бор', 'даставка бор', 'доставка бор',

    # ketadi
    'кетади', 'кетвотти', 'кетиши керак', "shopir kerak", "1kishi ayol kishili mashina kerak"
]

# 🔥 BIR MARTA KOMPILYATSIYA (ENG MUHIM)
KEYWORDS_RE = re.compile("|".join(KEYWORDS), re.IGNORECASE)

# =================== PHONE REGEX ====================
PHONE_RE = re.compile(r'(\+?998[\d\-\s\(\)]{9,15}|9\d{8})')

def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('998') and len(digits) >= 12:
        return '+' + digits[:12]
    if len(digits) == 9:
        return '+998' + digits
    return None

# =================== HANDLER ========================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # 🚀 1. ENG TEZ RETURNLAR
    if not (event.is_group or event.is_channel):
        return

    if event.chat_id in SKIP_CHAT_IDS:
        return

    text = event.raw_text
    if not text:
        return

    low = text.lower()

    # 🚀 2. BITTA REGEX — HAMMASI SHU YERDA
    if not KEYWORDS_RE.search(low):
        return

    # 🚀 3. FAQAT SHU YERDAN KEYIN await
    sender = await event.get_sender()
    chat = await event.get_chat()

    group_name = getattr(chat, 'title', 'Nomaʼlum guruh')
    if getattr(chat, 'username', None):
        link = f"https://t.me/{chat.username}/{event.id}"
        group_display = f"<a href='{link}'>{group_name}</a>"
    else:
        group_display = group_name

    username = getattr(sender, 'username', None)
    owner_display = f"@{username}" if username else "Berkitilgan"

    sender_id = getattr(sender, 'id', None)
    profile_link = (
        f"<a href='tg://user?id={sender_id}'>Profilga o‘tish</a>"
        if sender_id else "Berkitilgan"
    )

    phone = normalize_phone(sender.phone) if sender.phone else None
    if not phone and any(c.isdigit() for c in text):
        for m in PHONE_RE.finditer(text):
            phone = normalize_phone(m.group(0))
            if phone:
                break

    message = (
        f"🚖 <b>Yangi e’lon!</b>\n\n"
        f"📝 <b>Matn:</b>\n{text}\n\n"
        f"📍 <b>Guruh:</b> {group_display}\n\n"
        f"👤 <b>Egasi:</b> {owner_display}\n\n"
        f"📞 <b>Telefon:</b> {phone or 'Berkitilgan'}\n\n"
        f"🔗 <b>Profil:</b> {profile_link}"
    )

    await asyncio.gather(*(
        client.send_message(tid, message, parse_mode='html')
        for tid in TARGET_CHAT_IDS
    ))

    print("📨 Yuborildi:", group_name)

# =================== START ==========================
print("🚀 Taxi bot ULTRA SUPER TEZ rejimda ishga tushdi...")
client.start()
client.run_until_disconnected()
