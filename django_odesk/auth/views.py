from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django_odesk.core.clients import DefaultClient
from django_odesk.auth import ODESK_REDIRECT_SESSION_KEY, \
                              ODESK_TOKEN_SESSION_KEY
from django.views.generic.base import RedirectView


class AuthenticateView(RedirectView):
    
    def get_redirect_url(self):
        redirect_to = self.request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        self.request.session[ODESK_REDIRECT_SESSION_KEY] = redirect_to
        odesk_client = DefaultClient()
        return odesk_client.auth.auth_url()


class CallBackView(RedirectView):
    redirect_url = None
    
    def get_redirect_url(self):
        odesk_client = DefaultClient()
        frob = self.request.GET.get('frob', None)
        if frob:
            token, auth_user = odesk_client.auth.get_token(frob)
            self.request.session[ODESK_TOKEN_SESSION_KEY] = token
            #TODO: Get rid of (conceptually correct) additional request to odesk.com
            user = django_authenticate(token = token)
            if user:
                login(self.request, user)
            else:
                pass 
                #Probably the odesk auth backend is missing. Should we raise an error?
            self.redirect_url = self.request.session.pop(ODESK_REDIRECT_SESSION_KEY, 
                                               self.redirect_url)
            if not self.redirect_url:
                self.redirect_url =  '/'   
            return self.redirect_url
        
        else:
            return odesk_client.auth.auth_url()
        
