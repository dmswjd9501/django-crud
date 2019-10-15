from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
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
    return render(request, 'accounts/signup.html', context)
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
