from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from .models import article,Comment
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = article.objects.all()

    return render(request,"articles.html",{"articles":articles})
def index(request):
    return render(request,"index.html")
    
def about(request):
    return render(request,"about.html")
@login_required(login_url = "user:login")
def dashboard(request):
    articles = article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)
@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.slug = slugify(article.title)
        article.author = request.user
        article.save()

        messages.success(request,"Article created successfully")
        return redirect("article:dashboard")
    return render(request,"addarticle.html",{"form":form})
def detail(request,slug):
    #article = Article.objects.filter(id = id).first()   
    article_ = get_object_or_404(article, slug=slug)
    comments = article_.comments.all()
    return render(request,"detail.html",{"article":article_,"comments":comments })
@login_required(login_url = "user:login")
def updateArticle(request, slug):

    article_ = get_object_or_404(article, slug=slug)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article_)
    if form.is_valid():
        article_ = form.save(commit=False)
        
        article_.author = request.user
        article_.save()

        messages.success(request,"The article has been successfully updated")
        return redirect("article:dashboard")


    return render(request,"update.html",{"form":form})
@login_required(login_url = "user:login")
def deleteArticle(request,slug):
    article_ = get_object_or_404(article,slug=slug)

    article_.delete()

    messages.success(request,"Article Successfully Deleted")

    return redirect("article:dashboard")
def addComment(request,slug):
    article_ = get_object_or_404(article, slug=slug)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author  = comment_author, comment_content = comment_content)

        newComment.article = article_

        newComment.save()
    return redirect(reverse("article:detail",kwargs={"slug":slug}))
    