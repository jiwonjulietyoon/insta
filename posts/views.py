from django.shortcuts import render, redirect
from .forms import PostForm

# Create your views here.
def create(request):
    if request.method == "POST":
        # 작성된 포스트(게시글)를 DB에 적용
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:create')
    else: # GET 방식
        # 포스팅을 작성하는 form을 보여줌.
        form = PostForm()
        return render(request, 'posts/create.html', {
            'form': form
        })


    
    
    
    