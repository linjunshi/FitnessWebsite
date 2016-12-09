import requests
# get user_objects
from fitness.models import *
import base64
import os
import hashlib
import time
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect

base_url, from_email = 'http://cs4920.jwang.id.au:8000', 'gedanfitness@gmail.com'

# get_info done by Edward 7/10/16
def check_login (request):
    """get info function return the message, either confirmed or 0,
    to indicates success and failded, it store the login in status
    to the session to indicates this user has logged in"""

    if 'loginEmail' in request.POST:
        posted_email = request.POST['loginEmail']
        posted_password = hashlib.sha256(str(request.POST['loginPassword']).encode('utf-8')).hexdigest()
        try:
            user = UserAccounts.objects.get(email=posted_email)
            # print ("\n" + user + "\n")
            # print("\n\nemail = %s, password = %sn\n" %
            #         (posted_email, posted_password))
            if user.email == posted_email and user.password == posted_password:
                if user.email_verified == True:
                   register_session(request, user)
                   return HttpResponse("confirmed")
                else:
                   return HttpResponse("not verified")
        except Exception as e:
            # print("\n%s\n" % (e))
            pass
    return HttpResponse("0")


# register_user
def register_user (request):
    if 'signupEmail' in request.POST:
        posted_email = request.POST['signupEmail']
        posted_password = hashlib.sha256(str(request.POST['signupPassword']).encode('utf-8')).hexdigest()
        # posted_password = request.POST['signupPassword']
        posted_username = request.POST['signupUserName']
        random_token = base64.urlsafe_b64encode(os.urandom(16)).rstrip(b'=').decode('ascii')
        try:
            user = UserAccounts.objects.get(email=posted_email)
            return HttpResponse("deny")
            # print ("\n" + user + "\n")
        except Exception as e:
            try:
                user = UserAccounts(username = posted_username, email = posted_email,
                                    password = posted_password, secure_token = random_token)

                #Email information
                subject = 'GeDan Fitness - Email Verification'
                text_content = 'Dear ' + posted_username + ', please visit '+base_url+'/register/email/ and enter ' + random_token + ' as your token. Thanks, GeDan Fitness.'
                html_content = '<p>Dear '+ posted_username +', please visit <a href="'+base_url+'/register/email?registerEmail='+posted_email+'&token='+random_token+'">'+base_url+'/register/email?registerEmail='+posted_email+'&token='+random_token+'</a> to verify your email.</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [posted_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # TO-DO : comment the next 2 lines in the final product
                user.email_verified = 1 #require verification first
                register_session(request, user) #require verification first
                # print("\n\nemail = %s, password = %s, username = %s\n\n" %
                # (posted_email, posted_password, posted_username))
                user.save()
            except Exception as e:
                print(e)
            return HttpResponse("ok")
    return HttpResponse("deny")


def register_session (request, user):
    request.session["signed_in"] = True
    request.session["email"] = user.email
    request.session["username"] = user.username


# def user_logout(requests):
#     requests.session['signed_in'] = False


# email sending done by John
def send_password_reset (request):
    email_request = None
    token_request = None

    if request.method == 'POST':
       if 'email' in request.POST:
          email_request = request.POST['email']
       if 'token' in request.POST:
          token_request = request.POST['token']
    elif request.method == 'GET':
       if 'email' in request.GET:
          email_request = request.GET['email']
       if 'token' in request.GET:
          token_request = request.GET['token']

    if email_request != None and token_request == None:
       try:
          user = UserAccounts.objects.get(email=email_request)
          random_token = base64.urlsafe_b64encode(os.urandom(16)).rstrip(b'=').decode('ascii')
          user.forgotten_token = random_token
          user.forgotten_token_created = time.time()
          user.save()

          subject = 'GeDan Fitness - Password Reset Link'
          text_content = 'Dear ' + user.username + ', please visit '+base_url+'/register/forgotPassword/ and enter ' + random_token + ' as your token. This link is valid for only 24 hours, and only the latest link requested is valid. Thanks, GeDan Fitness.'
          html_content = '<p>Dear '+ user.username +', please visit <a href="'+base_url+'/register/forgotPassword?email='+user.email+'&token='+random_token+'">'+base_url+'/register/forgotPassword?email='+user.email+'&token='+random_token+'</a> to verify your email. This link is valid for only 24 hours, and only the latest link requested is valid.</p>'
          msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
          msg.attach_alternative(html_content, "text/html")
          msg.send()
          
       except Exception as e:
          print(e) #email provided does not belong to valid user or error in sending
       return HttpResponse("sent")

    elif email_request != None and token_request != None:
       try:
          user = UserAccounts.objects.get(email=email_request)
          if user.forgotten_token == token_request and user.forgotten_token_created+86400 > time.time(): #24hour expiry
             if 'password' in request.POST:
                user.forgotten_token_created = 0
                user.password = hashlib.sha256(str(request.POST['password']).encode('utf-8')).hexdigest()
                user.save()
                register_session(request, user)
                #return HttpResponse("password reset")
                return HttpResponseRedirect(base_url+"/profile/home/")
             else:
                return render(request, 'forgotPassword.html', {'email': email_request, 'token': token_request})
          else:
             return HttpResponse("<meta http-equiv='refresh' content='2; url="+base_url+"'>Error, incorrect token or token has expired.")
       except Exception as e:
          print(e)
    return HttpResponse("error")

def register_email (request):
    responseMessage = "Error, email address or token provided is incorrect."
    registeringEmail = None
    receivedToken = None

    if request.method == 'POST' and 'registerEmail' in request.POST and 'token' in request.POST:
       registeringEmail = request.POST['registerEmail']
       receivedToken = request.POST['token']
    elif request.method == 'GET' and 'registerEmail' in request.GET and 'token' in request.GET:
       registeringEmail = request.GET['registerEmail']
       receivedToken = request.GET['token']
    else:
       if request.session["signed_in"] == True:
           return HttpResponseRedirect(base_url+"/profile/home/")
       return render(request, 'registerEmail.html')

    if not registeringEmail == None and not receivedToken == None:
       try:
           user = UserAccounts.objects.get(email = registeringEmail)
           if user.email_verified == True:
              responseMessage = "Email already verified"
           elif user.secure_token == receivedToken:
              user.email_verified = True
              user.save()
              responseMessage = "<meta http-equiv='refresh' content='1; url="+base_url+"'>Email is now verified. You should be redirected in one second."
              register_session(request, user)
       except Exception as e:
           pass
    return HttpResponse(responseMessage)
