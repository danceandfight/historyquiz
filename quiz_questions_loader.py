import os
from dotenv import load_dotenv


def get_quiz_questions():
    quiz_directory = os.getenv('QUIZ_DIRECTORY')
    filenames = os.listdir(quiz_directory)
    with open(f'{quiz_directory}/{filenames[0]}', encoding='KOI8-R') as f:
        quiz_questions = f.read()
    quiz_question_chunks = quiz_questions.split('\n\n')
    question_answer_pairs = {}
    for chunk in quiz_question_chunks:
        if chunk.startswith('Вопрос'):
            key = chunk
        if chunk.startswith('Ответ'):
            value = chunk
            question_answer_pairs[key] = value
    return question_answer_pairs

if __name__ == '__main__':
    load_dotenv()
    get_quiz_questions()