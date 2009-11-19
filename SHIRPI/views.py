# Create your views here.
import urllib
from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm, ProfileForm
from project.SHIRPI.settings import *

from datetime import datetime
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

#main page
def index(request):
	#get critical, moderate and good reports
	Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by('-health_report_status', '-combined').all()[:10]
	Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by('-health_report_status', '-combined').all()[:10]
	Good = Restaurant.objects.filter(health_report_status__lte=GOOD_VAL).order_by('-health_report_status', '-combined').all()[:10]
	#render the index page
	return render_to_response("SHIRPI/index.html", {'Critical':Critical, 'Moderate':Moderate,'Good':Good}, RequestContext(request))

#browsing restaurants
def browse(request, restaurant_name = None, restaurant_address = None, api_flag = None):
	# Prepare strings for database query
	if restaurant_name == None:
		restaurant_name = ""
	if restaurant_address == None:
		restaurant_address = ""
		
	restaurant_name = urllib.unquote_plus(restaurant_name).lower()
	restaurant_address = urllib.unquote_plus(restaurant_address).lower()
	
	if restaurant_name == "all":
		restaurant_name = ""
	if restaurant_address == "all":
		restaurant_address = ""
	
	# here so that user can search for all good restaurants on albert street
	# or all mcdonalds that are good, etc
	
	# Consider modifying the above to something similar to:
	lower_limit = request.GET.get('lower_limit')
	upper_limit = request.GET.get('upper_limit')
	
	if upper_limit == "critical":
		range_high = 9999
		
		if lower_limit == "moderate":
			range_low = MODERATE_VAL
		elif lower_limit == "good":
			range_low = GOOD_VAL
		else:
			range_low = CRITICAL_VAL
	
	elif upper_limit == "moderate":
		range_high = CRITICAL_VAL
		
		if lower_limit == "good":
			range_low = GOOD_VAL
		else:
			range_low = MODERATE_VAL
	
	elif upper_limit == "good":
		range_high = GOOD_VAL+1
		range_low = GOOD_VAL
	

	# Query Database
	# ACTUAL RANGE EXCLUSION SHOULD BE DONE AS PART OF THIS TO IMPROVE UPON PERFORAMNCE

	try:
		if lower_limit == None and upper_limit==None:
			results = Restaurant.objects.filter(name__icontains=restaurant_name, address__icontains=restaurant_address)
		else:
			if upper_limit == None:
				range_high = 99999
			if lower_limit == None:
				range_low = -1
			results = results.filter(health_report_status__gte=range_low, health_report_status__lt=range_high)
	except Restaurant.DoesNotExist:
		error = "No results."
	
	# Browse Page Display
	if api_flag == None:
		if len(results) == 1:
			restaurant = results[0]
			#get the reports
			reps = HealthReport.objects.filter(restaurant=restaurant)
			#get the comments
			comments = Comment.objects.filter(restaurant=restaurant)[0:5]
			#render the page
			context =  {'restaurant': restaurant, 'reps':reps, 'comments': comments}
			return render_to_response("SHIRPI/view_restaurant.html", context, RequestContext(request))
		elif len(results) == 0:
			return render_to_response("SHIRPI/error.html", {'error':"No matches found"}, RequestContext(request))
		else:
			return render_to_response("SHIRPI/browse.html", {'restaurants': results}, RequestContext(request))
	
	# API Display
	else:
		display_type = request.GET.get('display')
		MySpecialApiData = []
		for location in results:	# disgusting loop solves problems
			if display_type == "full":
				report_results = HealthReport.objects.filter(restaurant=location)
			else:
				report_results = None
			MySpecialApiData.append({ 'location': location, 'reports': report_results })
		
		context = { 'results': MySpecialApiData, 'display_type': display_type }
		return render_to_response("SHIRPI/api.xml", context, RequestContext(request),  mimetype='application/xml')

def view_restaurant(request, restaurant_name, restaurant_address):
	try:
		restaurant = Restaurant.objects.get(name__iexact=urllib.unquote_plus(restaurant_name), address__iexact=urllib.unquote_plus(restaurant_address))
		reports = HealthReport.objects.filter(restaurant=restaurant)
		comments = Comment.objects.filter(restaurant=restaurant)
		context = {'restaurant': restaurant, 'reports': reports, 'comments': comments}
		return render_to_response("SHIRPI/view_restaurant.html", context, RequestContext(request))
	except Restaurant.DoesNotExist:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

def view_profile(request, user_name):
	user_name = urllib.unquote_plus(user_name)
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/error.html', {'error': "No user with username '" + user_name +"'"}, RequestContext(request))
	favourites = Favourite.objects.filter(user=user_to_view).order_by('rank')
	comments = Comment.objects.filter(author=user_to_view)
	context = {'user_to_view': user_to_view, 'favourites': favourites, 'comments': comments}
	return render_to_response('SHIRPI/view_profile.html', context, RequestContext(request))	

def edit_profile(request):
	user = request.user
#	if user.is_authenticated():
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['new_password'] != form.cleaned_data['password_again']:
				return render_to_response('SHIRPI/edit_profile.html', {'message': "New passwords do not match"}, RequestContext(request))
			if not user.check_password(form.cleaned_data['old_password'])
				return render_to_response('SHIRPI/edit_profile.html', {'message': "Incorrect password"}, RequestContext(request))
			user.email = form.cleaned_data['email']
			user.set_password(form.cleaned_data['new_password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			return render_to_response('SHIRPI/edit_profile.html', {'form': form, 'message': "Changes completed"}, RequestContext(request))
	else:
		form = ProfileForm(initial={'email': request.user.email})
		return render_to_response('SHIRPI/edit_profile.html', {'form': form}, RequestContext(request))
	return render_to_response('SHIRPI/error.html', {'error':"You are not logged in"}, RequestContext(request)) 
