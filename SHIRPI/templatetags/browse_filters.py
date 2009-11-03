from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_restaurant_set(set, category, autoescape=None):
	#start table
	result = "<table class=\"" + category + " restaurant_set\">"
	result += "\n\t<caption>" + category.capitalize() + "</caption>"
	result += "\n\t" + display_restaurant_table_header(set)
	#display info for each restaurant in the set
	for rest in set:
		result += "\n\t" + display_restaurant_info(rest)
	#end table and return resulting table
	result += "\n\t</table>\n"
	return mark_safe(result)
display_restaurant_set.needs_autoescape = True
display_restaurant_set.needs_category = True

#display the info of one restaurant
@register.filter
def display_restaurant_info(value, autoescape=None):
	if value.cleanliness_count<1:
		value.cleanliness_count=1
	if value.combined_count<1:
		value.combined_count = 1
	if value.food_quality_count<1:
		value.food_quality_count=1
	if value.atmosphere_count<1:
		value.atmosphere_count = 1
	if value.wait_time_count<1:
		value.wait_time_count =1 
	result = '<tr>\n\t<td><a href="/cs215/SHIRPI/browse/' + value.name +'/' + value.address + '">' + value.name + '</a></td>'
	result += '<td>' + str(value.address) + '</td><td>' + str(value.health_report_status) +'</td>'
	result += '<td>' + str(value.combined/value.combined_count) + '</td><td>' + str(value.food_quality/value.food_quality_count) + '</td>'
	result += '<td>' + str(value.cleanliness/value.cleanliness_count) + '</td><td>' + str(value.atmosphere/value.atmosphere_count) + '</td><td>' + str(value.wait_time/value.wait_time_count) + '</td>'
	result += '\n</tr>\n'
	return mark_safe(result)
display_restaurant_info.needs_autoescape = True

#display a group of comments in a table
@register.filter
def display_comment_set(set, user_name, autoescape=None):
	#start the table
	result = '<table class=\"comment_set\">\n'
	result += "<caption>Comments</caption>"
	result += display_comment_table_header(set, user_name)
	#put the information for each comment into the table
	for comment in set:
		result += display_comment(comment, user_name)
	#end the table and return it
	result += '</table>'
	return mark_safe(result)
display_comment_set.needs_autoescape=True
display_comment_set.needs_user_name = True

#display one comment
@register.filter
def display_comment(value, user_name,autoescape=None):
	result = '<tr>'
	result += '<td>'
	#if it an anonymous user, don't allow them to view their profile
	if value.author.username!="Anonymous":
	        result += '<a href="/cs215/SHIRPI/view_profile/' + value.author.username+ '">'
	
	result += value.author.username
	if value.author.username!="Anonymous":
		result += '</a>'
	result += '</td>'
 	result += '<td>'

	if user_name == value.author.username:
		result += '<a href="/cs215/SHIRPI/edit_comment/' + str(value.pk) + '">' + value.comment + '</a>'
	else:
		result += value.comment
	result += '<td>'+ str(value.combined)+'</td>'
 	result += '<td>'+ str(value.food_quality) +'</td>'
 	result += '<td>'+ str(value.cleanliness) +'</td>'
 	result += '<td>'+ str(value.atmosphere)+'</td>'
 	result += '<td>'+ str(value.wait_time) +'</td>'
 	result += '</tr>'
	return mark_safe(result)
display_comment.needs_autoescape = True
display_comment.needs_user_name = True

#display restaurant title row
@register.filter
def display_restaurant_table_header(value, autoescape=None):
	result =  '<tr><th>Name</th><th width="200px">Address</th><th>HI Status</th><th>Combined</th><th>Food Quality</th><th>Cleanliness</th><th>Atmosphere</th><th>Wait Time</th></tr>'
	return mark_safe(result)
display_restaurant_table_header.needs_autoescape = True

#display comment title row
@register.filter
def display_comment_table_header(value, autoescape=None):
	result = ' <tr><th>Author</th><th width="300px">Comment</th><th>Combined</th><th>Food Quality</th><th>Cleanliness</th><th>Atmosphere</th><th>Wait Time</th></tr>'
	return mark_safe(result)
display_comment_table_header.needs_autoescape = True

