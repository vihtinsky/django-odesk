from django.conf.urls.defaults import *
from django_odesk.auth.views import AuthenticateView, CallBackView

urlpatterns = patterns('django_odesk.auth.views',
    url(r'^authenticate/$', AuthenticateView.as_view()),
    url(r'^callback/$', CallBackView.as_view()),
)
