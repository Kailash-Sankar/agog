Qweb app

## Synopsis
  http://felhound16.pythonanywhere.com/
  A web app for Q & A built on 
  - Python, Django
  - mySQL
  - AngularJS, MDL
  
## Design Principles
  The UI is designed with Material Design priciples. Each indepent feature/item is considered as a card.
  The cards are maintained as reusuable angular templates maximizing DRY principle
  
  Reuqests render a template which is enacapsulated by a wrapper and includes cards releavant to the request page.
  The angular framework encapsulates each page's content. The frame is laoded first followed by request to populate each of the card.
  
  Django's ORM is used for building data.
  Endpoints which return just plain data are kept seperate so that they can be moved out in future as an API app

## Pages
  All pages except home are responsive. 
  - /home/
    - login to the account    
  - /dashboard/
    - view trending items (in progress)
    - view your questions
    - voting is not enabled in this page
  - /ask/
    - ask a question
  - /question/
    - view a question
    - add answers
    - upvote, downvote, cancel vote
  - /profile/
    - view user info
    - add favourite tags

## Installation
  - setup virtualenv 2.7
  - pip on the requirements.txt
  - add and configure settings.py
  - setupd mysql db, migrate data
  - configure wsgi or run local server
  
## API Reference
  TODO

## Tests
There are a few test accounts added through admin for testing.




