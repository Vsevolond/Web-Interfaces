import django.contrib.auth.backends
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


class Member(models.Model):
    info = models.ForeignKey(django.contrib.auth.backends.UserModel, on_delete=models.CASCADE)
    avatar = models.ImageField()
    rank = models.IntegerField()


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="questions")
    like_users = models.ManyToManyField(Member, related_name="likes")
    dislike_users = models.ManyToManyField(Member, related_name="dislikes")


class Answer(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now=True)
    correct = models.BooleanField(default=False)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="answers")
    like_users = models.ManyToManyField(Member, related_name="likes")
    dislike_users = models.ManyToManyField(Member, related_name="dislikes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="answers", related_query_name="answer")


class Tag(models.Model):
    name = models.CharField(max_length=10)
    rank = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="tags", related_query_name="tag")
