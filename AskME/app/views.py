from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# Create your views here.

def index(request):
    paginator = Paginator(models.QUESTIONS, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'paginator': paginator, 'page': page_obj, 'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/index.html', context=context)

def ask(request):
    context = {'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/ask.html', context=context)

def settings(request):
    context = {'pop_tags': models.POP_TAGS, 'is_home': False, 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/settings.html', context=context)

def question(request, id: int):
    if id < len(models.QUESTIONS):
        question_item = models.QUESTIONS[id]
        context = {'question': question_item, 'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
        return render(request, 'auth_ok/question.html', context=context)
    else:
        return HttpResponse("There is no such question")

def tag(request, question_tag: str):
    tag_questions = []
    for question_item in models.QUESTIONS:
        if question_tag in question_item['tags']:
            tag_questions.append(question_item)

    if len(tag_questions) > 0:
        paginator = Paginator(tag_questions, 3)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        context = {'paginator': paginator, 'page': page_obj, 'tag': question_tag, 'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
        return render(request, 'auth_ok/tag.html', context=context)
    else:
        return HttpResponse("There are no questions with this tag")

def hot(request):
    hot_questions = []
    for question_id in sorted(models.HOT_QUESTIONS):
        hot_questions.append(models.QUESTIONS[question_id])
    paginator = Paginator(hot_questions, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'paginator': paginator, 'page': page_obj, 'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
    return render(request, 'auth_ok/hot.html', context=context)

def login(request):
    context = {'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
    return render(request, 'not_auth/login.html', context=context)

def signup(request):
    context = {'pop_tags': models.POP_TAGS, 'is_home': True, 'is_auth': models.IS_AUTH}
    return render(request, 'not_auth/signup.html', context=context)
