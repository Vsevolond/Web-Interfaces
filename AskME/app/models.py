import random
from django.contrib.auth.backends import UserModel
from django.db import models
from django.db.models import Count, Sum
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    for i in range(id * id):
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


class MemberManager(models.Manager):
    def best_members(self):
        return self.annotate(rating=Count('questions')+Count('answers')).order_by('-rating')[:10]


class Member(models.Model):
    profile = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    avatar = models.ImageField(default="unknown.jpg", upload_to="avatars", blank=True)

    objects = MemberManager()

    def __str__(self):
        return self.profile.__str__()

    def get_avatar(self):
        return 'img/' + self.avatar.name


class QuestionManager(models.Manager):
    def hot_questions(self):
        return self.all().annotate(rank=Count('answers')).order_by('-rank')[:10]


class Question(models.Model):
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="questions")

    objects = QuestionManager()

    # @property
    # def rank(self):
    #     return self.get_likes() - self.get_dislikes()

    def get_answers(self):
        return self.answers.all()

    def get_num_answers(self):
        return self.get_answers().count()

    def get_likes(self):
        return self.votes.filter(type='like').count()

    def get_dislikes(self):
        return self.votes.filter(type='dislike').count()

    def get_text(self):
        return self.text

    def get_date(self):
        return f'{self.date}'

    def get_author(self):
        return self.author

    def get_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.title


class VoteQuestion(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes")
    TYPE = [('like', '+'), ('dislike', '-')]
    type = models.CharField(max_length=7, choices=TYPE)


class Answer(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    correct = models.BooleanField(default=False)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    # @property
    # def rank(self) -> int:
    #     return self.get_likes() - self.get_dislikes()

    def get_likes(self):
        return self.votes.filter(type='like').count()

    def get_dislikes(self):
        return self.votes.filter(type='dislike').count()

    def __str__(self):
        return self.text

    def get_date(self):
        return f'{self.date}'

    def get_author(self):
        return self.author


class VoteAnswer(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="votes")
    TYPE = [('like', '+'), ('dislike', '-')]
    type = models.CharField(max_length=7, choices=TYPE)


# class Vote(models.Model):
#     author = models.OneToOneField(Member, on_delete=models.CASCADE)
#     #question_or_answer = models.ForeignKey(to=models, on_delete=models.CASCADE, related_name="votes")
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
#     object_id = models.PositiveIntegerField(null=True)
#     content_object = GenericForeignKey('content_type', 'object_id')
#     TYPE = [('like', '+'), ('dislike', '-')]
#     type = models.CharField(max_length=7, choices=TYPE)


class TagManager(models.Manager):
    def pop_tags(self):
        return self.all().annotate(rank=Count('questions')).order_by('-rank')[:10]


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

    def color(self):
        return self.COLORS[self.class_tag]

    def questions_by_tag(self):
        return self.questions.all()

    def __str__(self):
        return self.name

