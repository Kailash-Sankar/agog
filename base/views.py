from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from base.models import *
import logging
import json

#logger instance
logger = logging.getLogger(__name__)

def home(request):
	return render( request, 'base/home.html', {})

	  
def display_meta(request):
    values = request.META.items()
    values.sort()
    return render( request, 'base/utils/meta.html', { 'values' : values })

#---- auth -------

def user_login(request):
	error = "";	
	if request.META.get('REQUEST_METHOD') == 'POST':
		u = request.POST.get('username',"");
		p = request.POST.get('password',"");
		if u and p:		
			user = authenticate(username=u, password=p)
			if user is not None:
			    # the password verified for the user
			    if user.is_active:
			        #print("User is valid, active and authenticated")
			        login(request, user)
			        redirect('assign_training')
			    else:
			        error = "The password is valid, but the account has been disabled!"
			else:
			    # the authentication system was unable to verify the username and password
			    error = "The username and password were incorrect."
	else: 
		error = "Username & Password are mandatory."
	return render( request, 'base/home.html', { 'error' : error })			    


def user_logout(request):
    logout(request)
    # Redirect to a success page.


#---- pages ----

def dashboard(request):
	tf = '';
	return render( request, 'base/dashboard.html', { 'tf' : tf })
	
def ask(request):	
	return render( request, 'base/ask_question.html', {})
	
def question(request,qid):
	q = Question.objects.get(id=qid); #.values();
	print q;
	return render( request, 'base/view_question.html', { 'q' : q })


# ---- API endpoints -----
def tags(request,query):
	cat = Category.objects.filter(name__icontains=query).values('name','id')
	subcat = SubCategory.objects.filter(name__icontains=query).values('name','id')

	tags = list(cat) + list(subcat)
	return JsonResponse(tags,safe=False)

def trending(request,type):
	logger.debug('this is the type',type)
	if type == 'questions':
		trendingItems = list( Question.objects.values('summary','likes') )
		return JsonResponse(trendingItems,safe=False)
	elif type == 'answers':	
		trendingItems = [{ 'summary' : 'it works.' },{ 'summary' : 'why'}]
		return JsonResponse(trendingItems,safe=False)

def answers(request,qid,page):
	ansObj = Answer.objects.filter(question=qid);
	user = request.user

	ansList = {};
	for a in ansObj:
		row = {
			'aid' 			: a.id,
			'description' 	: a.description,
			'username' 		: a.user.username,
			'uid'			: a.user.id,
			'created_date' 	: a.created_date,
			'updated_date' 	: a.updated_date,
			'likes'			: ALike.objects.filter(answer=a.id).count(),			
		}

		#check if logged in user like this answer		
		try:
			print a.id,user.id
   			likeObj = ALike.objects.filter(answer=a.id,user=user.id).get()   			
   			mylike = likeObj.like
		except ALike.DoesNotExist:
   			mylike = None
   		except AttributeError:
   			myLike = None	
 		  			
 		row['mylike'] = mylike   		
		ansList[a.id] = row;

	print ansList	
	return JsonResponse(ansList,safe=False)

def like(request,aid):
	#json input
	data = json.loads(request.body)
	user = request.user

	#load answer 
	ansObj =  Answer.objects.get(id=aid)
	status = False;

	print data;
	bool_like = data['like']

	if ansObj and type(bool_like) == type(True):

		#update count in answer		
		if bool_like == True:		
			#upvote
			ansObj.likes = ansObj.likes + 1
		elif bool_like == False:
			#down vote
			ansObj.likes = ansObj.likes - 1
		else:
			#delete the vote
			ansObj.likes = ansObj.likes - 1

		#update/create like row		
		obj, created = ALike.objects.update_or_create(
			answer_id = aid,
			user_id = user.id,
			defaults = {
				'like' : bool_like
			}
		)

		if created:
			print 'row added';

		if obj:
			print 'row updated';

		#save incremented count	
		ansObj.save()
		status = True;
	
	return JsonResponse({ 'status' : status, 'aid' :aid })