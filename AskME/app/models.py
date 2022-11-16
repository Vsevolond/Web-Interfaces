import random

import django.contrib.auth.backends
from django.db import models
from django.db.models import Count
from functools import partial

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



#class MemberManager(models.Manager):

class Member(models.Model):
    info = models.OneToOneField(django.contrib.auth.backends.UserModel, on_delete=models.CASCADE)
    avatar = models.ImageField(default="AskME/static/img/unknown.jpg", upload_to="avatars", blank=True)
    rank = models.IntegerField(blank=True, null=True, default=0)

    #objects = MemberManager()

    def __str__(self):
        return self.info.__str__()

    def get_avatar(self):
        return self.avatar.name


class Question(models.Model):
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="questions")
    like_users = models.ManyToManyField(Member, related_name="question_likes", blank=True)
    dislike_users = models.ManyToManyField(Member, related_name="question_dislikes", blank=True)

    def get_text(self):
        return self.text

    def get_date(self):
        return f'{self.date}'

    def get_author(self):
        return self.author

    def get_likes(self):
        return self.like_users.all().count()

    def get_dislikes(self):
        return self.dislike_users.all().count()

    def get_tags(self):
        return self.tags.all()

    def get_num_answers(self):
        return self.answers.all().count()

    def get_answers(self):
        return self.answers.all()

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="answers")
    like_users = models.ManyToManyField(Member, related_name="answer_likes", blank=True)
    dislike_users = models.ManyToManyField(Member, related_name="answer_dislikes", blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="answers", related_query_name="answer")

    def __str__(self):
        return self.text

    def get_date(self):
        return f'{self.date}'

    def get_author(self):
        return self.author

    def get_likes(self):
        return self.like_users.all().count()

    def get_dislikes(self):
        return self.dislike_users.all().count()


class TagManager(models.Manager):
    def pop_tags(self):
        return self.all().annotate(rank=Count('questions')).order_by('rank').reverse()[:10]


class Tag(models.Model):
    name = models.CharField(max_length=10)
    questions = models.ManyToManyField(Question, related_name="tags", related_query_name="tag")
    CLASS_TAGS = [("btn btn-primary", 'primary'), ("btn btn-secondary", 'secondary'), ("btn btn-success", 'success'),
                     ("btn btn-danger", 'danger'), ("btn btn-warning", 'warning'), ("btn btn-info", 'info'),
                     ("btn btn-dark", 'dark')]
    class_tag = models.CharField(max_length=20, choices=CLASS_TAGS, default='primary')
    objects = TagManager()

    COLORS = {
        'btn btn-primary': '#007bff',
        'btn btn-secondary': '#6c757d',
        'btn btn-success': '#28a745',
        'btn btn-danger': '#dc3545',
        'btn btn-warning': '#ffc107',
        'btn btn-info': '#17a2b8',
        'btn btn-dark': '#343a40'
    }

    # def __init__(self, *args):
    #     self.color = random.choice(COLOR_BUTTONS)
    #     super().__init__(*args)

    def color(self):
        return self.COLORS[self.class_tag]

    def rank(self) -> int:
        return self.questions.all().count()

    def questions_by_tag(self):
        return self.questions.all()

    def __str__(self):
        return self.name


