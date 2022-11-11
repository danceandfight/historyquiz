import os
import random
import redis
from dotenv import load_dotenv

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from quiz_questions_loader import get_quiz_questions


def send_message(event, vk, msg, keyboard):
    vk.messages.send(
        user_id=event.user_id,
        message=msg,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


def create_keyboard():

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.PRIMARY)
    
    return keyboard

def handle_new_question_request(event, vk, keyboard, quiz_questions, redis_db):
    current_question, answer = random.choice(list(quiz_questions.items()))
    send_message(event, vk, current_question, keyboard)
    print(f'{current_question}\n{answer}')
    redis_db.set(event.user_id, current_question)


def handle_solution_attempt(event, vk, keyboard, quiz_questions, redis_db):
    answer = quiz_questions[redis_db.get(event.user_id)].replace('Ответ:', '').lower().strip().split('.')[0]
    if event.text.lower() in answer:
        send_message(event, vk, 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»', keyboard)
    else:
        send_message(event, vk, 'Неправильно… Попробуешь ещё раз?', keyboard)

def cancel(event, vk, keyboard, quiz_questions, redis_db):
    send_message(event, vk, quiz_questions[redis_db.get(event.user_id)], keyboard)


def main():
    load_dotenv()
    r = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'), 
        db=0,
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
        )

    vk_session = vk_api.VkApi(token=os.getenv('VK_GROUP_TOKEN'))
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = create_keyboard()
    quiz_questions = get_quiz_questions()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text in ['Привет!', 'Добрый день!']:
                send_message(event, vk, 'Привет! Я бот для викторин!', keyboard)
            try:
                if event.text == 'Сдаться':
                    cancel(event, vk, keyboard, quiz_questions, r)
                elif event.text == 'Новый вопрос':
                    handle_new_question_request(event, vk, keyboard, quiz_questions, r)
                else:
                    handle_solution_attempt(event, vk, keyboard, quiz_questions, r)
            except Exception:
                pass

if __name__ == '__main__':
    main()