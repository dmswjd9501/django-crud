from IPython import embed
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET

from .forms import ArticleForm
from .models import Article, Comment


# Create your views here.
@require_GET
def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

# def new(request):
#     return render(request, 'articles/new.html')

    
def create(request):
    if request.method == 'POST':
        # POST 요청 -> 검증 및 저장
        article_form = ArticleForm(request.POST)
        embed()
        if article_form.is_valid():
            # 검증에 성공하면 저장하고, 
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            article = article_form.save()
            # redirect
            return redirect('articles:detail', article.pk)
    else:
    # GET 요청 -> Form
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증 실패 시 에러메세지와 입력값 채워진 Form context
    context = {
        'article_form' : article_form
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    # if request.method == 'POST':
    article.delete()
    return redirect('articles:index')
    # else:
    #     return redirect('articles:detail', article.pk)

# def edit(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     context = {
#         'article': article
#     }
#     return render(request, 'articles/edit.html', context)
\
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article) # 수정할 대상 : instance=article
        if article_form.is_valid():
            article = article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)

    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)


@require_POST
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment = Comment()
    comment.content = request.POST.get('comment_content')
    comment.article = article
    # comment.article_id = article_pk
    comment.save()
    return redirect('articles:detail', article_pk)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    # messages.add_message(request, messages.INFO, '댓글이 삭제 되었습니다.')
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('articles:detail', article_pk)