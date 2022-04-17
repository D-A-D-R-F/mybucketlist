from django.shortcuts import render , HttpResponseRedirect , redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from httplib2 import Http
from .models import User , Bucket_List , Connect_Users , Shared_Items
import random
import datetime
import os
import googleapiclient.discovery

def index(request):
    return render(request , "different/index.html")

@login_required
def random_activities(request):
    return render(request , "different/random.html")

@login_required
def completed(request , item):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('random_events'))
    else:
        current_status = Bucket_List.objects.filter(username = request.user.username , item = item).first()
        if current_status.status == 'pending':
            current_status.status = 'completed'
            current_status.save()

        return HttpResponseRedirect(reverse('bucket_list'))
        


@login_required
def bucket_list(request):
    if request.method == 'POST':
        bucket_task = request.POST['bucket_list_input']
        category = request.POST['category']
        duration_value = request.POST['duration']
        duration_unit = request.POST['time-unit']
        location = request.POST['location-input']

        if duration_unit == 'HOURS':
            duration = round(int(duration_value) / 24 , 3)
        elif duration_unit == 'DAYS':
            duration = duration_value
        elif duration_unit == 'MONTHS':
            duration = int(duration_value) * 30.436875

        buckets = Bucket_List.objects.filter(username = request.user.username).all()
        current_id = len(buckets) + 1


        username = request.user.username
        add_bucket = Bucket_List(bucket_id = current_id ,username=username , item = bucket_task , category = category , duration = duration , location = location , status = 'pending')
        add_bucket.save()
        return HttpResponseRedirect(reverse('bucket_list'))
    else:
        categories = ['Travel' , 'Relationships' , 'Career' , 'Financial' , 'Entertainment' , 'Adventure' , 'Contribution' , 'Creativity' , 'Education' , 'Health']

        pending_buckets = Bucket_List.objects.filter(username = request.user.username , status = 'pending').all()
        completed_buckets = Bucket_List.objects.filter(username = request.user.username , status = 'completed').all()
        return render(request , 'different/bucket_list.html' , {
            'categories':categories , 
            'buckets':pending_buckets , 
            'completed_items':completed_buckets

        })

@login_required
def error(request , message):
    return render(request , "different/error.html" , {
        'message':message
    })

@login_required
def random_events(request):
    date = datetime.datetime.now().day
    month = datetime.datetime.now().month
    months_days = {
        1:31 , 
        2:28 , 
        3:31 , 
        4:30 , 
        5:31 , 
        6:30 , 
        7:31 , 
        8:31 , 
        9:30 , 
        10:31 , 
        11:30 ,
        12:31 
    }

    month_names = {
        1:'January' , 
        2:'February' , 
        3:'March' , 
        4:'April' , 
        5:'May' , 
        6:'June' , 
        7:'July' , 
        8:'August' , 
        9:'September' , 
        10:'October' , 
        11:'November' ,
        12:'December' 
    }
    days_in_month = months_days[month]
    number = random.randint(int(date) , days_in_month)

    current_month = month_names[month]

    all_bucket_list_events = Bucket_List.objects.filter(username = request.user.username , status='pending').all()
    if len(all_bucket_list_events) == 0:
        message = 'Looks like you don\'t have any pending tasks on your bucket list! Click \'My Bucket\' above to create some new ones!'
        return HttpResponseRedirect(reverse('error' , kwargs ={'message': message}))

    all_events = []
    for event in all_bucket_list_events:
        all_events.append(event.item)
    
    random_no = random.randint(0 , len(all_events) - 1)

    random_event = all_events[random_no]


    
    api = os.environ.get('yt-api-bucket-list')
    youtube_object = googleapiclient.discovery.build("youtube" , "v3" , developerKey=api)
    request_api = youtube_object.search().list(
                    part="snippet",
                    maxResults = 5,
                    q = random_event , 
                    type = 'video'
                    
    )
    response = request_api.execute()

    links_urls = []
    for i in range(0 , 5):
        vid_id = response['items'][i]['id']['videoId']
        links_urls.append(vid_id)
    


    formatted_random_event = random_event.replace(' ' , '+')
    place_of_event = Bucket_List.objects.filter(username = request.user.username , item = random_event).first().location
    formatted_place = place_of_event.replace(' ' , '+')
    location_of_event = formatted_random_event  + '+' + 'in' + '+' + formatted_place


    return render(request , 'different/event_calendar.html' , {
        'random_date':number , 
        'month_name':current_month , 
        'random_event':random_event ,
        'links':links_urls , 
        'api_key':os.environ.get('maps-api') , 
        'formatted_random' : formatted_random_event , 
        'location':location_of_event

    })




@login_required
def connect(request):
    if request.method == 'POST':
        location = request.POST['location']
        email = request.POST['email']

        if email == '':
            contact = 'No number provided.'
        else:
            contact = email

        check_presence = Connect_Users.objects.filter(username = request.user.username).first()
        if check_presence:
            check_presence.location = location
            check_presence.email = contact
            check_presence.save()
            return HttpResponseRedirect(reverse("connect"))

        else: 
            add = Connect_Users(username = request.user.username , location = location , email = email)
            add.save()

            return HttpResponseRedirect(reverse("connect"))

    else:
        checker = Connect_Users.objects.filter(username = request.user.username).first()
        if checker:
            user_location = Connect_Users.objects.filter(username = request.user.username).first().location
            query = Connect_Users.objects.filter(location = user_location).all()
            if len(query) == 1:
                messag_e = 'Looks like there aren\'t any users in your region , sorry!'

                return render(request , 'different/connect.html' , {
                'common':query,
                'message':messag_e

            })
            else:
                return render(request , 'different/connect.html' , {
                'common':query,
            })
        else:
            return render(request , 'different/connect.html')


@login_required
def share_completed(request):
    if request.method == 'POST':
        item_completed = request.POST['item-completed']
        user_comment = request.POST['user-comment']
        username = request.user.username

        insert = Shared_Items(username= username , comment = user_comment , completed_item = item_completed)
        insert.save()
        return HttpResponseRedirect(reverse("share"))
    else:

        items = Bucket_List.objects.filter(username = request.user.username , status = "completed").all()
        user_shared_items = Shared_Items.objects.filter(username = request.user.username).all()
        all_shared_items = Shared_Items.objects.all()
        return render(request , "different/achievements.html" , {
            'items':items , 
            'shared_items':user_shared_items , 
            'all_shared':all_shared_items
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "different/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "different/login.html")

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "different/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "different/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "different/register.html")