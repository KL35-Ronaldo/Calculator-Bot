from os import getenv
from pyrogram.types import *
from pyrogram import Client, filters
from traceback import format_exc as exc


Bot = Client(
    session_name=getenv("SESSION_NAME", "Calculator Bot"),
    api_id=int(getenv("API_ID", "0")),
    api_hash=getenv("API_HASH", ""),
    bot_token = getenv("BOT_TOKEN", ""),
    sleep_threshold=int(getenv("SLEEP_THRESHOLD", "5"))
)


START_TEXT = """Hai **__{}__** 👋,

__I'm a Simple and Powerful Telegram **--Calculator--** Bot. Send **--/calculator--** to Start Calculating.__

__Made by **--@KL35Ronaldo--**__"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('😎 Master 😎', user_id=1790509785)
        ]
    ]
)

CALCULATE_TEXT = "__Made by --**@KL35Ronaldo**--__"

CALCULATE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("DEL", callback_data="DEL"),
            InlineKeyboardButton("AC", callback_data="AC"),
            InlineKeyboardButton("(", callback_data="("),
            InlineKeyboardButton(")", callback_data=")")
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
            InlineKeyboardButton("÷", callback_data="/")
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
            InlineKeyboardButton("×", callback_data="*")
        ],
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
            InlineKeyboardButton("-", callback_data="-"),
        ],
        [
            InlineKeyboardButton(".", callback_data="."),
            InlineKeyboardButton("0", callback_data="0"),
            InlineKeyboardButton("=", callback_data="="),
            InlineKeyboardButton("+", callback_data="+"),
        ]
    ]
)


@Bot.on_message(filters.command(["start"]))
async def start(c: Client, m: Message):
    if len(m.command) != 1 and m.command[1] == "calculate":
        await m.reply(CALCULATE_TEXT, True, reply_markup=CALCULATE_BUTTONS)
        return
    await m.reply(START_TEXT.format(m.from_user.mention), True, reply_markup=START_BUTTONS)

@Bot.on_message(filters.private & filters.command(["calc", "calculate", "calculator"]))
async def calculate(c: Client, m: Message):
    await m.reply("0", True, reply_markup=CALCULATE_BUTTONS)

@Bot.on_callback_query()
async def cb_data(c: Client, q: CallbackQuery):
    m, d = q.message, q.data
    try:
        t = m.text.strip()
        if d == "=":
            text = float(eval(t))
        elif d == "DEL":
            text = t[:-1] if not len(t) == 1 else t
        elif d == "AC":
            text = "0"
        else:
            text = t + d
        await m.edit(f"{text}", reply_markup=CALCULATE_BUTTONS)
    except:
        if "you tried to edit it using the same content" in exc():
            await q.answer()
        else:
            print(exc())

@Bot.on_inline_query()
async def inline(c: Client, q: InlineQuery):
    d = q.query
    if len(d) == 0:
        try:
            answers = [
                InlineQueryResultArticle(
                    "Calculator",
                    InputTextMessageContent(CALCULATE_TEXT),
                    None,
                    CALCULATE_BUTTONS,
                    None,
                    "A Simple Calculator Made By Ronaldo Fan.",
                    "https://telegra.ph/file/3ed71fa60172e09e96794.jpg"
                )
            ]
        except:
            print(exc())
    else:
        try:
            t = d.strip().split("=")[0].strip() if "=" in d else d.strip()
            dd = t.replace("×", "*").replace("x", "*").replace("X", "*").replace("÷", "/")
            t = float(eval(dd))
            answers = [
                InlineQueryResultArticle(
                    "Results",
                    InputTextMessageContent(f"{dd} = {t}"),
                    None,
                    None,
                    None,
                    "A Simple Calculator Made By Ronaldo Fan.",
                    "https://telegra.ph/file/3ed71fa60172e09e96794.jpg"
                )
            ]
        except:
            print(exc())
            answers = [
                InlineQueryResultArticle(
                    "Error",
                    InputTextMessageContent(f"Sorry Something Went Wrong..!\n\n\n`{exc()}`\n\n\nPlease Try Again."),
                    None,
                    None,
                    None,
                    "A Simple Calculator Made By Ronaldo Fan.",
                    "https://telegra.ph/file/3ed71fa60172e09e96794.jpg"
                )
            ]
    await q.answer(answers, 300, False, False, "", "🔥 A Simple Calculator Made By Ronaldo Fan. 🔥", "calculate")


Bot.run()
