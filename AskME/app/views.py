from django.http import HttpResponse
from django.shortcuts import render
from . import models

# Create your views here.

def index(request):
    context = {'questions': models.QUESTIONS, 'pop_tags': models.POP_TAGS, 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/index.html', context=context)

def ask(request):
    context = {'pop_tags': models.POP_TAGS, 'page': "Home", 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/ask.html', context=context)

def settings(request):
    context = {'pop_tags': models.POP_TAGS, 'page': "Settings", 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/settings.html', context=context)

def question(request, id: int):
    question_item = models.QUESTIONS[id]
    context = {'question': question_item, 'pop_tags': models.POP_TAGS, 'page': "Home", 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/question.html', context=context)

def tag(request, question_tag: str):
    tag_questions = []
    for question_item in models.QUESTIONS:
        if question_tag in question_item['tags']:
            tag_questions.append(question_item)

    context = {'questions': tag_questions, 'tag': question_tag, 'pop_tags': models.POP_TAGS, 'page': "Home", 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/tag.html', context=context)

def hot(request):
    hot_questions = []
    for question_id in sorted(models.HOT_QUESTIONS):
        hot_questions.append(models.QUESTIONS[question_id])
    context = {'questions': hot_questions, 'pop_tags': models.POP_TAGS, 'page': "Home", 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/hot.html', context=context)

def login(request):
    context = {'pop_tags': models.POP_TAGS, 'page': "Home", 'is_auth': models.IS_AUTH}
    return render(request, 'not_auth/login.html', context=context)

def signup(request):
    context = {'pop_tags': models.POP_TAGS, 'page': "Home", 'is_auth': models.IS_AUTH}
    return render(request, 'not_auth/signup.html', context=context)
