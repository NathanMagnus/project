# Create your views here.
from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from hello.models import *
from django.views.generic.simple import direct_to_template
from django import forms
from django.http import HttpResponseRedirect

CRIT_VAL = 3#Category.get(category="Critical")
MOD_VAL = 1#Category.get(category="Moderate")
GOOD_VAL = 0#Category.get(category="Good")

def save(request, rest_name):
	try:
		review = Review()
		review.combined = request.POST['overall']
		review.restaurant = Restaurant.objects.get(name=rest_name)
		review.review = "Good place to eat"
		review.cleanliness = 10
		review.food_quality = 10
		review.atmosphere = 11
		review.wait_time = 0
		review.save()
		
	except Restaurant.DoesNotExist:
		return HttpResposneRedirect('/cs215/hello/index.html')
	return HttpResponseRedirect('/cs215/hello/browse/'+rest_name+'/')

def index(request):
	return render_to_response('hello/index.html')

def review(request, rest_name):
	form = ReviewForm(request.POST)
	rest = Restaurant.objects.get(name=rest_name)
	return render_to_response('hello/review.html', {'rest':rest, 'form': form})

def login(request):
	login_template = 'registration/login.html'
	form = LoginForm(request.POST)
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		djlogin(request, user)
	return render_to_response(login_template, {'error': "Login failed", 'next': '/cs215/hello/'})

def logout(request):
	form = LoginForm(request.POST)
	djlogout(request)
	return direct_to_template(request, 'hello/index.html')

def browse(request, rest_name):
	try:
		rest = Restaurant.objects.get(name=rest_name)
		reviews = Review.objects.filter(restaurant = rest)
		return render_to_response('hello/browse.html', {'rest': rest, 'reviews': reviews})
	except Restaurant.DoesNotExist:
		if rest_name == "All":
			crit = Restaurant.objects.filter(health_inspection_status__gte=CRIT_VAL)
			mod = Restaurant.objects.filter(health_inspection_status__gte=MOD_VAL).filter(health_inspection_status__lt=CRIT_VAL)
			good = Restaurant.objects.filter(health_inspection_status__lte=GOOD_VAL)
			return render_to_response('hello/browse.html', {'categories': {'Critical': crit, 'Moderate': mod, 'Good':good}})
		else:
			return render_to_response('hello/browse.html', {'error': "Restaurant does not exist."})

def register(request):
	rform = RegistrationForm(request.POST)
	return render_to_response('hello/register.html', {'rform': rform, 'form': form})
