import logging
import os
import random
import redis

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from dotenv import load_dotenv
from enum import Enum
from functools import partial
from quiz_questions_loader import get_quiz_questions


logger = logging.getLogger(__name__)


class Questions(Enum):
    SEND_QUESTION = 1
    GET_ANSWER = 2


def start(bot, update):
    update.message.reply_text('Привет! Я бот для викторин!')
    custom_keyboard = [['Новый вопрос', 'Сдаться'], 
                      ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, 
                    text="Custom Keyboard Test", 
                    reply_markup=reply_markup)
    return Questions.SEND_QUESTION
    

def help(bot, update):
    update.message.reply_text('Help!')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def handle_new_question_request(redis_db, quiz_questions, bot, update):
    current_question, answer = random.choice(list(quiz_questions.items()))
    update.message.reply_text(current_question)
    redis_db.set(update.effective_user.id, current_question)
    
    return Questions.GET_ANSWER


def handle_solution_attempt(redis_db, quiz_questions, bot, update):
    answer = quiz_questions[redis_db.get(update.effective_user.id)].replace('Ответ:', '').lower().strip().split('.')[0]
    if update.message.text.lower() in answer:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return Questions.SEND_QUESTION
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')


def cancel(redis_db, quiz_questions, bot, update):
    update.message.reply_text(quiz_questions[redis_db.get(update.effective_user.id)])
    
    return Questions.SEND_QUESTION


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

    load_dotenv()
    r = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'), 
        db=0,
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
        )
    quiz_questions = get_quiz_questions()
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(telegram_bot_token)

    dp = updater.dispatcher

    partial_handle_new_question_request = partial(handle_new_question_request, r, quiz_questions)
    partial_handle_solution_attempt = partial(handle_solution_attempt, r, quiz_questions)
    partial_cancel = partial(cancel, r, quiz_questions)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            Questions.SEND_QUESTION: [RegexHandler('^Новый вопрос$',
                                    partial_handle_new_question_request),
                            ],
            Questions.GET_ANSWER: [RegexHandler('^Сдаться$', partial_cancel),
                         MessageHandler(Filters.text,
                                partial_handle_solution_attempt)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
