from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required


from .forms import CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    # 여기 들여쓰기 하지 않도록 주의하자 . 유효하지 않으면 이쪽으로 와야함
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)
    # 만약 POST 요청 -> 검증 실패하면 6 7 8 14 15 16 17 순서대로 실행 
    # 만약 GET 요청 -> 11 12 14 15 16 17 실행
    # 그때 form은 7번 라인의 request.POST 값 그대로 나타내주게!

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST) # 인자의 순서가 다름 / request에 사용자이름, 쿠키같은게 들어져서 옴
        if form.is_valid():
            user = form.get_user() # user 인스턴스를 가지고 와서
            auth_login(request, user) # login 시켜주는 함수에 넣어주자 로그인!
            return redirect(request.GET.get('next') or 'articles:index') # GET.get 딕셔너리에서 값 가지고 올때 오류안뜨고 None값 뜬다. 
            # 단축평가 : T or T이면 (앞에서가 T이면) 뒤를 평가할 필요 X
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        # 1. 사용자가 보낸 내용 담아서
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # 2. 검증
        if form.is_valid():
            form.save()
            return redirect('articles:index')
        # 3. 반영
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def password_change(request):
    # passwordchangeForm 상속받아
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # form에 담긴 유저 정보
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user) # 반드시 첫번째 인자로 user
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def profile(request, account_pk):
    # user = User.objects.get(pk=account_pk)
    User = get_user_model()
    user = get_object_or_404(User, pk=account_pk)
    context = {
        'user_profile' : user
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, account_pk):
    User = get_user_model()
    user_profile = get_object_or_404(User, pk=account_pk)
    if request.user != user_profile:
        if request.user in user_profile.followers.all():
           user_profile.followers.remove(request.user)
        else:
           user_profile.followers.add(request.user)
        
    return redirect('accounts:profile', account_pk)