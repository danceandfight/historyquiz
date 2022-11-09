import os

def get_quiz_questions():
    filenames = os.listdir('quiz-questions')
    with open(f'quiz-questions/{filenames[0]}', encoding='KOI8-R') as f:
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
