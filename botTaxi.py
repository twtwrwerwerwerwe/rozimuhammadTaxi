import re
import time
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat, User

# =================== TELEGRAM API ===================
api_id = 28023612
api_hash = 'fe94ef46addc1b6b8253d5448e8511f0'

# sequential_updates=False -> Telethon bir nechta kelgan xabarni ketma-ket emas,
# balki bir vaqtda (parallel) qayta ishlaydi. Bu botni sezilarli tezlashtiradi,
# chunki guruhlar ko'p bo'lganda xabarlar navbatda kutib turmaydi.
client = TelegramClient(
    'taxi_session',
    api_id,
    api_hash,
    sequential_updates=False,
)

# =================== SKIP CHAT ID ===================
# Ushbu guruh/kanallardagi xabarlar hech qachon tekshirilmaydi.
SKIP_CHAT_IDS = [
    -1003398571650,
    -1002963614686,
    -1003322681147
]

# =================== TARGET CHAT ID ===================
# Topilgan e'lonlar shu guruh(lar)ga yuboriladi.
TARGET_CHAT_IDS = [
    -1003398571650,
    -1002963614686
]

# =================== KALIT SO'ZLAR (LOTIN + KIRILL) ===================
# Har bir kategoriya ostida avval qo'lda yozilgan so'zlar, keyin esa
# ularning lotin->kirill (o'zbekcha-kirill) avtomatik yozilishi keladi.

# --- ODAM / KISHI / QIZ / AYOL BOR ---
KEYWORDS_BASE_ODAM_BOR = [
    '1 kishi bor', '1 kishi bor edi', '1 kishi bor ekan', '1 kishi ekan', '1 ta qiz bola bor',
    '1 ta qiz bor', '1 киши бор', '1 та қиз бола бор', '1 та қиз бор',
    '1kishi ayol kishili mashina kerak', '1kishi bor', '1kishi ekan', '1odam bor', '1ta odam bor',
    '1ta qiz bola bor', '1ta qiz bor', '1киши аёл кишили машина керак', '1та одам бор',
    '2 kishi bor edi', '2 kishi bor ekan', '2 kishi ekan', '2 kishimiz', '2 киши бор',
    '2-kishi bor', '2-ta ayolkishi bor', '2-ta kishi bor', '2-ta odam bor', '2kishi bor',
    '2kishi ekan', '2kishimiz', '2ta ayol bor', '2ta odam bor', '2та аёл бор', '2та одам бор',
    '3 kishi bor edi', '3 kishi bor ekan', '3 kishi ekan', '3 kishimiz', '3 киши бор',
    '3-kishi bor', '3-ta ayolkishi bor', '3-ta kishi bor', '3-ta odam bor', '3kishi bor',
    '3kishi ekan', '3kishimiz', '3ta odam bor', '3та одам бор', '4 kishi bor edi',
    '4 kishi bor ekan', '4 kishimiz', '4 odam bor', '4 киши бор', '4 одам бор', '4-kishi bor',
    '4-ta ayolkishi bor', '4-ta kishi bor', '4-ta odam bor', '4kishi bor', '4kishi ekan',
    '4kishimiz', '4ta odam bor', '4та одам бор', 'amirsoydan 1kishi',
    'ayol kishi bor mashina sorashyabdi', 'ayollar bor mashina kerak', 'ayollar bor moshina kerak',
    'bagdodan 1kishi bor', 'bir qiz bir bola bor', 'bitta odam bor', "bog'doddan 2kishi",
    'Chirchiqdan 1 kishi', 'chirchiqdan 1kishi', 'ertagaga qoqonga 1kishi', "farg'onaga 1kishi",
    "farg'onaga 2kishi", "farg'onaga 3kishi", "farg'onaga 4kishi", 'fargonadan 1kishi',
    'fargonaga 2kishi', 'fargonaga odam bor', "g'azalkantdan 2 kishi", "g'azalkentdan 1kishi",
    'gazalkentdan 1kishi', 'gazalkentdan 2kishi', 'ikkita odam bor', 'kampilek odam bor',
    'katta yoshli ayol bor', 'kompilek odam bor', 'komplek odam bor', 'komplekt odam bor',
    "o'zimizdan 1kishi", 'odam bor', 'odam bor 1', 'odam bor 2', 'odam bor 3', 'odam bor 4',
    'odam bor edi', 'odam bor ekan', 'odam borakan', 'odam.bor', 'odambor', 'ozimizdan 1kishi',
    'ozimizdan 2 kishi', 'Qibraydan 1 kishi', 'qiz bola bor', 'qoqondan odam bor',
    'qoqonga 1kishi', 'qoqonga odam bor', 'rishtonga 1kishi', 'rishtonga 1kishi bor',
    'rishtonga 2kishi', 'rishtonga 3kishi', 'rishtonga 4kishi', 'rishtonga bir kishi',
    'rishtonga odam bor', 'tashkentdan rishtonga odam bor', "to'rtta odam bor", 'tortta odam bor',
    'toshkenda odam bor', "toshkendan bog'dodga odam bor", "toshkendan farg'onaga odam bor",
    'Toshkenga 1kishi', 'toshkenga 1kishi bor', 'toshkentdan 1 kishi bering degan',
    'toshkentdan 1 kishi bering deganga', 'toshkentdan 2 kishi bering degan',
    'toshkentdan 2 kishi bering deganga', 'toshkentdan 3 kishi bering degan',
    'toshkentdan 3 kishi bering deganga', 'toshkentdan 4 kishi bering degan',
    'toshkentdan 4 kishi bering deganga', 'toshkentdan bagdodga odam bor', 'toshkentdan bir kishi',
    'Toshkentdan Rishtonga 1odam bor', 'toshkentga 1kishi', 'toshkentga 1kishi bor',
    'Toshkentga 1ta odam bor', 'toshkentga 2kishi', 'toshkentga 3kishi', 'toshkentga 4kishi',
    'toshkentga odam bor', 'toshketga 1kishi', 'towga 1kishi', 'towga 2kishi', 'towga 3kishi',
    'towga 4kishi', 'uchkoprikda 1kishi', 'uchkoprikdan 1kishi', 'uchta odam bor',
    'yangiqorgondan 1kishi', 'Yangiyuldan 1 kishi', 'Zangiotadan 1 kishi', 'амирсойдан 1киши',
    'аёл киши бор машина сўрашяпти', 'аёллар бор машина керак', 'бағдодан 1киши бор',
    'бир қиз бир бола бор', 'битта одам бор', 'боғдоддан 2киши', 'газалкентдан 1киши',
    'газалкентдан 2киши', 'зангиотадан 1 киши', 'иккита одам бор', 'кампилек одам бор',
    'катта ёшли аёл бор', 'компилек одам бор', 'компилект odam бор', 'комплек одам бор',
    'комплект одам бор', 'одам бор', 'одам бор 1', 'одам бор 2', 'одам бор 3', 'одам бор 4',
    'одам бор эди', 'одам бор экан', 'озимиздан 1киши', 'озимиздан 2 киши', 'риштонга 1 киши',
    'риштонга одам бор', 'ташкентдан риштонга одам бор', 'тошкентга 1 киши', 'тошкентга одам бор',
    'тошкентдан бағдодга одам бор', 'тошкентдан боғдодга одам бор',
    'тошкентдан фарғонага одам бор', 'тўрта одам бор', 'тўртта одам бор', 'учкўприкда 1киши',
    'учкўприкдан 1киши', 'учта одам бор', 'фарғонага 1 киши', 'фарғонага 2киши',
    'фарғонага одам бор', 'фарғонадан 1киши', 'чирчиқдан 1 киши', 'чирчиқдан 1киши',
    'эртагага қўқонга 1киши', 'янгийўлдан 1 киши', 'янгиқўрғондан 1киши', 'ўзимиздан 1киши',
    'ғазалкентдан 1киши', 'ғазалкентдан 2 киши', 'қибрайдан 1 киши', 'қиз бола бор',
    'қўқонга 1киши', 'қўқонга одам бор', 'қўқондан одам бор',
]

# --- MASHINA / MOSHINA KERAK ---
KEYWORDS_BASE_MASHINA_KERAK = [
    'bagajli mashina kerak', 'bosh mashina bormi', 'bosh mashina kerak', 'jentra kerak',
    'kobalt kerak', 'mashina izlayapman', 'mashina kera', 'mashina keraa', 'mashina kerak',
    'mashina kerak edi', 'mashina kere', 'mashina kerek', 'mashina topaman', 'moshina kerak',
    'pustoy mashina kerak', 'yengil mashina kerak', 'багажли машина керак', 'бош машина борми',
    'бош машина керак', 'джентра керак', 'енгил машина керак', 'машина бор', 'машина излаяпман',
    'машина керeк', 'машина керак', 'машина кере', 'мошина керак', 'пустой машина керак',
]

# --- POCHTA / DOSTAVKA ---
KEYWORDS_BASE_POCHTA_DOSTAVKA = [
    'dastafka', 'dastafka bor', 'dastavka bor', 'dostavka bor', 'pochta bor', 'pochta bormi',
    'pochta kerak', 'pochta ketadi', 'pochta olib ketadi', 'даставка бор', 'доставка бор',
    'почта бор', 'почта керак', 'почта кетади', 'почта олиб кет', 'почта олиб кетади', 'пошта бор',
    'риштонга почта бор', 'риштондан почта бор', 'тошкентга почта бор', 'тошкентдан почта бор',
]

# --- KETADI / KETMOQCHI ---
KEYWORDS_BASE_KETADI_BOSHQA = [
    'bagdodga ketishi kerak', 'ketadi', 'ketishi kerak', 'ketvotti', 'toshkentga ketaman',
    'бағдодга кетиши керак', 'кетади', 'кетвотти', 'кетиши керак', 'тошкентга кетаман',
]

# --- BOSHQA KALIT SO'ZLAR ---
KEYWORDS_BASE_BOSHQA = [
    '1 kiwi bor edi', '1 kiwi bor ekan', '1 ta kamlarga', '1ta kamla', '1ta kamlarga',
    '2 kiwi bor edi', '2 kiwi bor ekan', '2 kiwimiz', '2kiwimiz', '3 kiwi bor edi',
    '3 kiwi bor ekan', '3 kiwimiz', '3kiwimiz', '4 kiwi bor edi', '4 kiwi bor ekan', '4 kiwimiz',
    '4kiwimiz', 'bagajga yuk bor', "birinchi so'raganga", 'bitta kamlarga', 'boshi bormi',
    'fargonaga kim yuryabdi', 'kim yurapti akalar', 'kim yuryabdi', "o'zimizdan kim bor",
    'ozimizdan kim bor', 'poshta  bor', 'Rishotondan 1kiwi', 'rishotondan 1kiwi bor',
    'shopir kerak', 'srochni kim yuryabdi', 'srochni yuradigan taxi kerak',
    'toshkentdan 1 kiwi bering degan', 'toshkentdan 1 kiwi bering deganga',
    'toshkentdan 2 kiwi bering deganga', 'toshkentdan 3 kiwi bering deganga',
    'toshkentdan 4 kiwi bering deganga', 'yuk bor', 'yuradiganla bormi', 'yuradiganlar bormi',
    'yurayotganla bomi', 'yurayotganla bormi', 'yurayotganlar bomi', 'yurayotganlar bormi',
    'yurediganla bormi', 'yurediganlar bomi', 'yurediganlar bormi', 'доставкa бор',
    'доставкa керак', 'кетвотди', 'кетишади', 'кетяпт', 'ким юрапти акалар', 'ким юряпти',
    'кобальт керак', 'машina кераа', 'озимиздан ким бор', 'срочни юрадиган такси керак',
    'фарғонага ким юряпти', 'шопир керак', 'юрадиганла борми', 'юрадиганлар борми',
    'юраётганла боми', 'юраётганла борми', 'юраётганлар боми', 'юраётганлар борми',
    'юредигaнла борми', 'юредигaнлар боми', 'юредигaнлар борми', 'ўзимиздан ким бор',
]

KEYWORDS_BASE = (
    KEYWORDS_BASE_ODAM_BOR +
    KEYWORDS_BASE_MASHINA_KERAK +
    KEYWORDS_BASE_POCHTA_DOSTAVKA +
    KEYWORDS_BASE_KETADI_BOSHQA +
    KEYWORDS_BASE_BOSHQA
)
# Quyidagilar - yuqoridagi lotincha so'zlarning kirillcha (o'zbek-kirill)
# ko'rinishi, avtomatik harf-ma-harf o'giril(transliteratsiya qilin)gan va
# faqat mavjud bo'lmagan (hali ro'yxatda yo'q) so'zlargina qo'shilgan.

# --- ODAM / KISHI / QIZ / AYOL BOR — kirillcha ---
KEYWORDS_TRANSLIT_ODAM_BOR = [
    '1 киши бор еди', '1 киши бор екан', '1 киши екан', '1киши бор', '1киши екан', '1одам бор',
    '1та қиз бола бор', '1та қиз бор', '2 киши бор еди', '2 киши бор екан', '2 киши екан',
    '2 кишимиз', '2-киши бор', '2-та аёлкиши бор', '2-та киши бор', '2-та одам бор', '2киши бор',
    '2киши екан', '2кишимиз', '3 киши бор еди', '3 киши бор екан', '3 киши екан', '3 кишимиз',
    '3-киши бор', '3-та аёлкиши бор', '3-та киши бор', '3-та одам бор', '3киши бор', '3киши екан',
    '3кишимиз', '4 киши бор еди', '4 киши бор екан', '4 кишимиз', '4-киши бор', '4-та аёлкиши бор',
    '4-та киши бор', '4-та одам бор', '4киши бор', '4киши екан', '4кишимиз',
    'аёл киши бор машина сорашябди', 'аёллар бор мошина керак', 'багдодан 1киши бор',
    'ертагага қоқонга 1киши', 'одам бор еди', 'одам бор екан', 'одам боракан', 'одам.бор',
    'одамбор', 'риштонга 1киши', 'риштонга 1киши бор', 'риштонга 2киши', 'риштонга 3киши',
    'риштонга 4киши', 'риштонга бир киши', 'тоwга 1киши', 'тоwга 2киши', 'тоwга 3киши',
    'тоwга 4киши', 'тортта одам бор', 'тошкенга 1киши', 'тошкенга 1киши бор', 'тошкенда одам бор',
    'тошкендан боғдодга одам бор', 'тошкендан фарғонага одам бор', 'тошкентга 1киши',
    'тошкентга 1киши бор', 'тошкентга 1та одам бор', 'тошкентга 2киши', 'тошкентга 3киши',
    'тошкентга 4киши', 'тошкентдан 1 киши беринг деган', 'тошкентдан 1 киши беринг деганга',
    'тошкентдан 2 киши беринг деган', 'тошкентдан 2 киши беринг деганга',
    'тошкентдан 3 киши беринг деган', 'тошкентдан 3 киши беринг деганга',
    'тошкентдан 4 киши беринг деган', 'тошкентдан 4 киши беринг деганга',
    'тошкентдан багдодга одам бор', 'тошкентдан бир киши', 'тошкентдан риштонга 1одам бор',
    'тошкетга 1киши', 'учкоприкда 1киши', 'учкоприкдан 1киши', 'фаргонага 2киши',
    'фаргонага одам бор', 'фаргонадан 1киши', 'фарғонага 1киши', 'фарғонага 3киши',
    'фарғонага 4киши', 'янгиюлдан 1 киши', 'янгиқоргондан 1киши', 'ғазалкантдан 2 киши',
    'қоқонга 1киши', 'қоқонга одам бор', 'қоқондан одам бор',
]

# --- MASHINA / MOSHINA KERAK — kirillcha ---
KEYWORDS_TRANSLIT_MASHINA_KERAK = [
    'жентра керак', 'йенгил машина керак', 'кобалт керак', 'машина кера', 'машина кераа',
    'машина керак еди', 'машина керек', 'машина топаман',
]

# --- POCHTA / DOSTAVKA — kirillcha ---
KEYWORDS_TRANSLIT_POCHTA_DOSTAVKA = [
    'дастафка', 'дастафка бор', 'почта борми',
]

# --- KETADI / KETMOQCHI — kirillcha ---
KEYWORDS_TRANSLIT_KETADI_BOSHQA = [
    'багдодга кетиши керак',
]

# --- BOSHQA KALIT SO'ZLAR — kirillcha ---
KEYWORDS_TRANSLIT_BOSHQA = [
    '1 киwи бор еди', '1 киwи бор екан', '1 та камларга', '1та камла', '1та камларга',
    '2 киwи бор еди', '2 киwи бор екан', '2 киwимиз', '2киwимиз', '3 киwи бор еди',
    '3 киwи бор екан', '3 киwимиз', '3киwимиз', '4 киwи бор еди', '4 киwи бор екан', '4 киwимиз',
    '4киwимиз', 'багажга юк бор', 'биринчи сўраганга', 'битта камларга', 'боши борми',
    'ким юрябди', 'ришотондан 1киwи', 'ришотондан 1киwи бор', 'срочни ким юрябди',
    'срочни юрадиган тахи керак', 'тошкентдан 1 киwи беринг деган',
    'тошкентдан 1 киwи беринг деганга', 'тошкентдан 2 киwи беринг деганга',
    'тошкентдан 3 киwи беринг деганга', 'тошкентдан 4 киwи беринг деганга', 'фаргонага ким юрябди',
    'юк бор', 'юредиганла борми', 'юредиганлар боми', 'юредиганлар борми',
]

KEYWORDS_TRANSLIT = (
    KEYWORDS_TRANSLIT_ODAM_BOR +
    KEYWORDS_TRANSLIT_MASHINA_KERAK +
    KEYWORDS_TRANSLIT_POCHTA_DOSTAVKA +
    KEYWORDS_TRANSLIT_KETADI_BOSHQA +
    KEYWORDS_TRANSLIT_BOSHQA
)

# Ikkala ro'yxatni (lotincha + kirillcha) birlashtiramiz va aniq takrorlarni olib tashlaymiz.
KEYWORDS = list(dict.fromkeys(KEYWORDS_BASE + KEYWORDS_TRANSLIT))

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


def get_username(user):
    """Foydalanuvchi username'ini qaytaradi.

    Telegram endi bitta akkauntda bir nechta username bo'lishiga ruxsat beradi.
    Bunday hollarda eski `.username` maydoni bo'sh (None) bo'lib qolishi mumkin,
    lekin haqiqiy username `.usernames` ro'yxatida turadi. Aynan shu sabab
    ba'zida username bor bo'lsa ham bot uni "Berkitilgan" deb ko'rsatgan.
    """
    uname = getattr(user, 'username', None)
    if uname:
        return uname
    usernames = getattr(user, 'usernames', None)
    if usernames:
        for u in usernames:
            if getattr(u, 'username', None):
                return u.username
    return None


def build_message_link(chat_id, chat_username, msg_id):
    """Xabarga to'g'ridan-to'g'ri o'tadigan havolani tuzadi.

    - Ochiq (username'li) guruh/kanal bo'lsa -> https://t.me/username/msg_id
    - Yopiq (username'siz) super-guruh/kanal bo'lsa -> https://t.me/c/ID/msg_id
      (bu havola faqat shu guruh a'zosi bo'lgan akkauntlarda ochiladi)
    - Oddiy (eski turdagi) guruhlarda xabarga to'g'ridan-to'g'ri havola bo'lmaydi.
    """
    if chat_username:
        return f"https://t.me/{chat_username}/{msg_id}"
    chat_id_str = str(chat_id)
    if chat_id_str.startswith('-100'):
        internal_id = chat_id_str[4:]
        return f"https://t.me/c/{internal_id}/{msg_id}"
    return None


# =================== KESH (TEZLIK UCHUN) ===================
# Har bir xabar uchun guruh va yuboruvchi ma'lumotini qaytadan so'rab
# o'tirmaslik uchun keshlab qo'yamiz - bu botni sezilarli tezlashtiradi.
CHAT_CACHE = {}
CHAT_CACHE_TIME = {}
SENDER_CACHE = {}
SENDER_CACHE_TIME = {}
CACHE_TTL = 1800  # 30 daqiqa - shundan keyin ma'lumot qayta yangilanadi
MAX_SENDER_CACHE = 8000  # xotira shishib ketmasligi uchun chegara


async def get_chat_info(event):
    chat_id = event.chat_id
    now = time.time()
    cached = CHAT_CACHE.get(chat_id)
    if cached and now - CHAT_CACHE_TIME.get(chat_id, 0) < CACHE_TTL:
        return cached

    chat = await event.get_chat()
    info = {
        'title': getattr(chat, 'title', 'Nomaʼlum guruh'),
        'username': getattr(chat, 'username', None),
    }
    CHAT_CACHE[chat_id] = info
    CHAT_CACHE_TIME[chat_id] = now
    return info


async def get_sender_info(event):
    sender_id = event.sender_id
    if sender_id is None:
        return None

    now = time.time()
    cached = SENDER_CACHE.get(sender_id)
    if cached and now - SENDER_CACHE_TIME.get(sender_id, 0) < CACHE_TTL:
        return cached

    sender = await event.get_sender()
    if sender is None:
        return None

    if len(SENDER_CACHE) > MAX_SENDER_CACHE:
        SENDER_CACHE.clear()
        SENDER_CACHE_TIME.clear()

    info = {
        'id': sender_id,
        'is_user': isinstance(sender, User),
        'username': get_username(sender),
        'phone': getattr(sender, 'phone', None),
    }
    SENDER_CACHE[sender_id] = info
    SENDER_CACHE_TIME[sender_id] = now
    return info


# =================== HANDLER ===================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # 🔥 ULANGAN SESSIYA A'ZO BO'LGAN BARCHA GURUH VA KANALLAR TEKSHIRILADI
        # (shaxsiy chatlar bundan mustasno)
        if not (event.is_group or event.is_channel):
            return

        chat_id = event.chat_id
        if chat_id in SKIP_CHAT_IDS:
            return

        text = event.raw_text
        if not text or not KEYWORDS_RE.search(text):
            return

        chat_info, sender_info = await asyncio.gather(
            get_chat_info(event),
            get_sender_info(event),
        )

        group_name = chat_info['title']

        if sender_info:
            username = sender_info['username']
            owner_display = f"@{username}" if username else "Berkitilgan"

            if sender_info['is_user']:
                profile_link = f"<a href='tg://user?id={sender_info['id']}'>Profilga o'tish</a>"
            elif username:
                profile_link = f"<a href='https://t.me/{username}'>Profilga o'tish</a>"
            else:
                profile_link = None

            phone = normalize_phone(sender_info['phone']) if sender_info['phone'] else None
        else:
            # Anonim admin nomidan yozilgan xabar (guruh nomidan yuborilgan)
            post_author = getattr(event.message, 'post_author', None)
            owner_display = post_author if post_author else "Anonim (guruh nomidan)"
            profile_link = None
            phone = None

        if not phone:
            for m in PHONE_RE.finditer(text):
                phone = normalize_phone(m.group(0))
                if phone:
                    break

        phone_display = phone if phone else "Berkitilgan"

        msg_link = build_message_link(chat_id, chat_info['username'], event.id)

        lines = [
            "🔈  <b>Elon topildi!</b>",
            "",
            f"📝  <b>Elon:</b> {text}",
            "",
            f"📍  <b>Guruh:</b> {group_name}",
            "",
            f"👤  <b>User:</b> {owner_display}",
            "",
            f"📞  <b>Raqam:</b> {phone_display}",
            "",
            "_________________________",
            "",
        ]
        if msg_link:
            lines.append(f"👉 <a href='{msg_link}'>Xabarga o'tish</a>")
        if profile_link:
            lines.append(f"🙍 {profile_link}")

        message_text = "\n".join(lines)

        # Barcha manzillarga bir vaqtning o'zida (parallel) yuboriladi - tezroq.
        await asyncio.gather(*[
            client.send_message(target_id, message_text, parse_mode='html', link_preview=False)
            for target_id in TARGET_CHAT_IDS
        ])
        print(f"📨 Yuborildi -> {len(TARGET_CHAT_IDS)} ta manzil")

    except Exception as e:
        print("❌ Xatolik:", e)


# =================== KESHNI ISHGA TUSHIRISHDA TO'LDIRISH ===================
async def warm_up_cache():
    """Sessiya a'zo bo'lgan barcha guruh/kanallarni oldindan keshga oladi.

    Shu tufayli birinchi mos xabar kelganda ham guruh nomini/username'ini
    qayta so'rab o'tirmay, darhol javob beradi - bu tezlikni oshiradi va
    ayni paytda barcha ulangan guruh/kanallar nazoratda ekanini kafolatlaydi.
    """
    count = 0
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, (Channel, Chat)):
            CHAT_CACHE[dialog.id] = {
                'title': getattr(entity, 'title', 'Nomaʼlum guruh'),
                'username': getattr(entity, 'username', None),
            }
            CHAT_CACHE_TIME[dialog.id] = time.time()
            count += 1
    return count


async def cache_refresher():
    """Guruh nomi/username o'zgarishi yoki yangi guruhga qo'shilish holatlarini
    hisobga olish uchun keshni har 15 daqiqada yangilab turadi."""
    while True:
        await asyncio.sleep(900)
        try:
            count = await warm_up_cache()
            print(f"🔄 Kesh yangilandi: {count} ta guruh/kanal")
        except Exception as e:
            print("⚠️ Kesh yangilashda xatolik:", e)


# =================== START ===================
async def main():
    await client.start()
    count = await warm_up_cache()
    print(f"🚕 Taxi bot ishga tushdi... {count} ta guruh/kanal nazoratga olindi.")
    asyncio.create_task(cache_refresher())
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
