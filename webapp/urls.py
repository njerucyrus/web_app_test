from django.conf.urls import url
from webapp import views

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^apply/$', views.ScholarshipApplicationView.as_view(), name='apply'),
    ]
