#QWeb app
:sparkles: 0.0.0 This app was built over a weekend as a dev interview challenge :sparkles:

## Synopsis
  
  A web app for Q & A built on 
  - Python, Django
  - mySQL
  - AngularJS, MDL
  
## Design Principles
  The UI is designed with Material Design in mind. Each indepent feature/item is considered as a card.
  The cards are maintained as reusable angular templates maximizing DRY principle.
  
  Requests render a template which is contained by a wrapper and includes cards relevant to the requested page.
  The angular framework encapsulates each page's content. The frame is loaded first followed by request to populate each of the cards.
  
  Each card has it's own angular controller for the operations provided within it.
  
  Django's ORM is used for building data.
  Endpoints which return just plain data are kept seperate so that they can be moved out in  as an API app later.
    
## Pages
  All pages except home are responsive. 
  - /home/
    - login to the account    
  - /dashboard/
    - view trending items (in progress)
    - view your questions    
  - /ask/
    - ask a question
  - /question/
    - view a question
    - add answers
    - vote
  - /profile/
    - view user info
    - add favourite tags
  -/admin/ - Django amdin site  
 
## Features - Done
  - Q&A
    Add Questions and answers
  - Votes
    for questions and answers - upvote, downvote, undo upvote, undo downvote
  - Tags
    add tags to a question
    add tags to profile
    provision for accepting custom user tags
  - Security
    Auth, CSRF,ORM
 
## Features - Pending
   - vote on Dashboard
   - trending data based on activity and tags   - 
   - edit option for questions, answers and profile
   - trim question, like count font-size redux
   - preview/better editor (NicEdit)
   - Registration
    
## Installation
  - setup virtualenv Python 2.7
  - pip on the requirements.txt
  - add and configure settings.py
  - setupd mysql db, migrate data
  - configure wsgi or run local server
  
## Issues
   There might be bugs. The app was developed over a short time to solve an interview challenge.
   
## Notes
  I am a beginner with Django & Angular but it was fun building through experimentation. Now there's a solid foundation for the app to grow and for me to learn. Over the coming weekends I'll be pushing updates as I explore django more. 
  I realize now how easy it is to host a django app when compared to the dependency nightmares i've faced while setting up Catalyst.
  

## Tests
There are a few test accounts added through admin for testing. [u: alpha,beta,gamma,delta,omega , p:testpwd45 ]
All models required for testing and reqistered in admin site.
Debug is set to true




