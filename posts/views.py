from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_http_methods

# Create your views here.
def create(request):
    if request.method == "POST":
        # 작성된 포스트(게시글)를 DB에 적용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else: # GET 방식
        # 포스팅을 작성하는 form을 보여줌.
        form = PostForm()
        return render(request, 'posts/create.html', {
            'form': form
        })

def list(request):
    # 모든 포스트를 보여준다
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {
        'posts': posts,
    })
    
#@require_POST   # POST method만 accept하고 싶을 때 => if request.method == "POST": 를 쓰는 것과 동일
def delete(request, id):
    post = Post.objects.get(pk=id)
    if post.user != request.user:
        return redirect('posts:list')
    post.delete()
    return redirect('posts:list')

def update(request, id):
    # post = Post.objects.get(pk=id)
    post = get_object_or_404(Post, pk=id)
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, 'posts/update.html', {
            'form': form,
        })
    else: # "POST"
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    
    