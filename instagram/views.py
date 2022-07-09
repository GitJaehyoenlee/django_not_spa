from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
from instagram.forms import PostForm
from .models import Tag, Post


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