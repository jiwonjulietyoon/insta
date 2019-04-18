from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import LoginForm, CustomUserChangeForm, ProfileForm, CustomUserCreationForm
from .models import Profile, User

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
        else:
            return redirect('accounts:signup')
    else: # GET - 유저 정보 입력 받음
        form = CustomUserCreationForm()
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
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        # profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('people', user.username)
    else: # "GET"  # 편집
        user_change_form = CustomUserChangeForm(instance=request.user)
        
        ##### ISSUE:  instance 를 넣어줄 정보가 있는 유저가 있고, 없는 유저도 있다.
        ### Solution 1
        # if Profile.objects.get(user=request.user):
        #     profile = Profile.objects.get(user=request.user)
        # else:
        #     profile = Profile.objects.create(user=request.user)
            
        ### Solution 2    
        profile, created = Profile.objects.get_or_create(user=request.user) 
              # get_or_create : Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.
        profile_form = ProfileForm(instance=profile)
        
        
        return render(request, 'accounts/update.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form,
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

def follow(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    
    # 만약 현재 유저가 해당 유저를 이미 팔로우하고 있었으면, 언팔로우 (remove)
    if request.user in person.followers.all():
        person.followers.remove(request.user)
    
    # 반대로, 팔로우를 안 하고 있었다면 팔로우 한다.   (add)
    else:
        person.followers.add(request.user)
    
    return redirect('people', person.username)





