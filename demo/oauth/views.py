import random
import requests
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse

# Create your views here.

def __random_string(n):
    '''create random string'''
    s = ''
    for c in random.sample('zyxwvutsrqponmlkjihgfedcba',n):
        s = s + c
    return s


def github_redirect(request):
    random_string = __random_string(10)
    request.session['github_state'] = random_string
    redirect_url = settings.GITHUB_REDIRECT + "?client_id=" + \
    settings.GITHUB_CLIENT_ID + "&redirect_uri=" + settings.REDIRECT_URL\
    +"&state="+ random_string
    return HttpResponseRedirect(redirect_url)

def github_auth(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    save_state = request.session.get('github_state',"no")
    if save_state == state:
        params = {"client_id":settings.GITHUB_CLIENT_ID, "client_secret":settings.GITHUB_CLIENT_SECERT, \
        "code":code, "state":state, "redirect_uri":settings.REDIRECT_URL}
        headers = {"Accept":"application/json"}
        url = settings.GITHUB_REDIRECT_EXCHANGE
        r = requests.post(url, params=params, headers=headers)
        access_token = r.json()['access_token']
        params = {"access_token":access_token}
        r = requests.get(settings.GITHUB_API, params=params)
        json_result = r.json()
        return render(request, 'oauth/index.html', {"result":json_result})
    else:
        raise Http404()

def home(request):
    '''home page'''
    return render(request, 'oauth/index.html')
