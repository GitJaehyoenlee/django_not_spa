from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
from instagram.forms import PostForm
from .models import Tag, Post

@login_required
def index(request):
    suggested_user_list = get_user_model().objects.all()\
            .exclude(pk=request.user.pk)\
            .exclude(pk__in=request.user.following_set.all())[:3]
    return render(request, "instagram/index.html", {
        "suggested_user_list": suggested_user_list,
    })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "새글이 등록되었습니다")
            return redirect("/") # TODO get_absolute_url 구현 필요
    else:
        form = PostForm()
    return render(request, "instagram/post_form.html", {
        "form": form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {
        "post": post,
    })

def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # db 에 카운트를 던져서 얻어옴
    # len(post_list) # 메모리에 로드한 후 개수를 세는 방식
    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
    })
