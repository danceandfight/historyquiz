import logging
import os
import random
import redis

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from dotenv import load_dotenv
from enum import Enum
from quiz_questions_loader import get_quiz_questions

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


r = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'), 
        db=0,
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
        )


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


def handle_new_question_request(bot, update):
    quiz_questions = get_quiz_questions()
    current_question, answer = random.choice(list(quiz_questions.items()))
    update.message.reply_text(current_question)
    r.set(update.effective_user.id, current_question)
    
    return Questions.GET_ANSWER


def handle_solution_attempt(bot, update):
    quiz_questions = get_quiz_questions()
    answer = quiz_questions[r.get(update.effective_user.id)].replace('Ответ:', '').lower().strip().split('.')[0]
    if update.message.text.lower() in answer:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return Questions.SEND_QUESTION
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')


def cancel(bot, update):
    quiz_questions = get_quiz_questions()
    update.message.reply_text(quiz_questions[r.get(update.effective_user.id)])
    
    return Questions.SEND_QUESTION


def main():
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(telegram_bot_token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            Questions.SEND_QUESTION: [RegexHandler('^Новый вопрос$',
                                    handle_new_question_request),
                            ],
            Questions.GET_ANSWER: [RegexHandler('^Сдаться$', cancel),
                         MessageHandler(Filters.text,
                                handle_solution_attempt)],
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
