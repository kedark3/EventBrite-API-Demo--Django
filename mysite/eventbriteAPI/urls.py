from django.conf.urls import url
from eventbriteAPI import views


urlpatterns = [
    url(r'^events/', views.events,name='event_list'),       #URL for events list page
    url(r'^events-by-cat/', views.events_by_cat,name='events_by_cat'), #URL for iframes
    url(r'^$',views.home,name='home'), #URL for home page

]
