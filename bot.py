from os import environ

from firebase_admin import credentials, db, initialize_app
from flask import Flask, request
from telebot import TeleBot, types
from wikipedia import (
    WikipediaPage,
    geosearch,
    page,
    random,
    search,
    set_lang,
    suggest,
    summary,
)

# Firebase connection
cred = credentials.Certificate("firebase.json")  # Firebase key
initialize_app(
    cred, {"databaseURL": "https://yourappname-user-default-rtdb.firebaseio.com/"}
)
ref = db.reference("/")
z = ref.get()

# Telegram API
TOKEN = ""  # Bot key
bot = TeleBot(TOKEN)

# Flask connection
server = Flask(__name__)

# Common Messages
error = "Wrong word, use <b>title</b>"
error2 = "Wrong word, use <b>suggest</b>"
word = " for the word..."

# Languages
lang_list = [
    "aa",
    "ab",
    "abs",
    "ace",
    "ady",
    "ady-cyrl",
    "aeb",
    "aeb-arab",
    "aeb-latn",
    "af",
    "ak",
    "aln",
    "als",
    "alt",
    "am",
    "ami",
    "an",
    "ang",
    "anp",
    "ar",
    "arc",
    "arn",
    "arq",
    "ary",
    "arz",
    "as",
    "ase",
    "ast",
    "atj",
    "av",
    "avk",
    "awa",
    "ay",
    "az",
    "azb",
    "ba",
    "ban",
    "ban-bali",
    "bar",
    "bat-smg",
    "bbc",
    "bbc-latn",
    "bcc",
    "bcl",
    "be",
    "be-tarask",
    "be-x-old",
    "bg",
    "bgn",
    "bh",
    "bho",
    "bi",
    "bjn",
    "bm",
    "bn",
    "bo",
    "bpy",
    "bqi",
    "br",
    "brh",
    "bs",
    "btm",
    "bto",
    "bug",
    "bxr",
    "ca",
    "cbk-zam",
    "cdo",
    "ce",
    "ceb",
    "ch",
    "cho",
    "chr",
    "chy",
    "ckb",
    "co",
    "cps",
    "cr",
    "crh",
    "crh-cyrl",
    "crh-latn",
    "cs",
    "csb",
    "cu",
    "cv",
    "cy",
    "da",
    "de",
    "de-at",
    "de-ch",
    "de-formal",
    "din",
    "diq",
    "dsb",
    "dtp",
    "dty",
    "dv",
    "dz",
    "ee",
    "egl",
    "el",
    "eml",
    "en",
    "en-ca",
    "en-gb",
    "eo",
    "es",
    "es-419",
    "es-formal",
    "et",
    "eu",
    "ext",
    "fa",
    "ff",
    "fi",
    "fit",
    "fiu-vro",
    "fj",
    "fo",
    "fr",
    "frc",
    "frp",
    "frr",
    "fur",
    "fy",
    "ga",
    "gag",
    "gan",
    "gan-hans",
    "gan-hant",
    "gcr",
    "gd",
    "gl",
    "glk",
    "gn",
    "gom",
    "gom-deva",
    "gom-latn",
    "gor",
    "got",
    "grc",
    "gsw",
    "gu",
    "gv",
    "ha",
    "hak",
    "haw",
    "he",
    "hi",
    "hif",
    "hif-latn",
    "hil",
    "ho",
    "hr",
    "hrx",
    "hsb",
    "ht",
    "hu",
    "hu-formal",
    "hy",
    "hyw",
    "hz",
    "ia",
    "id",
    "ie",
    "ig",
    "ii",
    "ik",
    "ike-cans",
    "ike-latn",
    "ilo",
    "inh",
    "io",
    "is",
    "it",
    "iu",
    "ja",
    "jam",
    "jbo",
    "jut",
    "jv",
    "ka",
    "kaa",
    "kab",
    "kbd",
    "kbd-cyrl",
    "kbp",
    "kg",
    "khw",
    "ki",
    "kiu",
    "kj",
    "kjp",
    "kk",
    "kk-arab",
    "kk-cn",
    "kk-cyrl",
    "kk-kz",
    "kk-latn",
    "kk-tr",
    "kl",
    "km",
    "kn",
    "ko",
    "ko-kp",
    "koi",
    "kr",
    "krc",
    "kri",
    "krj",
    "krl",
    "ks",
    "ks-arab",
    "ks-deva",
    "ksh",
    "ku",
    "ku-arab",
    "ku-latn",
    "kum",
    "kv",
    "kw",
    "ky",
    "la",
    "lad",
    "lb",
    "lbe",
    "lez",
    "lfn",
    "lg",
    "li",
    "lij",
    "liv",
    "lki",
    "lld",
    "lmo",
    "ln",
    "lo",
    "loz",
    "lrc",
    "lt",
    "ltg",
    "lus",
    "luz",
    "lv",
    "lzh",
    "lzz",
    "mad",
    "mai",
    "map-bms",
    "mdf",
    "mg",
    "mh",
    "mhr",
    "mi",
    "min",
    "mk",
    "ml",
    "mn",
    "mni",
    "mnw",
    "mo",
    "mr",
    "mrh",
    "mrj",
    "ms",
    "mt",
    "mus",
    "mwl",
    "my",
    "myv",
    "mzn",
    "na",
    "nah",
    "nan",
    "nap",
    "nb",
    "nds",
    "nds-nl",
    "ne",
    "new",
    "ng",
    "nia",
    "niu",
    "nl",
    "nl-informal",
    "nn",
    "no",
    "nov",
    "nqo",
    "nrm",
    "nso",
    "nv",
    "ny",
    "nys",
    "oc",
    "olo",
    "om",
    "or",
    "os",
    "pa",
    "pag",
    "pam",
    "pap",
    "pcd",
    "pdc",
    "pdt",
    "pfl",
    "pi",
    "pih",
    "pl",
    "pms",
    "pnb",
    "pnt",
    "prg",
    "ps",
    "pt",
    "pt-br",
    "qu",
    "qug",
    "rgn",
    "rif",
    "rm",
    "rmy",
    "rn",
    "ro",
    "roa-rup",
    "roa-tara",
    "ru",
    "rue",
    "rup",
    "ruq",
    "ruq-cyrl",
    "ruq-latn",
    "rw",
    "sa",
    "sah",
    "sat",
    "sc",
    "scn",
    "sco",
    "sd",
    "sdc",
    "sdh",
    "se",
    "sei",
    "ses",
    "sg",
    "sgs",
    "sh",
    "shi",
    "shi-latn",
    "shi-tfng",
    "shn",
    "shy-latn",
    "si",
    "simple",
    "sk",
    "skr",
    "skr-arab",
    "sl",
    "sli",
    "sm",
    "sma",
    "smn",
    "sn",
    "so",
    "sq",
    "sr",
    "sr-ec",
    "sr-el",
    "srn",
    "ss",
    "st",
    "stq",
    "sty",
    "su",
    "sv",
    "sw",
    "szl",
    "szy",
    "ta",
    "tay",
    "tcy",
    "te",
    "tet",
    "tg",
    "tg-cyrl",
    "tg-latn",
    "th",
    "ti",
    "tk",
    "tl",
    "tly",
    "tn",
    "to",
    "tpi",
    "tr",
    "tru",
    "trv",
    "ts",
    "tt",
    "tt-cyrl",
    "tt-latn",
    "tum",
    "tw",
    "ty",
    "tyv",
    "tzm",
    "udm",
    "ug",
    "ug-arab",
    "ug-latn",
    "uk",
    "ur",
    "uz",
    "uz-cyrl",
    "uz-latn",
    "ve",
    "vec",
    "vep",
    "vi",
    "vls",
    "vmf",
    "vo",
    "vot",
    "vro",
    "wa",
    "war",
    "wo",
    "wuu",
    "xal",
    "xh",
    "xmf",
    "xsy",
    "yi",
    "yo",
    "yue",
    "za",
    "zea",
    "zgh",
    "zh",
    "zh-classical",
    "zh-cn",
    "zh-hans",
    "zh-hant",
    "zh-hk",
    "zh-min-nan",
    "zh-mo",
    "zh-my",
    "zh-sg",
    "zh-tw",
    "zh-yue",
    "zu",
]


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True
    )
    texts = [
        "Definition 📖",
        "Title 🖊️️",
        "URL  🔗",
        "Language 🔣",
        "Random 🔀",
        "Help ⚠️",
        "Map 🗺️",
        "Nearby 📍",
    ]
    buttons = []
    for text in texts:
        button = types.KeyboardButton(text)
        buttons.append(button)
    markup.add(*buttons)
    return markup


def support_keyboard():
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True
    )
    texts = ["🧑🏻‍💻️ Dev", "🐛 Bug", "💻️ Source", "🔙 Back"]
    buttons = []
    for text in texts:
        button = types.KeyboardButton(text)
        buttons.append(button)
    markup.add(*buttons)
    return markup


def extra_keyboard():
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True
    )
    texts = ["Suggest 💡", "Fluky 💫", "Back ⬅️"]
    buttons = []
    for text in texts:
        button = types.KeyboardButton(text)
        buttons.append(button)
    markup.add(*buttons)
    return markup


def check(text, command):
    checker = str(text).replace("/", "").replace("#", "").lower().split(" ")
    if command in checker:
        return 1
    return 0


def change_lan(message):
    user_id = str(message.from_user.id)
    set_lang(z[user_id])


@bot.message_handler(func=lambda message: check(message.text, "start"))
def welcome(message):
    user_id = message.from_user.id
    ref.update({user_id: "en"})
    welcome_msg = (
        "Greetings " + message.from_user.first_name + ", I am Wikibot 🤖\n\n"
        "What can I do? Use <b>help</b>."
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_msg,
        parse_mode="html",
        reply_markup=main_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "definition"))
def definition(message):
    def_msg = bot.reply_to(message, "<b>Definition</b>" + word, parse_mode="html")
    bot.register_next_step_handler(def_msg, process_definition)


def process_definition(message):
    try:
        def_msg = str(message.text)
        change_lan(message)
        def_str = summary(def_msg, sentences=10)
        def_split = def_str.split("\n\n", 1)[0]
        bot.send_message(
            chat_id=message.chat.id,
            text="<b>" + def_msg + "</b> \n\n" + def_split,
            parse_mode="html",
            reply_markup=main_keyboard(),
        )
    except Exception as c:
        if str(c)[:7] == "Page id":
            msg = "<b>Not Found!</b>"
        else:
            msg = str(c).replace("may refer to", "<b>may refer to</b>")
        bot.send_message(
            chat_id=message.chat.id,
            text=msg,
            parse_mode="html",
            reply_markup=main_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "title"))
def title(message):
    title_msg = bot.reply_to(message, "<b>Title</b>" + word, parse_mode="html")
    bot.register_next_step_handler(title_msg, process_title)


def process_title(message):
    try:
        title_msg = str(message.text)
        change_lan(message)
        title_result = search(title_msg)
        if title_result:
            bot.send_message(
                chat_id=message.chat.id,
                text="Possible titles are...",
                parse_mode="html",
            )
            for i in title_result:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=i.replace(title_msg, "<b>" + title_msg + "</b>").replace(
                        title_msg.lower(), "<b>" + title_msg.lower() + "</b>"
                    ),
                    parse_mode="html",
                    reply_markup=main_keyboard(),
                )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=error2,
                parse_mode="html",
                reply_markup=main_keyboard(),
            )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text=error2,
            parse_mode="html",
            reply_markup=main_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "help"))
def aid(message):
    text = (
        "These keywords can be used to control me - \n\n"
        "<b>Primary</b> \n"
        "Definition 📖 - fetches definition of a word \n"
        "Title 🖊️️ - fetches a bunch of related titles\n"
        "URL 🔗 - gives the URL of wiki page of the word \n"
        "Prefix 🔡 - show all available languages \n"
        "Language 🔣 - set the language you want \n\n"
        "<b>Secondary</b> \n"
        "Nearby 📍 - locations near a coordinate \n"
        "Map 🗺️ - location in map with wiki database \n"
        "Random 🔀 - pops a random article from wiki \n\n"
        "<b>Extra</b> \n"
        "Fluky 💫 - fetches a random title from wiki \n"
        "Suggest 💡 - returns a suggested word if found \n"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="html",
        reply_markup=main_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "url"))
def url(message):
    url_msg = bot.reply_to(message, "<b>URL</b>" + word, parse_mode="html")
    bot.register_next_step_handler(url_msg, process_url)


def process_url(message):
    try:
        url_message = str(message.text)
        change_lan(message)
        url_page = page(url_message).url
        url_link = "<a href='" + url_page + "'>🔗</a>"
        bot.send_message(
            chat_id=message.chat.id,
            text=url_link + "for <b>" + url_message + "</b>",
            parse_mode="html",
            reply_markup=main_keyboard(),
        )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text=error,
            parse_mode="html",
            reply_markup=main_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "language"))
def ln(message):
    ln_msg = bot.reply_to(
        message, "Type the prefix of your <b>language</b>...", parse_mode="html"
    )
    bot.register_next_step_handler(ln_msg, process_ln)


def process_ln(message):
    try:
        ln_msg = str(message.text).lower()
        if ln_msg in lang_list:
            user_id = message.from_user.id
            ref.update({user_id: str(message.text).lower()})
            global z
            z = ref.get()
            text = "Set Successfully."
        else:
            text = (
                "Please, check for the correct <a href="
                '"https://github.com/themagicalmammal/wikibot/blob/master/Lang.md"'
                ">prefix</a>."
            )
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="html",
            reply_markup=main_keyboard(),
        )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text="Error, changing language",
            reply_markup=main_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "support"))
def support(message):
    text = (
        "Support commands that I provide -  \n\n"
        "Bugs 🐛 - to report bugs or suggest mods\n"
        "Dev 🧑🏻‍💻️ - provides information about my creator\n"
        "Source 💻️ - to view the source code"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="html",
        reply_markup=support_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "prefix"))
def prefix(message):
    text = (
        "Language is set with the help of it's Prefix. \n<b>Example</b> - English:en<a "
        'href="https://github.com/themagicalmammal/wikibot/blob/master/Lang.md"'
        ">.</a>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="html",
        reply_markup=main_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "random"))
def randomize(message):
    try:
        change_lan(message)
        random_title = page(random(pages=1)).url
        random_text = "<a href='" + random_title + "'>✨</a>"
        bot.send_message(
            chat_id=message.chat.id,
            text=random_text,
            parse_mode="html",
            reply_markup=main_keyboard(),
        )
    except BaseException:
        randomize(message)


@bot.message_handler(func=lambda message: check(message.text, "map"))
def chart(message):
    co_msg = bot.reply_to(message, "<b>Location</b> of the place...", parse_mode="html")
    bot.register_next_step_handler(co_msg, process_co)


def process_co(message):
    try:
        co_msg = str(message.text)
        set_lang("en")
        lat, lon = WikipediaPage(co_msg).coordinates
        bot.send_message(
            chat_id=message.chat.id, text=str(round(lat, 5)) + ", " + str(round(lon, 5))
        )
        bot.send_location(
            chat_id=message.chat.id,
            latitude=lat,
            longitude=lon,
            reply_markup=main_keyboard(),
        )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text="Not a location.",
            reply_markup=main_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "nearby"))
def geo(message):
    geo_msg = bot.reply_to(
        message, "Send me the <b>coordinates</b>...", parse_mode="html"
    )
    bot.register_next_step_handler(geo_msg, process_geo)


def process_geo(message):
    try:
        lat, lan = (
            str(message.text)
            .replace("E", "")
            .replace("W", "")
            .replace("N", "")
            .replace("S", "")
            .replace("° ", "")
            .replace("°", "")
            .replace(",", "")
            .replace("  ", " ")
            .split(" ")
        )
        set_lang("en")
        locations = geosearch(latitude=lat, longitude=lan, results=10, radius=1000)
        if locations:
            nearby = "<b>Nearby locations</b> are..."
            bot.send_message(
                chat_id=message.chat.id,
                text=nearby,
                parse_mode="html",
                reply_markup=main_keyboard(),
            )
            for i in locations:
                bot.send_message(
                    chat_id=message.chat.id, text=i, reply_markup=main_keyboard()
                )
        else:
            sorry = "Sorry, can't find nearby locations"
            bot.send_message(
                chat_id=message.chat.id, text=sorry, reply_markup=main_keyboard()
            )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text="Use <b>Map</b> to get coordinates.",
            parse_mode="html",
            reply_markup=main_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "fluky"))
def fluky(message):
    change_lan(message)
    fluky_title = random(pages=1)
    bot.send_message(
        chat_id=message.chat.id, text=fluky_title, reply_markup=extra_keyboard()
    )


@bot.message_handler(func=lambda message: check(message.text, "back"))
def back(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="<b>Commands</b>",
        parse_mode="html",
        reply_markup=main_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "suggest"))
def suggestion(message):
    suggest_msg = bot.reply_to(
        message, "<b>Suggestion</b> for the word...", parse_mode="html"
    )
    bot.register_next_step_handler(suggest_msg, process_suggest)


def process_suggest(message):
    sorry = "Sorry, <b>no suggestions.</b>"
    try:
        suggest_msg = str(message.text)
        change_lan(message)
        suggest_str = str(suggest(suggest_msg))
        if suggest_str != "None":
            text = suggest_str
        else:
            text = sorry
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="html",
            reply_markup=extra_keyboard(),
        )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text=sorry,
            parse_mode="html",
            reply_markup=extra_keyboard(),
        )


@bot.message_handler(func=lambda message: check(message.text, "bug"))
def bug(message):
    text = (
        "Submit a Issue or Revision<a "
        'href="https://github.com/themagicalmammal/wikibot/issues">.</a> '
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="html",
        reply_markup=support_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "dev"))
def dev(message):
    text = (
        "I was made with ❤ by @themagicalmammal"
        '<a href="https://github.com/themagicalmammal">.</a>'
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="html",
        reply_markup=support_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "source"))
def source(message):
    text = (
        "Checkout out How I was made"
        '<a href="https://github.com/themagicalmammal/wikibot">.</a>'
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="html",
        reply_markup=support_keyboard(),
    )


@bot.message_handler(func=lambda message: check(message.text, "extra"))
def extra(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="<b>Extra</b>",
        parse_mode="html",
        reply_markup=extra_keyboard(),
    )


@bot.message_handler(func=lambda message: True)
def unrecognized(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="<b>Please</b>, use a keyword",
        parse_mode="html",
        reply_markup=main_keyboard(),
    )


# Heroku Connection
@server.route("/" + TOKEN, methods=["POST"])
def establish():
    bot.process_new_updates(
        [types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://yourappname.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
