import re
from telethon import TelegramClient, events
from telethon.tl.types import PeerChat, PeerChannel

# ================= TELEGRAM =================
api_id = 28023612
api_hash = 'fe94ef46addc1b6b8253d5448e8511f0'

client = TelegramClient('taxi_session', api_id, api_hash)

# ============= FILTRLANMAYDIGAN GURUHLAR =============
# ❗ BU YERGA FAQAT FILTR YO'Q BO'LADIGAN GURUH ID-LARINI YOZASIZ
SAFE_CHAT_IDS = {
    -1003398571650,
    -1002963614686,
}

# ============= XABAR YUBORILADIGAN GURUHLAR =============
TARGET_CHATS = [
    'https://t.me/+BFl15wH-PAswZTYy',
    'https://t.me/+wsoP192AA5w1ZWIy',
]

# ============= KEYWORDS =============
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
    '3та одам бор','4та одам бор', 'toshkentdan bir kishi', 'rishtonga bir kishi', '1 ta qiz bor', 'ayol kishi bor mashina sorashyabdi'
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
    'кетяпт','кетвотди','кетади','кетишади','кетиши керак',

    # dostavka
    'dastavka bor','dostavka bor','dastafka','dastafka bor',
    'доставкa бор','даставка бор','доставка бор','доставкa керак'
]

KEYWORDS_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

PHONE_RE = re.compile(r'(\+?998[\d\-\s\(\)]{9,15}|9\d{8})')

def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('998'):
        return '+' + digits[:12]
    if len(digits) == 9 and digits.startswith('9'):
        return '+998' + digits
    if len(digits) >= 9:
        return '+998' + digits[-9:]
    return None

# ================= HANDLER =================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # Chat IDni TO‘G‘RI OLAMIZ (asosiy muammo shu edi!)
        chat_id = event.chat_id
        text = event.raw_text

        # === 1) Agar guruh SAFE bo‘lsa → filtr yo‘q
        if chat_id not in SAFE_CHAT_IDS:
            # === Qolgan guruhlar → keyword bo‘lishi shart
            if not text or not KEYWORDS_RE.search(text):
                return

        # sender
        sender = await event.get_sender()
        chat = await event.get_chat()

        group_name = getattr(chat, 'title', 'Noma\'lum guruh')
        if getattr(chat, 'username', None):
            group_link = f"https://t.me/{chat.username}/{event.id}"
        else:
            group_link = group_name

        username = getattr(sender, 'username', None)
        haber_egasi = f"@{username}" if username else "Berkitilgan"

        sender_id = getattr(sender, 'id', None)
        profile_link = f"<a href='tg://user?id={sender_id}'>Profil</a>" if sender_id else "Berkitilgan"

        phone = getattr(sender, 'phone', None)
        phone = normalize_phone(phone) if phone else None

        if not phone:
            for m in PHONE_RE.finditer(text):
                phone = normalize_phone(m.group(0))
                if phone:
                    break
        phone = phone or "Raqam berkitilgan"

        msg = (
            f"🚖 <b>Xabar topildi!</b>\n\n"
            f"📄 <b>Matn:</b>\n{text}\n\n"
            f"📍 <b>Guruh:</b> {group_name} — {group_link}\n\n"
            f"👤 <b>Habar egasi:</b> {haber_egasi}\n\n"
            f"📞 <b>Raqam:</b> {phone}\n\n"
            f"🔗 <b>Profil:</b> {profile_link}\n\n"
            f"🔔 Yangi e'lonlar uchun kuzatib boring!"
        )

        for tg in TARGET_CHATS:
            await client.send_message(tg, msg, parse_mode='html')
            print(f"📨 Yuborildi → {tg}")

    except Exception as e:
        print("❌ Xatolik:", e)

# ================= START =================
client.start()
client.run_until_disconnected()
