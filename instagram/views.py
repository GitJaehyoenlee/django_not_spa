from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Create your views here.
from django.utils import timezone

from instagram.forms import PostForm, CommentForm
from .models import Tag, Post

@login_required
def index(request):
    #작성자가 본인이나, 팔로워인 경우만 가져옴

    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
                .filter(
                    Q(author=request.user) |
                    Q(author__in=request.user.following_set.all())
                )\
                .filter(
                    created_at__gte=timesince # less then equal
                )
    suggested_user_list = get_user_model().objects.all()\
            .exclude(pk=request.user.pk)\
            .exclude(pk__in=request.user.following_set.all())[:3]

    comment_form = CommentForm()
    return render(request, "instagram/index.html", {
        "suggested_user_list": suggested_user_list,
        "post_list": post_list,
        "comment_form": comment_form,
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
    comment_form = CommentForm()
    return render(request, "instagram/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    print("t")
    messages.success(request, f"포스팅 #{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅 #{post.pk}를 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form =  CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # is_ajax : ajax 여부를 판단하는 방식 : 현재는 구분자를 구별하지 못해 제거됨
            if request.is_ajax():
                return render(request, "instagram/_comment.html",{
                    'comment': comment
                })
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html",{
        "form" : form,
    })


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # db 에 카운트를 던져서 얻어옴
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False
    # len(post_list) # 메모리에 로드한 후 개수를 세는 방식
    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
        "is_follow": is_follow
    })
