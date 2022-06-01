
import random
from django.conf import Settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from .decorator import ajax_required
from django.http import  JsonResponse
import json
# Create your views here.

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
        data = request.body
        try:
            user = Settings.AUTH_USER_MODEL.get(email=data['email'])
            otp = random.randint(1000,9999)
            return JsonResponse({'status':'success', 'otp':otp})
        except:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'failed'})
        

        