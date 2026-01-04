import re
import html
import asyncio
from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== TELETHON ==================
API_ID = 28023612
API_HASH = "fe94ef46addc1b6b8253d5448e8511f0'Y"

tg_client = TelegramClient("taxi_session", API_ID, API_HASH)

# ================== BOT ==================
BOT_TOKEN = "7990459607:AAHabwIyHWo5e01xfpP79vrL-RpNWm1OlyA'Y"
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== TARGET GURUH ==================
FORWARD_GROUPS = [
    -1003398571650,
    -1002963614686
]


# ================== FILTR ==================
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
    'кетади', 'кетвотти', 'кетиши керак', "shopir kerak", "1kishi ayol kishili mashina kerak"
]

PHONE_RE = re.compile(r'\+998\d{9}')

def find_phone(text):
    m = PHONE_RE.search(text)
    return m.group(0) if m else "Berkitilgan"

# ================== TELETHON HANDLER ==================
@tg_client.on(events.NewMessage(incoming=True))
async def telethon_handler(event):
    if not (event.is_group or event.is_channel):
        return

    text = event.raw_text
    if not text or not KEYWORDS.search(text):
        return

    chat = await event.get_chat()
    sender = await event.get_sender()

    phone = find_phone(text)

    # guruh linki
    if getattr(chat, "username", None):
        msg_link = f"https://t.me/{chat.username}/{event.id}"
    else:
        msg_link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"

    # profil link
    if sender.username:
        profile_link = f"https://t.me/{sender.username}"
    else:
        profile_link = f"tg://user?id={sender.id}"

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profil", url=profile_link)],
        [InlineKeyboardButton(text="📨 Habar manzili", url=msg_link)],
        [InlineKeyboardButton(text="✅ Qabul qildim", callback_data="accept")]
    ])

    message = (
        "<b>🚖 Yangi buyurtma!</b>\n\n"
        f"📝 <b>Matn:</b>\n{html.escape(text)}\n\n"
        f"📞 <b>Raqam:</b> {phone}"
    )

    for gid in FORWARD_GROUPS:
        await bot.send_message(
            gid,
            message,
            reply_markup=buttons,
            parse_mode="HTML"
        )

# ================== CALLBACK ==================
@dp.callback_query(F.data == "accept")
async def accept(cb: types.CallbackQuery):
    await cb.message.edit_text(
        cb.message.text + "\n\n✅ <i>Buyurtma qabul qilindi</i>",
        parse_mode="HTML"
    )
    await cb.answer("Qabul qilindi")

# ================== RUN ==================
async def main():
    await tg_client.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
