import os


def get_quiz_questions(quiz_directory):
    filenames = os.listdir(quiz_directory)
    question_answer_pairs = {}
    for filename in filenames:
        with open(f'{quiz_directory}/{filename}', encoding='KOI8-R') as f:
            quiz_questions = f.read()
        quiz_question_chunks = quiz_questions.split('\n\n')
        for chunk in quiz_question_chunks:
            if chunk.startswith('Вопрос'):
                key = chunk
            if chunk.startswith('Ответ'):
                value = chunk
                question_answer_pairs[key] = value
    return question_answer_pairs
