'''
*Author : Kedar Vijay Kulkarni
*Website: http://KedarKulkarni.in
*GitHub : http://github.com/kedark3
*Please refer GitHub Repository for more django projects done by me
*HealthApp, SMSPoll, Template-Designer, CLRMS are all Django code repositories
'''


from django.http import HttpResponse
from django.template import loader
from eventbriteAPI.forms import SimpleForm
import urllib.request
from json import loads

'''This class is used to create objects of events to hold the URL and Name of event
These objects are then passes in context to template iframe.html '''

class event_class(object):
    def __init__(self,event_name,event_url):
        self.event_name=event_name
        self.event_url=event_url



#Auth token that could be changed whenever required

token='NXLCZBPL2MEMGQIV57UF' #created own token, apart from one specified in email


#This view will be used to load all the categories in the select box
def home(request):


    # Access list from the API
    with urllib.request.urlopen('https://www.eventbriteapi.com/v3/categories/?token=%s' %token) as f:
        #loading data recieved from urlopen to JSON format in info variable
        categories = loads(f.read().decode('utf-8'))

    #This is a tuple that will be used to create a django form
    FAVORITE_EVENT_CHOICES=()

    '''For every category in JSON variable categories, we add its id and name in the tuple
    i.e. in FAVORITE_EVENT_CHOICES'''
    for category in categories['categories']:
        FAVORITE_EVENT_CHOICES=((category['id'],category['name']),)+FAVORITE_EVENT_CHOICES


    '''We have imported SimpleForm from forms.py and we pass it the tuple containing
    list of all the event categories.'''

    form= SimpleForm(reversed(FAVORITE_EVENT_CHOICES))
    template = loader.get_template('eventbriteAPI/index.html')
    context = {
        'form':form,
    }
    return HttpResponse(template.render(context, request))
#=======================================End of View - home==========================================================


def events(request):
    #Here we retrieve all the event categories chosen by the user, user may choose 1,2 or 3 categories at the max
    event_category_id_list=request.GET.getlist('favorite_event_categories')

    '''
    Here we have used try except blocks to retrieve the categories one by one in variables
    cat_events1, cat_events2, cat_events3- it denotes category of events
    to make sure that program does not crash even if there are no categories in url
    '''
    try:
        cat_events1=event_category_id_list[0]
    except Exception:
        cat_events1=0


    try:
        cat_events2=event_category_id_list[1]
    except Exception:
        cat_events2=0

    try:
        cat_events3=event_category_id_list[2]
    except Exception:
        cat_events3=0

    '''We have sent page number to be 0 from home page by default, but to handle test cases
    where for any unforeseen reason page number is not retrived, we use try except block.'''
    try:
        page=request.GET['page']
    except Exception:
        page=0

    template = loader.get_template('eventbriteAPI/result.html')

    '''This context sends the ready urls to iFrame tags on result page and then
    iFrame use these urls as source and calls respective views'''

    context = {

        'events1':'/events-by-cat/?categories={}&token={}&page={}'
    .format(cat_events1,token,page),
        'events2':'/events-by-cat/?categories={}&token={}&page={}'
    .format(cat_events2,token,page),
        'events3':'/events-by-cat/?categories={}&token={}&page={}'
    .format(cat_events3,token,page),
    }
    return HttpResponse(template.render(context, request))



#=======================================End of View - events==========================================================


def events_by_cat(request):
    '''
    This view in particular makes calls to search API of EventBrite and retrieves the list of events
    that are based on user's choice of categories and it also appends page number in url, keeping in minde pagination
    We make sure to use exception handling in case of invalid input
    '''
    try:
        response=urllib.request.urlopen('https://www.eventbriteapi.com/v3/events/search/?categories={}&token={}&page={}'
                .format(request.GET['categories'],token,request.GET['page']))
    except Exception as e:
        return HttpResponse(str(e))

    #If no exception occurs, we read reponse and put it in events_list in json format
    with response as f:
        event_list = loads(f.read().decode('utf-8'))
    events_in_cat=[]

    '''These variables are used to send in context of iframecontent.html template in anchor tag
    to help generate url for particular pages of the event list'''

    page_count=event_list["pagination"]["page_count"] #gets total page count from JSON data
    page_number=event_list["pagination"]["page_number"] #gets current page count from JSON data


    for event in event_list["events"]:
        events_in_cat.append(event_class(event['name']['text'],event['url']))


    #if page number is equal to total number of pages, we go back to page 0
    if page_number==page_count:
        next_page_number=1
    else:
    #else we add 1 to page number
        next_page_number=page_number+1

    template = loader.get_template('eventbriteAPI/ifamecontent.html')
    context = {
        'events':events_in_cat,
        'page_number':page_number,
        'page_count':page_count,
        'previous':request.get_full_path().split('page')[0]+'page='+str(page_number-1),
        'next':request.get_full_path().split('page')[0]+'page='+str(next_page_number),
    }

    return HttpResponse(template.render(context, request))
#=======================================End of View - events_by_cat==========================================================

#=======================================End of Views.py======================================================================

