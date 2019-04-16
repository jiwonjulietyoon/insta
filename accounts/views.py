from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import LoginForm, CustomUserChangeForm

# Create your views here.
def login(request):
    if request.method == "POST": # POST : 실제 로그인 (세션에 유저 정보 추가)
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next 정의돼 있으면, 해당 URL로 redirect // 정의돼있지 않으면, posts:list로 redirect
            return redirect(request.GET.get('next') or 'posts:list')
    
    else: # GET : 로그인 정보 입력
        form = AuthenticationForm()
    return render(request, 'accounts/login2.html', {
        'form': form,
    })
    
    #######################################################################
    
    # login_form = LoginForm(request.POST)
    # if login_form.is_valid():
    #     username = login_form.cleaned_data['username']
    #     password = login_form.cleaned_data['password']
        
    #     user = authenticate(
    #         username=username,
    #         password=password
    #     )
        
    #     if user:
    #         auth_login(request, user)
    #         return redirect('posts:list')
    #     login_form.add_error(None, 'Incorrect ID or password')
    # else:
    #     login_form = LoginForm()
    # return render(request, 'accounts/login.html', {
    #     'login_form': login_form,
    # })

 ######################################################################
 
 
 
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
    

def signup(request):
    if request.method == "POST": # POST - 유저 등록
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:list')
        else:
            return redirect('accounts:signup')
    else: # GET - 유저 정보 입력 받음
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })
    

def people(request, username):
    # 사용자에 대한 정보
    people = get_object_or_404(get_user_model(), username=username)
    # 유저 객체 표현 방법:
    # 1. settings.AUTH_USER_Model  (from django.conf)
    # 2. get_user_model()  ###
    
    return render(request, 'accounts/people.html' ,{
        'people': people,
    })
    
    
# 회원 정보 변경 (편집 & 반영)
def update(request):
    if request.method == "POST":  # 반영
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user = user_change_form.save()
            return redirect('people', user.username)
    else: # "GET"  # 편집
        user_change_form = CustomUserChangeForm(instance=request.user)
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/update.html', {
            'user_change_form': user_change_form,
        })
    

# 회원 탈퇴
def delete(request):
    if request.method == "POST":  # 탈퇴 로직
        request.user.delete()
        return redirect('posts:list')
        # return redirect('accounts:signup')
    return render(request, 'accounts/delete.html')

# 비밀번호 변경
def password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', request.user.username)
    else: #"GET"
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html', {
            'password_change_form': password_change_form,
        })







