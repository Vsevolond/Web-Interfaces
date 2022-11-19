import os
from functools import partial
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth.backends import UserModel
from django.db import models
from app import models
import random, string, glob
from hashlib import sha256


def get_random_password():
    return ''.join(random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits, 8))


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        UserModel.objects.all().delete()
        models.Member.objects.all().delete()
        models.Question.objects.all().delete()
        models.Answer.objects.all().delete()
        models.Tag.objects.all().delete()
        models.VoteQuestion.objects.all().delete()
        models.VoteAnswer.objects.all().delete()
        ratio = kwargs['ratio']
        users_to_create = [UserModel(username=f'User{i}', #password=sha256(get_random_password().encode()).hexdigest(),
                           email=f'user{i}@mail.ru') for i in range(1, ratio+1)]
        models.UserModel.objects.bulk_create(users_to_create)
        included_extensions = [#'jpg', 'jpeg',
                               'png']
        icons = [file for file in os.listdir('./static/img/')
                      if any(file.endswith(ext) for ext in included_extensions)]
        members_to_create = [models.Member(profile=UserModel.objects.get(username=f'User{i}'),
                                 avatar=random.choice(icons)) for i in range(1, ratio + 1)]
        models.Member.objects.bulk_create(members_to_create)
        members = models.Member.objects.all()
        for i in range(1, ratio * 10 + 1):
            q = models.Question(author=random.choice(members), title=f'Question{i}',
                                text=f'Text of Question{i} about something')
            q.save()
        questions = models.Question.objects.all()
        answers_to_create = [models.Answer(question=random.choice(questions), author=random.choice(members),
                                 text=f'Text of Answer{i} for Question') for i in range(1, ratio * 100 + 1)]
        models.Answer.objects.bulk_create(answers_to_create)
        question_votes = [models.VoteQuestion(author=random.choice(members),
                                              question=random.choice(questions),
                                              type=random.choice(['like', 'dislike'])) for _ in range(ratio * 100)]
        models.VoteQuestion.objects.bulk_create(question_votes)
        answers = models.Answer.objects.all()
        answer_votes = [models.VoteAnswer(author=random.choice(members),
                                              answer=random.choice(answers),
                                              type=random.choice(['like', 'dislike'])) for _ in range(ratio * 100)]
        models.VoteAnswer.objects.bulk_create(answer_votes)
        tag_classes = ['btn btn-primary', 'btn btn-secondary', 'btn btn-success', 'btn btn-danger',
                       'btn btn-warning', 'btn btn-info', 'btn btn-dark']
        for i in range(1, ratio + 1):
            tag = models.Tag(name=f'tag{i}', class_tag=random.choice(tag_classes))
            tag.save()
            tag.questions.set(random.choices(questions))