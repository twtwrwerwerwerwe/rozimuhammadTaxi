import re
import asyncio
from telethon import TelegramClient, events

# =================== TELEGRAM API ===================
api_id = 28023612
api_hash = 'fe94ef46addc1b6b8253d5448e8511f0'

client = TelegramClient('taxi_session', api_id, api_hash)

# =================== SKIP CHAT ID ===================
SKIP_CHAT_IDS = [
    -1003398571650,
    -1002963614686
]

# =================== TARGET CHAT ID ===================
TARGET_CHAT_IDS = [
    -1003398571650,
    -1002963614686
]

# =================== KALIT SO‘ZLAR ===================
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
    "2 kishi ekan", "3 kishi ekan", "1 kishi ekan", "toshketga 1kishi", "toshkenda odam bor",

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
    'кетади', 'кетвотти', 'кетиши керак', "shopir kerak", "1kishi ayol kishili mashina kerak", 
    "gazalkentdan 1kishi", "g'azalkentdan 1kishi", "gazalkentdan 2kishi", "g'azalkantdan 2 kishi",
    "o'zimizdan 1kishi", "ozimizdan 1kishi", "ozimizdan 2 kishi", "ozimizdan kim bor", "o'zimizdan kim bor",
    "yengil mashina kerak", "amirsoydan 1kishi", "qoqonga 1kishi", "kim yurapti akalar", "pustoy mashina kerak",
    "kobalt kerak", "jentra kerak", "bosh mashina bormi", "uchkoprikda 1kishi", "uchkoprikdan 1kishi", "chirchiqdan 1kishi",
    "yangiqorgondan 1kishi", "tashkentdan rishtonga odam bor", "toshkendan bog'dodga odam bor", "toshkentdan bagdodga odam bor",
    "4 odam bor", "2ta ayol bor", "katta yoshli ayol bor", "bir qiz bir bola bor", "srochni yuradigan taxi kerak",
    "kim yuryabdi", "toshkentga ketaman", "bagdodga ketishi kerak", "bagdodan 1kishi bor", "bog'doddan 2kishi",
    'кетади', 'кетвотти', 'кетиши керак', "шопир керак", "1киши аёл кишили машина керак",
    "газалкентдан 1киши", "ғазалкентдан 1киши", "газалкентдан 2киши", "ғазалкентдан 2 киши",
    "ўзимиздан 1киши", "озимиздан 1киши", "озимиздан 2 киши", "озимиздан ким бор", "ўзимиздан ким бор",
    "енгил машина керак", "амирсойдан 1киши", "қўқонга 1киши", "ким юрапти акалар", "пустой машина керак",
    "кобальт керак", "джентра керак", "бош машина борми", "учкўприкда 1киши", "учкўприкдан 1киши", "чирчиқдан 1киши",
    "янгиқўрғондан 1киши", "ташкентдан риштонга одам бор", "тошкентдан боғдодга одам бор", "тошкентдан бағдодга одам бор",
    "4 одам бор", "2та аёл бор", "катта ёшли аёл бор", "бир қиз бир бола бор", "срочни юрадиган такси керак",
    "ким юряпти", "тошкентга кетаман", "бағдодга кетиши керак", "бағдодан 1киши бор", "боғдоддан 2киши",
    "qoqonga odam bor", "qoqondan odam bor", "ertagaga qoqonga 1kishi", "fargonadan 1kishi", 'fargonaga odam bor',
    "fargonaga kim yuryabdi", "fargonaga 2kishi", "қўқонга одам бор", "қўқондан одам бор", "эртагага қўқонга 1киши", "фарғонадан 1киши", 'фарғонага одам бор',
    "фарғонага ким юряпти", "фарғонага 2киши"
]

KEYWORDS_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# =================== TELEFON REGEX ===================
PHONE_RE = re.compile(r'(\+?998[\d\-\s\(\)]{9,15}|9\d{8})')


def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('998') and len(digits) >= 12:
        return '+' + digits[:12]
    if len(digits) == 9:
        return '+998' + digits
    return None


# =================== HANDLER ===================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # 🔥 FAQAT SEN ULANGAN GURUH VA KANALLAR
        if not (event.is_group or event.is_channel):
            return

        chat_id = event.chat_id
        if chat_id in SKIP_CHAT_IDS:
            return

        text = event.raw_text
        if not text or not KEYWORDS_RE.search(text):
            return

        chat, sender = await asyncio.gather(
            event.get_chat(),
            event.get_sender()
        )

        group_name = getattr(chat, 'title', 'Nomaʼlum guruh')
        if getattr(chat, 'username', None):
            group_link = f"https://t.me/{chat.username}/{event.id}"
            group_display = f"<a href='{group_link}'>{group_name}</a>"
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
        if not phone:
            for m in PHONE_RE.finditer(text):
                phone = normalize_phone(m.group(0))
                if phone:
                    break

        phone_display = phone if phone else "Berkitilgan"

        message_text = (
            f"🚖 <b>Yangi e’lon!</b>\n\n"
            f"📝 <b>Matn:</b>\n{text}\n\n"
            f"📍 <b>Guruh:</b> {group_display}\n\n"
            f"👤 <b>Egasi:</b> {owner_display}\n\n"
            f"📞 <b>Telefon:</b> {phone_display}\n\n"
            f"🔗 <b>Profilga o'tish:</b> {profile_link}"
        )

        for target_id in TARGET_CHAT_IDS:
            await client.send_message(
                target_id,
                message_text,
                parse_mode='html'
            )
            print(f"📨 Yuborildi → {target_id}")

    except Exception as e:
        print("❌ Xatolik:", e)


# =================== START ===================
print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()