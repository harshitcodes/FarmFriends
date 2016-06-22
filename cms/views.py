
# third party stuff  ================================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save
from django.conf import settings
from django.template import RequestContext


# For mailing activation ===================================================
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import SuspiciousOperation
# cms stuff ==================================================================
from cms.forms import *
from cms.models import MyUser
# Create your views here.


@require_http_methods(['GET', 'POST'])
def base(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'GET':
        f = LoginForm();
    else:
        f = LoginForm(request.POST)
        if f.is_valid():
            user = f.get_user()
            auth_login(request, user)
            print("Valid")
            #return JsonResponse(data = {'success': True})
            return redirect('home')
        else:
            data = {'error': True, 'errors' : dict(f.errors.items())}
            return	JsonResponse(status = 400, data = data)

    return render(request, 'authentication/login.html',{'form': f})		


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'GET':
        f =SignupForm();
    else:
        f = SignupForm(request.POST)
        if f.is_valid():
            user = f.save();
            email_body_context = {
                'username' : user.username,
                'token': urlsafe_base64_encode(force_bytes(user.username)),
                'uid' : user.id,
                'protocol': 'http',
                'domain' : get_current_site(request).domain
            }
            body = loader.render_to_string('authentication/signup_email_body_text.html', email_body_context)
            email_message = EmailMultiAlternatives('Welcome To Proto',body, settings.DEFAULT_FROM_EMAIL, [user.email])
            email_message.send()
            return render(request, 'authentication/signup_email_sent.html', { 'email' : user.email })
    return render(request, 'authentication/signup.html', { 'form': f})


@require_GET
def logout(request):
    auth_logout(request)
    return redirect('base');


@require_GET
@login_required
def home(request):
    # print(request.user.profile_pic)

    return render(request, 'authentication/home.html', {})



@require_GET
def activate(request, uid = None, token = None):
    if request.user.is_authenticated():
        return redirect('home')
    '''
    try:
        user = MyUser.objects.get(id = uid)
    except MyUser.DoesNotExist:
        raise Http404('Invalid User')
    '''
    user = get_object_or_404(MyUser, id = uid)
    username_from_token = force_text(urlsafe_base64_decode(token))
    if user.is_active:
        return redirect('base')

    if user.username == username_from_token:
        user.is_active = True
        user.save()
        return render(request, 'authentication/activation_success.html')
    else:
        return render(request, 'authentication/activation_failure.html')    