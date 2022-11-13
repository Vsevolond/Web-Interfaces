from django.db import models

IS_AUTH = True

HOT_QUESTIONS = [
    1, 4, 7
]

POP_TAGS = [
    {'name': 'Swift', 'color': "btn btn-danger"},
    {'name': 'Xcode', 'color': "btn btn-warning"},
    {'name': 'tag7', 'color': "btn btn-success"},
    {'name': 'html', 'color': "btn btn-primary"},
    {'name': 'css', 'color': "btn btn-secondary"},
    {'name': 'tag4', 'color': "btn btn-dark"},
]

BEST_MEMBERS = [
    'Mr. Freeman',
    'Dr. House',
    'Bender',
    'Queen Victoria',
    'V. Pupkin'
]

QUESTIONS = []
for id in range(100):
    ANSWERS = []
    for i in range(id*id):
        ANSWERS.append({
            'id': i,
            'text': f'Text of Answer № {i}'
        })
    QUESTIONS.append({
        'id': id,
        'title': f'Question № {id}',
        'text': f'Text of Question № {id}',
        'ans_num': id * id,
        'answers': ANSWERS,
        'tags': [f'tag{i}' for i in range(id)]
    })

