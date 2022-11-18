from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# Create your views here.


def base_context():
    pop_tags = [{'name' : f'{pop_tag}', 'class_tag' : f'{pop_tag.class_tag}'}
                for pop_tag in models.Tag.objects.pop_tags()]
    best_members = models.Member.objects.best_members()
    return {'pop_tags': pop_tags,
            'best_members': best_members, 'is_home': True, 'is_auth': models.IS_AUTH}


def paginate(request, objects_list, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return paginator, page_obj


def index(request):
    questions = models.Question.objects.all()
    paginator, page_obj = paginate(request, questions, 3)
    context = base_context()
    context.update({'paginator': paginator, 'page': page_obj})
    return render(request, 'main/index.html', context=context)


def ask(request):
    context = base_context()
    return render(request, 'main/ask.html', context=context)


def settings(request):
    context = base_context()
    context['is_home'] = False
    return render(request, 'main/settings.html', context=context)


def question(request, id: int):
    if id <= models.Question.objects.last().id:
        question_item = models.Question.objects.get(id=id)
        paginator, page_obj = paginate(request, question_item.get_answers(), 5)
        context = base_context()
        context.update({'paginator': paginator, 'page': page_obj, 'question': question_item})
        return render(request, 'main/question.html', context=context)
    else:
        return HttpResponse(status=404, content="There is no such question")


def tag(request, tag_name: str):
    if models.Tag.objects.filter(name=tag_name).count() > 0:
        tag = models.Tag.objects.get(name=tag_name)
        tag_questions = tag.questions_by_tag()
        paginator, page_obj = paginate(request, tag_questions, 3)
        context = base_context()
        context.update({'paginator': paginator, 'page': page_obj, 'tag': tag})
        return render(request, 'main/tag.html', context=context)
    else:
        return HttpResponse(status=404, content="There are no questions with this tag")


def hot(request):
    hot_questions = models.Question.objects.hot_questions()
    paginator, page_obj = paginate(request, hot_questions, 3)
    context = base_context()
    context.update({'paginator': paginator, 'page': page_obj})
    return render(request, 'main/hot.html', context=context)


def login(request):
    context = base_context()
    return render(request, 'main/login.html', context=context)


def signup(request):
    context = base_context()
    return render(request, 'main/signup.html', context=context)
