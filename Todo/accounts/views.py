
from dataclasses import Field
import random
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from .decorator import ajax_required
from django.http import  JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import password_reset_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
import json
from Todo.settings import EMAIL_HOST_USER
from .form import UserSignUpForm
# Create your views here.

User = get_user_model()

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@ajax_required
def loginUser(request):
    if request.method == 'POST':
        resp = {}
        loginInfo = json.loads(request.body)
        user = authenticate(request,
                            username=loginInfo['username'],
                            password=loginInfo['password'])
        if user: 
            if user.is_active:
                login(request, user)
                resp['loginStatus'] = 'success'
            else:
                resp['loginStatus'] = 'disabled'
        else:
            resp['loginStatus'] = 'notfound'
        return JsonResponse(resp)
    return HttpResponseBadRequest()

@login_required
@ajax_required
def password_change_api(request):
    if request.method == 'POST':
        resp = {}
        formData = json.loads(request.body)
        if request.user.check_password(formData['old_password']):
            request.user.set_password(formData['new_password1'])
            request.user.save()
            resp['password_change'] = 'success'
        else:
            resp['password_change'] = 'error'
        return JsonResponse(resp)
    return JsonResponse({'password_change': 'failed'})

def password_reset(request):
    return render(request, 'registration/password_reset_form.html')

@ajax_required
def password_reset_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(email=data['email'])
            if user.is_active:
                site = get_current_site(request)
                html_message = render_to_string(
                    'registration/password_reset_email.html',
                    {
                        'user': user,
                        'protocol' : 'http',
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': password_reset_token.make_token(user)
                    })
                plain_message = strip_tags(html_message)
                send_mail(
                    'RESET PASSWORD REQUEST',
                    plain_message,
                    EMAIL_HOST_USER,
                    [data['email'],],
                    html_message=html_message
                )
                return JsonResponse({'status':'success'})
            return JsonResponse({'status':'disabled'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'notfound'})
    return JsonResponse({'status':'failed'})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        context = {'is_valid':True, 'uidb64':uidb64, 'token':token}
    else:
        context = {'is_valid':False}
    return render(request, 'registration/password_reset_confirm.html', context)

@ajax_required
def password_reset_confirm_api(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            
        if user is not None and password_reset_token.check_token(user, token):
            data = json.loads(request.body)
            user.set_password(data['new_password'])
            user.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'invalid'})
    else:
        return JsonResponse({'status':'failed'})
        
def signup(request):
    form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form':form})

@ajax_required
def signup_api(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            newUser.set_password(form.cleaned_data['password'])
            newUser.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status':'error', 'errors':form.errors.as_json()})
    