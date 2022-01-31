from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def articles(request):
    keyword = request.GET.get("keyword")
    
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()

    return render(request,"articles.html",{"articles":articles})

def index(request):
    return render(request,"index.html")
    
def about(request):
    return render(request,"about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        # article.title = titleify(article.title)
        article.author = request.user
        article.save()

        # messages.success(request,"Article created successfully")
        return redirect("article:dashboard")
    return render(request,"addarticle.html",{"form":form})

def detail(request, id):
    article = get_object_or_404(Article, pk = id)
    comments = None
    if article:
        comments = Comment.objects.filter(article = id) 
    return render(request,"detail.html",{"article":article, "comments":comments })

@login_required(login_url = "user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, pk = id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        # messages.success(request,"Article updated successfully")
        return redirect("article:dashboard")

    # messages.error(request,"It has been an error. Try again.")

    return render(request,"update.html",{"form":form})

@login_required(login_url = "user:login")
def deleteArticle(request, id):

    article = get_object_or_404(Article, pk = id)
    article.delete()

    return redirect("article:dashboard")

    
def addComment(request,title):
    article = get_object_or_404(Article, title = title)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)

        newComment.article = article

        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":article.id}))