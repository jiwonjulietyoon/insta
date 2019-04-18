from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def index(request):
    return redirect('posts:list')

@login_required
def create(request):
    if request.method == "POST":
        # 작성된 포스트(게시글)를 DB에 적용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:list')
    else: # GET 방식
        # 포스팅을 작성하는 form을 보여줌.
        form = PostForm()
        return render(request, 'posts/create.html', {
            'form': form
        })

def list(request):
    ##### 모든 포스트를 보여준다
    # posts = Post.objects.all()
    
    ##### 내가 팔로우한 사람들의 포스트 + 내가 작성한 포스트만 보여줌
    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(user_id__in=request.user.followings.all()) | Q(user=request.user)).order_by('-id')
        
        # my_filter = Q(user=request.user)
        # for user in request.user.followers.all():
        #     my_filter = my_filter | Q(user=user)
        # posts = Post.objects.filter(my_filter).order_by('-id')
    
    else:
        posts = None
    
    
    comment_form = CommentForm()
    return render(request, 'posts/list.html', {
        'posts': posts,
        'comment_form': comment_form,
    })

@login_required
@require_POST
def create_comment(request, post_id):
    comment_form = CommentForm(request.POST)
    post = get_object_or_404(Post, pk=post_id)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect('posts:list')

def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('posts:list')

    
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
    
@login_required
def like(request, id):
    # 1. like를 추가할 포스트를 가져옴
    post = get_object_or_404(Post, pk=id)
    
    # 2. 만약 유저가 해당 post를 이미 like했다면 like를 제거하고,
    #    like가 돼 있는 상태가 아니라면 like를 추가한다.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    
    return redirect('posts:list')

