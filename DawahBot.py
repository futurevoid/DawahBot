import os
import json
from typing import final
import telebot
from telebot import types
from keep_alive import keep_alive

# Load bot token from environment variables
bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot("7271890883:AAHV25203gANi6fopsr7aG0lGAydSnCNAlI")

# Introductory message and material types
intro_message = """السلام عليكم ورحمة الله وبركاته.,🌺

"أهلًا بكم في "بوت الدعوة"

تستطيع من خلال هذا البوت الوصول إلى مواد مشايخ الدعوة السلفية سواءً بصورة مرئيه أو صوتية أو تفريغ كتابي وعلى المنصات المختلفة.

📝خطوات تشغيل البوت:
١. اضغط على كلمة ابدأ أو "Start".
٢. استخدم الأزرار التي تظهر أسفل الشاشة لاختيار الدروس التي ترغب بالاستماع إليها أو قراءة التفريغ -إن توفر-.
"""

material_types = """🍃 اختر الصيغة المطلوبة:

1- صوتي mp3. 📢
2- لينك اليوتيوب. 📽
3- تفريغ كتابي. 📝
4- الكتاب. 📚
5- الاختبار. ✏️
"""

# Material options
audio = "1- صوتي mp3. 📢"
yt = "2- لينك اليوتيوب. 📽"
txt = "3- تفريغ كتابي. 📝"
book = "4- الكتاب. 📚"
test = "5- الاختبار. ✏️"
final_test = "الاختبار النهائي ✏️"

# Load materials data from JSON file
with open("materials.json", "r", encoding="utf-8") as file:
    materials = json.load(file)

# Global state to keep track of selected course and lecture
user_state = {}

# Start menu
@bot.message_handler(commands=['start', 'menu'])
def start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    droos = types.KeyboardButton("📚 كتب و دروس")
    social = types.KeyboardButton("🌐 الصفحــات الرسمية")
    betaqat = types.KeyboardButton("البطاقات الدعوية")
    markup.add(droos)
    markup.add(social)
    markup.add(betaqat)
    bot.send_message(message.chat.id, intro_message, reply_markup=markup)

# Handler for 'كتب و دروس' and main menu
@bot.message_handler(func=lambda message: '📚 كتب و دروس' in message.text or message.text == '🏠 القائمة الرئيسية')
def droos_prehandler(message):
    if message.text == '🏠 القائمة الرئيسية':
        start_menu(message)
        return
    
    
    with open('droos.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    droos_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for droos_line in materials.keys():  # Exclude the first and last line
        droos_markup.add(types.KeyboardButton(droos_line.strip()))
    droos_markup.add(types.KeyboardButton("🔙 الرجوع الى الشروحات"))
    droos_markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    bot.send_message(message.chat.id, "🌿 اخـتَر الشرح المَطـلوب من الازرار في الاسفل \n او أدخل جزء من اسم الدرس أو كلمة مفتاحية للبحث عنه  ", reply_markup=droos_markup)
    bot.register_next_step_handler(message, droos_search)

def droos_search(message):
    query = message.text.strip().lower()
    print(query)
    matching_droos = [droos_name for droos_name in materials.keys() if query in droos_name.lower()]
    
    for droos_name in materials.keys():
        if query == droos_name.lower():
            droos_handler(message)
            return

    if matching_droos:
        droos_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for droos_name in matching_droos:
            droos_markup.add(types.KeyboardButton(droos_name))
        droos_markup.add(types.KeyboardButton("🔙 الرجوع الى الشروحات"))
        droos_markup.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
        bot.send_message(message.chat.id, "اخـتَر الشرح المَطـلوب 🌿", reply_markup=droos_markup)
    else:
        bot.send_message(message.chat.id, "لم يتم العثور على دروس مطابقة. حاول مرة أخرى.")
        droos_prehandler(message)

# Handler for selecting specific lectures/materials
@bot.message_handler(func=lambda message: message.text in materials or message.text == '🏠 القائمة الرئيسية' or message.text == '🔙 الرجوع الى الشروحات')
def droos_handler(message):
    if message.text == '🏠 القائمة الرئيسية':
        start_menu(message)
        return
    elif message.text == '🔙 الرجوع الى الشروحات':
        droos_prehandler(message)
        return
    
    course = message.text
    user_state[message.chat.id] = {'course': course}  # Update user state with selected course

    lectures = materials[course].keys()
    droos_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lecture in lectures:
        droos_menu.add(types.KeyboardButton(lecture))

    droos_menu.add(types.KeyboardButton("🔙 الرجوع الى الشروحات"))
    droos_menu.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
    bot.send_message(message.chat.id, "اخـتَر الدرس المَطـلوب 🌿", reply_markup=droos_menu)

# Handler for selecting material types
@bot.message_handler(func=lambda message: any(message.text in materials[course] for course in materials) or message.text == '🏠 القائمة الرئيسية' or message.text == '🔙 الرجوع الى الشروحات')
def mat_type_handler(message):
    if message.text == '🏠 القائمة الرئيسية':
        start_menu(message)
        return
    elif message.text == '🔙 الرجوع الى الشروحات':
        droos_prehandler(message)
        return
    
    user_id = message.chat.id
    if user_id in user_state:
        course = user_state[user_id].get('course')
        if not course:
            droos_prehandler(message)
            return
        
        if message.text in "الاختبار النهائي":
            lecture = message.text
            user_state[user_id]['lecture'] = lecture
            material_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
            material_menu.add(types.KeyboardButton(final_test))
            material_menu.add(types.KeyboardButton("🔙 الرجوع الى الشروحات"))
            material_menu.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
            bot.send_message(message.chat.id, final_test, reply_markup=material_menu)
            return
            
        if message.text in materials[course]:
            lecture = message.text
            user_state[user_id]['lecture'] = lecture  # Update user state with selected lecture
            material_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
            material_menu.add(
                types.KeyboardButton(audio),
                types.KeyboardButton(yt),
                types.KeyboardButton(txt),
                types.KeyboardButton(book),
                types.KeyboardButton(test),
            )
            material_menu.add(types.KeyboardButton("🔙 الرجوع الى الشروحات"))
            material_menu.add(types.KeyboardButton("🏠 القائمة الرئيسية"))
            bot.send_message(message.chat.id, material_types, reply_markup=material_menu)
            return
        else:
            bot.send_message(message.chat.id, "Please select a valid option.")
    else:
        start_menu(message)


# Handler for providing the selected material
@bot.message_handler(func=lambda message: any(mat_type in message.text for mat_type in [audio, yt, txt, book, test]) or message.text == '🏠 القائمة الرئيسية' )
def material_handler(message):
    if message.text == "🏠 القائمة الرئيسية":
        start_menu(message)
        return

    user_id = message.chat.id
    if user_id in user_state:
        course = user_state[user_id].get('course')
        lecture = user_state[user_id].get('lecture')

        if course and lecture:
            mat_type = message.text
            material = materials[course][lecture].get(mat_type)
            if material:
                bot.send_message(message.chat.id, material)
                return

    start_menu(message)


keep_alive()
# Polling for messages
bot.infinity_polling(skip_pending=True)
