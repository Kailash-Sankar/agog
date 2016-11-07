from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from base.models import *
import logging
import json
from django.db.models import F
from django.db.models import Count

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
	
def view_question(request,qid):
	user = request.user;
	return render( request, 'base/view_question.html', { 'qid' : qid })

def profile(request):
	return render( request, 'base/user_profile.html')	

# ---- API endpoints -----

def question(request,qid):
	print 'question:',qid

	qObj = Question.objects.get(id=qid);
	user = request.user;

	q = {
		'qid'			: qObj.id,
		'summary' 		: qObj.summary,
		'description' 	: qObj.description,
		'user' 			: qObj.user.username,
		'created_date' 	: qObj.created_date,
		'updated_date' 	: qObj.updated_date,
		'likes'			: qObj.likes,
		'myQ'		    : False,
		'myLike'		: False,
	}

	#check if logged in user liked this answer		
	try:
   		likeObj = QLike.objects.filter(question=qid,user=user.id).get()   			
   		mylike = likeObj.like
	except QLike.DoesNotExist:
   		mylike = None
   	except AttributeError:
   		myLike = None	
 	  			
 	q['mylike'] = mylike   		
	
	#check if it's logged in user's question	
 	if qObj.user.id == user.id:
		q['myQ'] = True

	#get question tags
	q['tags'] = QTags(qid)

	print q;
	return JsonResponse(q,safe=False);


def tags(request,query):
	print query
	cat = Category.objects.filter(name__icontains=query).annotate(cid=F('id')).values('name','cid')	
	
	tags = list(cat); 
	print tags;
	return JsonResponse(tags,safe=False)

def trending(request,type):
	user = request.user

	trendingItems = [];

	logger.debug('this is the type',type)
	if type == 'questions':
		trendingItems = list( Question.objects.all()[:5].values('summary','likes','id') )
		
	elif type == 'answers':	
		trendingItems = [{ 'summary' : 'it works.' },{ 'summary' : 'why'}]
		RecentlyAnsweredQuestions()
		
	elif type == 'my':
		trendingItems = list( 
			Question.objects.filter(user_id=user.id).order_by('-id')[:5].values() 
		)

	return JsonResponse(trendingItems,safe=False)	

def answers(request,qid,page):
	ansObj = Answer.objects.filter(question=qid);
	user = request.user

	ansList = {};
	for a in ansObj:
		row = buildAnswerRow(a,user);
		ansList[a.id] = row;
		
	return JsonResponse(ansList,safe=False)


def alike(request,aid):
	#json input
	data = json.loads(request.body)
	user = request.user

	#load answer 
	ansObj =  Answer.objects.get(id=aid)
	
	#hadle dem likes
	res = likeThis(ansObj,data,user)
	return JsonResponse(res)

def qlike(request,qid):
	data = json.loads(request.body)
	user = request.user

	#load Question
	qObj =  Question.objects.get(id=qid)	

	res = likeThis(qObj,data,user)
	return JsonResponse(res)

def saveQuestion(request):
	data = json.loads(request.body)
	user = request.user

	qObj = Question(
		summary=data['summary'],
		description=data['description'],
		user_id = user.id,
		likes=0
	);
	qObj.save();

	for tag in data['tags']:
		if tag['id']:
			tObj = QTag(cat_id=tag['id'],question_id=qObj.id)
			tObj.save()
		else:
			print 'custom tags',tag['name']

	return JsonResponse({ 'qid' :qObj.id }) 		
	

def saveAnswer(request,qid):
	data = json.loads(request.body)
	user = request.user

	aObj = Answer(		
		description=data['description'],
		user_id = user.id,
		likes=0,
		question_id=qid,
	);
	aObj.save();

	aRow = buildAnswerRow(aObj,user);

	return JsonResponse(aRow) 		
	

def me(request):
	user = request.user

	profile = { 
		'username' : user.username,
		'first_name' : user.first_name,
		'last_name' : user.last_name,
		'about' : 'lorem ipsum',
	}
	profile['tags'] = UTags(user.id);

	return JsonResponse(profile,safe=False)

def userTags(request):
	user = request.user
	tags = UTags(user.id)

	return JsonResponse(tags,safe=False)

def saveUserTags(request):
	tags = json.loads(request.body)
	user = request.user
	xtags = list( UTag.objects.filter(user_id=user.id).select_related('cat').annotate(cid=F('cat__id')).values_list('cid',flat=True) )

	print 'tags',tags
	print 'xtags',xtags

	#create new tag-map if it doesn't exist in db
	vtags = [];
	for tag in tags:
		if tag['cid']:
			tObj, created = UTag.objects.get_or_create(cat_id=tag['cid'],user_id=user.id)			
			vtags.append(tag['cid'])
		else:
			print 'custom tags',tag['name']

	#delete remaining tags		
	for x in xtags:
		if x not in vtags:
			print 'deleting',x
			delObj = UTag.objects.filter(cat_id=x,user_id=user.id)
			delObj.delete()	

	#get all user tags		
	all_tags = UTags(user.id)		

	return JsonResponse(all_tags,safe=False) 	


# ---------- local routines -----------

def RecentlyAnsweredQuestions():
	#list( Question.objects.all()[:5].values('summary','likes','id') )
	x = Question.objects.annotate(noa=Count('answer')).order_by('-noa')[:5]	.values()
	print 'QA',x;



#build row for one answer
def buildAnswerRow(a,user):
	row = {
		'aid' 			: a.id,
		'description' 	: a.description,
		'username' 		: a.user.username,
		'uid'			: a.user.id,
		'created_date' 	: a.created_date,
		'updated_date' 	: a.updated_date,
		'likes'			: a.likes,
		'myAns'			: False,			
	}

	#check if logged in user liked this answer		
	try:
   		likeObj = ALike.objects.filter(answer=a.id,user=user.id).get()   			
   		mylike = likeObj.like
	except ALike.DoesNotExist:
   		mylike = None
   	except AttributeError:
   		myLike = None	
 	  			
 	row['mylike'] = mylike   		
		
 	#check if the logged in user added this answer 	
	if user.id == a.user.id:
		row['myAns'] = True;

	return row

#Return tags associated with a question	
def QTags(qid):
	cat = QTag.objects.filter(question_id=qid).select_related('cat').annotate(cid=F('cat__id'),name=F('cat__name')).values('cid','name')	
	tags = list(cat); 
	return tags;

#Return tags associated with a user	
def UTags(uid):
	cat = UTag.objects.filter(user_id=uid).select_related('cat').annotate(cid=F('cat__id'),name=F('cat__name')).values('cid','name')	
	print cat;
	tags = list(cat); 
	return tags;

#changes the like value for a question or an answer
def likeThis(Obj,data,user):
	
	status = False;
	bool_like = data['like']

	print data
	print Obj

	if Obj:
		print 'before',Obj.likes
		#update count in answer		
		if bool_like == True:		
			#upvote
			Obj.likes = F('likes') + 1
		elif bool_like == False:
			#down vote
			Obj.likes = F('likes') - 1
		else: 
			print 'code should come here'
			#bool_like is None
			#delete the vote
			if data['myLike'] == True:
				Obj.likes = F('likes') - 1
			elif data['myLike'] == False: 	
				Obj.likes = F('likes') + 1

		if isinstance(Obj, Answer):
			#update/create like row		
			newObj, created = ALike.objects.update_or_create(
				answer_id = Obj.id,
				user_id = user.id,
				defaults = {
					'like' : bool_like
				}
			)
		elif isinstance(Obj, Question):	
			#update/create like row		
			newObj, created = QLike.objects.update_or_create(
				question_id = Obj.id,
				user_id = user.id,
				defaults = {
					'like' : bool_like
				}
			)

		if created:
			print 'row added'
		if newObj:
			print 'row updated'

		#save incremented count	
		Obj.save()
		print 'after',Obj.likes
		status = True
	
	return { 'status' : status, 'id' : Obj.id }

	