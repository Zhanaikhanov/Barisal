#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import MessageHandler, Filters

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import os
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
CHOOSING_1, TYPING_REPLY_1, TYPING_CHOICE_1 = range(3)
CHOOSING_2, TYPING_REPLY_2, TYPING_CHOICE_2 = range(3)

def save_data(user_d, user_n):
    print("make sense")

    useraname = user_n["username"]
    category = user_d["category"]
    location = user_d["location"]
    text = user_d["text"]

    directory = "data/{}/{}/{}".format(location,category,"@"+useraname)

    if not os.path.exists(directory):
        os.makedirs(directory)

    i=1
    filename = ""
    while True:
        fil = "text" + str(i) + '.txt'
        if not os.path.exists(os.path.join(directory, fil)):
            filename = fil
            break
        else:
            i+=1

    path = directory
    with open(os.path.join(path, filename), 'w') as temp_file:
        temp_file.write(text)




reply_keyboard = [
        ['Безопасность'],
        ['Бизнес'],
        ['Государственное управление'],
        ['ЖКХ'],
        ['Здравоохранение'],
        ['Земельные отношения'],
        ['Инфраструктура'],
        ['Коррупция'],
        ['Трудовые отношения'],
        ['Судебно-правовая система'],
        ['Межэтнические и религиозные отношения'],
        ['Образование'],
        ['Общественный транспорт'],
        ['Транспорт и автомобильные дороги'],
        ['Экология'],
        ['Другое'],
        ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

reply_keyboard_1 = [
        ['г. Астана [1] [Z]'],
        ['г. Алматы [2] [A]'],
        ['Акмолинская область [3] [C]'],
        ['Актюбинская область [4] [D]'],
        ['Алматинская область [5] [B]'],
        ['Атырауская область [6] [E]'],
        ['Западно-Казахстанская область [7] [L]'],
        ['Жамбылская область [8] [H]'],
        ['Карагандинская область [9] [M]'],
        ['Костанайская область [10] [P]'],
        ['Кызылординская область [11] [N]'],
        ['Мангистауская область [12] [R]'],
        ['Южно-Казахстанская область [13] [X]'],
        ['Павлодарская область [14] [S]'],
        ['Северо-Казахстанская область [15] [T]'],
        ['Восточно-Казахстанская область [16] [F]'],
        ['г. Шымкент [17] [X]'],
        ['Donex']]

reply_keyboard_3 = [
        ['/location'],
        ['Done']
        ]
markup_3 = ReplyKeyboardMarkup(reply_keyboard_3, one_time_keyboard=True)

markup_1 = ReplyKeyboardMarkup(reply_keyboard_1, one_time_keyboard=True)

reply_keyboard_4 = [
        ['/text'],
        ['Done']
        ]
markup_4 = ReplyKeyboardMarkup(reply_keyboard_4, one_time_keyboard=True)


def category(update, context):
    update.message.reply_text(
        "Hello, this bot is here to accept your report. Please choose category of your report, from the following list:"
,
        reply_markup=markup)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['category'] = text
    update.message.reply_text(
        'You chose category - {}. Please choose location ...'.format(text.lower()),reply_markup=markup_3)

    return TYPING_REPLY



def done(update, context):
    user_data = context.user_data
    if 'category' in user_data:
        del user_data['category']

    update.message.reply_text("I learned these fa category cts about you:"
                              "{}"
                              "Until next time!".format(str(user_data)))

    user_data.clear()
    return ConversationHandler.END
# =============================================
def location(update, context):
    update.message.reply_text(
        "Hello this bot here to accept your report. Please choose location of your report, from the following list:",
        reply_markup=markup_1)
    return CHOOSING_1


def regular_choice_1(update, context):
    text = update.message.text
    context.user_data['location'] = text
    update.message.reply_text(
        'You chose location - {} Please choose text ...'.format(text.lower()),reply_markup=markup_4)

    return TYPING_REPLY_1







def done_1(update, context):
    user_data = context.user_data
    if 'location' in user_data:
        del user_data['location']

    update.message.reply_text("Your location is: location"
                              "{}"
                              "Until next time!".format(str(user_data)))

    user_data.clear()
    return ConversationHandler.END
# ================================================================
def text(update, context):
    update.message.reply_text(
        "Please describe your problem:")
    print("asdasd f=dtext")







def done_2(update, context):
    user_data = context.user_data
    text = update.message.text
    context.user_data['text'] = text
    print(str(user_data),update.message.from_user)


    save_data(user_data,update.message.from_user)
    #print('asdfg')

    update.message.reply_text("We accepted your report:\n"
                              "\tlocation - {}\n"
                              "\tcategory - {}\n"
                              "\ttext - {}\n"
                              
                              "Thank You!".format(user_data["location"],user_data["category"],user_data["text"]))

    user_data.clear()
    print("asdasd f=done2")
# ================================================================


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("653164476:AAE3YsRytJSd45waiYqg5cvGysLSnKdeiAY", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', category)],

        states={
            CHOOSING: [RegexHandler('^',
                                    regular_choice,
                                    pass_user_data=True),
                       ],

        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    conv_handler_1 = ConversationHandler(
        [CommandHandler('location', location)],

        {
            CHOOSING: [RegexHandler('^',
                                    regular_choice_1,
                                    pass_user_data=True),
                       
                       ],

        },

        [RegexHandler('^Donex$', done_1, pass_user_data=True)]
    )

    dp.add_handler(conv_handler_1)

    dp.add_handler(CommandHandler('text', text))
    dp.add_handler( MessageHandler(Filters.text, done_2) )



    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
