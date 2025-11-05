from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
import os

router = Router()

nenormativniy_set = {"хуй", "блять", "пидор", "пидарас", "пидрила", "сука", "сучка", "ебобо", "хуеглот", "пизда", "мудло", "блядь", "еблан", "долбоёб", "долбоеб", "долбаеб", "конч", "конченый", "мудак", "козёл ебаный", "сука", "мразь", "гондон", "пидорас", "петух", "дебил", "кретин", "идиот", "даун", "олигофрен", "долбоёбина", "уёбок", "дурак", "придурок", "тупица", "недоумок", "тормоз", "дундук", "безмозглый", "тупой как пробка", "олух", "балбес", "обалдуй", "бестолочь", "имбецил", "дегенерат", "уродина", "урод", "выродок", "животное", "скотина", "свинья", "быдло", "деревенщина", "хамуло", "хам", "грубиян", "невоспитанный свин", "подонок", "отброс общества", "гопник", "алкаш", "наркоман", "босяк", "нищеброд", "жлоб", "чмо", "чмошник", "бездарность", "ничтожество", "дилетант", "профан", "неумеха", "растяпа", "разгильдяй", "рукожоп", "криворукий", "копуша", "неряха", "недотёпа", "тварь дрожащая", "моль", "овощ", "пустое место", "ноль без палочки", "посмешище", "лузер", "говноед", "подлиза", "приспособленец", "шестёрка", "ботан", "ботаник", "зануда", "заучка", "слизняк", "тряпка", "тюфяк", "слюнтяй", "мямля", "кусок бесполезного мяса", "кусок дерьма в дорогом костюме", "ошибка природы", "ходячее недоразумение", "кусок говна с глазами", "пустое место в дорогой обёртке", "никто и звать тебя никак", "говно на палочке", "мусор человеческий", "исчадие ада"}

main_keyboard = ReplyKeyboardMarkup(keyboard= [[KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")], [KeyboardButton(text="Кнопка 3")]], resize_keyboard=True, one_time_keyboard=True)

@router.message(Command("off"))
async def off_handler(message: Message):
    # Экранируем все спецсимволы для MarkdownV2
    await message.answer("🛑 Бот выключается\\.\\.\\.")
    print("Бот отключен по команде /off")
    os._exit(0)  # Немедленное завершение процесса

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет\\! 👋\n"
        "Я бот, который показывает твой ID в Telegram\\.\n"
        "Просто отправь мне любое сообщение, и я скажу твой ID\\.\n"
        "Для выключения отправь /off"
    )
    await message.answer(
        "Выберите действие: ",
        reply_markup=main_keyboard
    )

# @router.message(F.text.lower() == "привет")
# async def hello_handler(message: Message):
#     await message.answer("Привет! 👋 Напиши мне что-нибудь и я покажу твой ID!")

@router.message(F.text)
async def message_handler(message: Message):
    user_id = message.from_user.id
    if message.text.lower().startswith("ты"):
        if message.text.lower()[3:] in nenormativniy_set:
            await message.answer("Сам такой сука")
        else:
            await message.answer(f"🤖 Твой ID\\: `{user_id}`")
    elif message.text.lower() in nenormativniy_set:
        await message.answer("иди нахуй заебал")
        await message.answer("пиши /off сука")
    else:
        await message.answer(f"🤖 Твой ID\\: `{user_id}`")

@router.message()
async def non_text_handler(message: Message):
    user_id = message.from_user.id
    await message.answer(f"🤖 Твой ID\\: `{user_id}`\\n\\(и я получил твой медиафайл\\!\\)")
