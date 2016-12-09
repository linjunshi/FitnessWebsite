from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
import time
import requests
import json
import smtplib
from fitness.ml import give_recommendation
import os
import hashlib


# get user_objects
from fitness.models import *
from django.db.models import Q

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from fitnessteaching import settings
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# Cherry Zhao 14-09-2016 START
'''
def food(request, food_id):
        r = requests.get('http://api.nal.usda.gov/ndb/reports/?ndbno=' + food_id + '&type=f&format=json&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        j = json.loads(r)
        output = ""
        output += ("<h3>" + j['report']['food']['name'] + "</h3> <br/>")
        output += ("<i>" + j['report']['food']['fg'] + "</i> <br/> <hr/>")
        output += ("<b> Nutrients </b><br/>")
        output += ("<table>")
        for item in j['report']['food']['nutrients']:
                output += ("<tr> <th>" + item['name'] + "</th>" + "<th>" + str(item['value']) + item['unit'] + "</th> </tr>")
        output += ("</table>")
        #for item in j['report']['item']:
        #       output += (item['name'] + "<br/>" + item['id'] + "<hr/>")
        return HttpResponse(output)

def foodGroup(request, group_id):
        r = requests.get('http://api.nal.usda.gov/ndb/search?format=json&fg=' + group_id + '&sort=n&max=50&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        j = json.loads(r)
        output = ""
        for item in j['list']['item']:
                output += ("<a href=\"../../" + item['ndbno'] + "/food/\">" + item['name'] + "<br/>" + item['ndbno'] + "</a> <hr/>")
        return HttpResponse(output)

def foodGroups(request):
        r = requests.get('http://api.nal.usda.gov/ndb/list?format=json&lt=g&sort=n&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        j = json.loads(r)
        template = get_template('test01.html')
        html = template.render({'foodGroups' : j})
        output = "<ul>"
        #for item in j['list']['item']:
        #       output += ("<li> <a href=\"../" + item['id'] + "/foodGroup/\">" + item['name'] + "</a> </li>")
        #output += "</ul>"
        #return HttpResponse(html)
'''

# Modified by Martin 16/09/2016
# Modified by Martin 16/09/2016

# Home page function
def home(request):
        return render(request, 'home_page.html')

def register(request):
    # print("\n\n\n%s\n\n\n" % "signed_in" in request.session)
    if "signed_in" in request.session and request.session["signed_in"] == True:
       return HttpResponseRedirect("/profile/home/")

    userEmail = request.POST.get("loginEmail")
    userPassword = request.POST.get("loginPassword")
    return render(request, 'sign_in.html')

def planner(request):
    # if 'category' in request.POST and request.POST['category'] is not None:
        # user = UserAccounts.objects.get(email=request.session['email'])
        # print("\n\nusername = %s\n\n" % user.username)
        # user.training_target = request.POST['category']
        # user.save()
        # list_of_links = give_recommendation(user.email)
    # print("'category' in request.POST = %s" % 'category' in request.POST)
    all_cats = FitnessCategories.objects.all()
    return render(request, 'planner.html', locals())

# Fitness muscle list function
def fitness(request):
        return render(request, 'fitness.html')

# Fitness video interface function
def video(request):
        return render(request, 'video_list.html')

def blah(request):
        return render(request, 'blah.html')

# Main category of food list function
def food_level1(request):
        # Get category list
        get_data = requests.get('http://api.nal.usda.gov/ndb/list?format=json&lt=g&sort=n&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        load_data = json.loads(get_data)

        # Set category level
        category_level = "main"

        return render(request, 'food.html', {'foodGroups' : load_data, 'level' : category_level})

# Sub category of food list function
def food_level2(request, group_id):
        # Get category list
        get_data = requests.get('http://api.nal.usda.gov/ndb/search?format=json&fg=' + group_id + '&sort=n&max=50&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        load_data = json.loads(get_data)

        # Set category level
        category_level = "sub"

        return render(request, 'food.html', {'foodGroups' : load_data,
                                                                                 'level' : category_level})
# Detail of food function
def food_level3(request, group_id, food_id):
        # Get category list
        get_group_data = requests.get('http://api.nal.usda.gov/ndb/search?format=json&fg=' + group_id +
                                                                  '&sort=n&max=50&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        load_group_data = json.loads(get_group_data)

        # Get food information
        get_food_data = requests.get('http://api.nal.usda.gov/ndb/reports/?ndbno=' + food_id +
                                                                 '&type=f&format=json&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        load_food_data = json.loads(get_food_data)

        # Set category level
        category_level = group_id

        return render(request, 'food.html', {'foodGroups' : load_group_data,
                                                                                 'foodDetail' : load_food_data,
                                                                                 'level' : category_level})

# Function of search
def search(request):
    # Get keyword
    keyword = request.GET.get('keyword')
    ndbno = request.GET.get('ndbno')

    get_search_result = requests.get('http://api.nal.usda.gov/ndb/search/?format=json&q=' + keyword + '&sort=n&max=50&offset=0&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text

    load_search_result = json.loads(get_search_result)

    food_amount = len(load_search_result)

    # Get food information
    load_food_data = "load_group_data"
    if ndbno:
        get_food_data = requests.get('http://api.nal.usda.gov/ndb/reports/?ndbno=' + ndbno +
                                                                 '&type=f&format=json&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
        load_food_data = json.loads(get_food_data)

    # video search part
    searched_videos = []
    all_videos = FitnessVideo.objects.all()
    for video in all_videos:
        if keyword in video.name:
            searched_videos.append(video)
    video_search_status = "Error" if len(searched_videos) == 0 else "Success"
    video_amount = len(searched_videos)
    #result_amount = len(load_food_data) + len(searched_videos)

    # user search part
    searched_users = []
    all_users = UserAccounts.objects.all()
    for user in all_users:
        if keyword in user.username:
            searched_users.append(user)
    user_search_status = "Error" if len(searched_users) == 0 else "Success"
    user_amount = len(searched_users)

    return render(request, 'search.html', {'result': load_search_result, 'keyword': keyword, 'ndbno': ndbno, 'foodDetail': load_food_data, 'searched_videos' : searched_videos, 'searched_users':searched_users, 'video_amount':video_amount,'user_amount':user_amount, 'food_amount':food_amount})

def food_search(request, keyword, food_id):
    # Get food information
    get_food_data = requests.get('http://api.nal.usda.gov/ndb/reports/?ndbno=' + food_id +
                                '&type=f&format=json&api_key=CUR7LCIwsCLTDq1UI5STCloAG7rAUuX7fTLfPvVN').text
    load_food_data = json.loads(get_food_data)
    category_level = "search"
    return render(request, 'food.html', {'foodDetail' : load_food_data,
                                        'level' : category_level,
                                        'keyword' : keyword,
                                        'food_id' : food_id})

def video_category(request, fitness):
    fitness = "category"
    # return render(request, 'fitness.html', {'page' : fitness})
    fitness_video_list = []
    video_list = list(FitnessCategories.objects.all())

    for fitness_type in video_list:
        fitness_type = str(fitness_type)
        fitness_video_list.append(fitness_type)
    return render( request, 'fitness.html', {'fitness_video_list' : fitness_video_list, 'page': fitness} )


def video_list(request, group_id):
        fitness = "videos"
        return render(request, 'fitness.html', {'page' : fitness})

# def sign_up(request):
#         getFirstName = request.POST.get("firstName")
#         getLastName = request.POST.get("lastName")
#         getSignUpEmail = request.POST.get("signupEmail")
#         getSignUpPassword = request.POST.get("signupPassword")
#
#         return render(request, 'home_page.html')

def profile(request, sub):
    update = "no"
    male = ""
    female = ""
    athlete = ""
    notAthlete = ""
    heartDisease = ""
    notHeartDisease = ""
    smoke = ""
    notSmoke = ""
    medicalImplant = ""
    notMedicalImplant = ""
    attendence = ""

    # get user email address
    user_email = request.session['email']
    try:
        user = UserAccounts.objects.get(email=user_email)
        getUpdateStatus = request.POST.get("submit")

        user_total = UserAccounts.objects.all()
        user.user_avatar_dir = '/img/avatar1.jpg'

        if getUpdateStatus == 'account_username':
            update = getUpdateStatus
            user.username = request.POST.get("username")
            #
            # import os
            # print("path = %s\n" % os.getcwd())
            try:
                f = request.FILES["fileToUpload"]
                destination = open('fitness/static/img/'+str(user.id)+'.jpg', 'wb+')
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
                if os.path.exists("fitness/static/img/"+str(user.id)+'.jpg'):
                    user.user_avatar_dir = '/img/%d.jpg' % user.id
                else:
                    user.user_avatar_dir = '/img/avatar1.jpg'
            except Exception as e:
                # if user.user_avatar_dir == None:
                user.user_avatar_dir = '/img/avatar1.jpg'

            # print("\nuploaded_file = %s\n\n" % uploaded_file.name)
        elif getUpdateStatus == 'account_location':
            update = getUpdateStatus

            try:
                user.last_location_lat = float(request.POST.get("last_location_lat"))
            except Exception as e:
                user.last_location_lat = 0.0

            try:
                user.last_location_long = float(request.POST.get("last_location_long"))
            except Exception as e:
                user.last_location_long = 0.0
            # Waiting for latitude and longititude

        elif getUpdateStatus == 'account_attendence':
            update = getUpdateStatus

            try:
                last_date = float(user.last_attend_date)
            except Exception as e:
                last_date = 0.0

            if (time.time() - last_date) > 3600:
                user.attendence += 1
                user.last_attend_date = time.time()
                attendence = "Sign up successfully"
            else:
                attendence = "You already signed up today :)"


        elif getUpdateStatus == 'personal':
            update = getUpdateStatus
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")

            try:
                user.age = int(request.POST.get("age"))
            except Exception as e:
                user.age = 0

            user.athlete = (request.POST.get("athlete") == "TRUE")
            user.heart_disease = (request.POST.get("heart_disease") == "TRUE")
            user.smoking = (request.POST.get("smoking") == "TRUE")
            user.medical_implant = (request.POST.get("medical_implant") == "TRUE")

            if request.POST.get("user_gender") == "male":
                user.gender = 'M'
            elif request.POST.get("user_gender") == "female":
                user.gender = 'F'
            else:
                user.gender = ''

            try:
                user.weight = float(request.POST.get("weight"))
            except Exception as e:
                user.weight = 0.0

            try:
                user.height = float(request.POST.get("height"))
            except Exception as e:
                user.height = 0.0

            try:
                user.blood_pressure_systolic = float(request.POST.get("blood_pressure_systolic"))
            except Exception as e:
                user.blood_pressure_systolic = 0.0

            try:
                user.blood_pressure_diastolic = float(request.POST.get("blood_pressure_diastolic"))
            except Exception as e:
                user.blood_pressure_diastolic = 0.0

            try:
                user.body_fat_percentage = float(request.POST.get("body_fat_percentage"))
            except Exception as e:
                user.body_fat_percentage = 0.0

        elif getUpdateStatus == "security":
            update = getUpdateStatus
            user.password = hashlib.sha256(str(request.POST['password']).encode('utf-8')).hexdigest()
        else:
            update = "match"

        user.save()

        if user.gender == 'M':
            male = "checked"
        else:
            female = "checked"

        if str(user.athlete) == "True":
            athlete = "checked"
        else:
            notAthlete = "checked"

        if str(user.heart_disease) == "True":
            heartDisease = "checked"
        else:
            notHeartDisease = "checked"

        if str(user.smoking) == "True":
            smoke = "checked"
        else:
            notSmoke = "checked"

        if str(user.medical_implant) == "True":
            medicalImplant = "checked"
        else:
            notMedicalImplant = "checked"

        request.session['username'] = user.username
        return render(request, 'profilePage.html', {'sub': sub, 'current_detail': user, 'update': update,
                                                'male': male, 'female': female,
                                                'athlete': athlete, 'notAthlete': notAthlete,
                                                'heartDisease': heartDisease, 'notHeartDisease': notHeartDisease,
                                                'smoke': smoke, 'notSmoke': notSmoke,
                                                'medicalImplant': medicalImplant, 'notMedicalImplant': notMedicalImplant,
                                                'user_email': user_email, 'attendence': attendence,
                                                'user_total': user_total, 'user': user})

    except Exception as e:
        print("\n\nexception = %s\n\n" % (e))
        pass

    return render(request, 'profilePage.html', {'sub': sub, 'email': user_email})


def friend(request):
    user_email = request.session['email']
    user = UserAccounts.objects.get(email=user_email)
    sub = "friend"
    ifSearch = ""
    friends = None
    if request.POST.get("friend"):
        ifSearch = "yes"
        friend_name = request.POST.get("friend")
        friends = UserAccounts.objects.filter(username__icontains = friend_name)
    my_friends = FriendsList.objects.filter(friend1 = user)
    return render(request, 'profilePage.html', {'sub': sub, 'friends': friends,
                                                'ifSearch': ifSearch, 'keyword': request.POST.get("friend"),
                                                'my_friends': my_friends})

def view_friend(request):
    friend_id = request.GET.get("id")
    friend = UserAccounts.objects.get(id = friend_id)
    user = UserAccounts.objects.get(email = request.session['email'])
    sub = "view_friend"
    ifFriend = "yes"

    if user.id == friend.id:
        ifFriend = "cannot"
    else:
        if not FriendsList.objects.filter(friend1_id = user.id, friend2_id = friend.id).exists():
            if request.POST.get("submit") == "add":
                insert = FriendsList(friend1 = user, friend2 = friend)
                insert.save()

                insert = FriendsList(friend1 = friend, friend2 = user)
                insert.save()
            else:
                ifFriend = "no"

    return render(request, 'profilePage.html', {'sub': sub, 'friend': friend, 'ifFriend': ifFriend, 'user':user})

def show_fitness_videos( request, category ):
    fitness = "videos"
    video_category = FitnessCategories.objects.get(name=category)
    video_category_id = video_category.id
    video_object_list = list ( FitnessVideo.objects.filter( category_id=video_category_id ) )

    # this_category_video_link_list = []
    # for video in video_object_list:
    #     this_category_video_link_list.append( video.link )

    return render( request, 'fitness.html', {'this_category_video_link_list' : video_object_list, 'page': fitness} )

def user_logout(request):
    request.session['signed_in'] = False
    return HttpResponseRedirect("/register/")

def like_video(request):
    # Check if user log in
    if 'signed_in' not in request.session or request.session['signed_in'] == False:
        return HttpResponse("not log in")

    user = UserAccounts.objects.get(email = request.session['email'])
    video = FitnessVideo.objects.get(id = request.GET['video_id'])

    # Check if user evaluate video before
    if VideosReview.objects.filter(user = user.id, video = video.id).exists():
        check = VideosReview.objects.get(user = user.id, video = video.id)
        if check.review == 1:
            return HttpResponse("evaluated")
        else:
            check.review = 1;
            check.save()
            update = FitnessVideo.objects.get(id = video.id)
            update.likes = video.likes + 1
            update.dislikes = video.dislikes - 1
            update.save()
    else:
        insert = VideosReview(user = user, video = video, target = user.training_target, review = 1)
        insert.save()
        update = FitnessVideo.objects.get(id = video.id)
        update.likes = video.likes + 1
        update.save()

    return HttpResponse(video.likes + 1)

def dislike_video(request):
    # Check if user log in
    if 'signed_in' not in request.session or request.session['signed_in'] == False:
        return HttpResponse("not log in")

    user = UserAccounts.objects.get(email = request.session['email'])
    video = FitnessVideo.objects.get(id = request.GET['video_id'])

    # Check if user evaluate video before
    if VideosReview.objects.filter(user = user.id, video = video.id).exists():
        check = VideosReview.objects.get(user = user.id, video = video.id)
        if check.review == 0:
            return HttpResponse("evaluated")
        else:
            check.review = 0;
            check.save()
            update = FitnessVideo.objects.get(id = video.id)
            update.dislikes = video.dislikes + 1
            update.likes = video.likes - 1
            update.save()
    else:
        insert = VideosReview(user = user, video = video, target = user.training_target, review = 0)
        insert.save()
        update = FitnessVideo.objects.get(id = video.id)
        update.dislikes = video.dislikes + 1
        update.save()

    return HttpResponse(video.dislikes + 1)

#@login_required
def homepage(request):
    msg_history = Chat.objects.all()
    return render(request, 'chat/base.html', {'messages': msg_history})

#@login_required
def get_new_messages(request):
    messages = Chat.objects.all()
    return JsonResponse({'messages': render_to_string('chat/messages.html', {'messages': messages, 'request_user_email':  request.session['email']})})


#@login_required
def save_new_msg(request):
    if request.is_ajax():
        msg = request.POST.get('new_msg', None)  # store new chat message
        user_1 = UserAccounts.objects.get(email=request.session['email'])
        chat = Chat(user=user_1, message=msg)
        chat.save()
    return HttpResponse('')  # just empty response in order to not cause an ajax error

#@login_required
def reset(request):
    Chat.objects.all().delete()
    print("MATCHHHHHHHHHHHHH")
    return HttpResponseRedirect('/homepage/')

def make_plan(request):
    sub = "plan"
    have_plan = "yes"
    videos = []
    user = UserAccounts.objects.get(email=request.session['email'])

    if 'cancel' in request.POST and request.POST['cancel'] is not None:
        user.training_target = None
        user.save()
    if 'category' in request.POST and request.POST['category'] is not None:
        category = "category"
        # print("\n\nusername = %s\n\n" % user.username)
        user.training_target = request.POST['category']
        user.save()
    elif user.training_target is None:
        have_plan = "no"
        return render(request, 'profilePage.html', locals())
    
    list_of_links = give_recommendation(user.email)
    for link in list_of_links:
        videos.append(FitnessVideo.objects.get(link = link))
    return render(request, 'profilePage.html', locals())

# Martin Ren 3/10/2016 END

# Cherry Zhao 14-09-2016 END
