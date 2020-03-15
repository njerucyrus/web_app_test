from django.conf.urls import url
from webapp import views

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^password/$', views.change_password, name='change_password'),

    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    url(r'^apply/$', views.ScholarshipApplicationView.as_view(), name='apply'),
    url(r'^staff-area/$', views.AdminDashboard.as_view(), name='admin'),
    url(r'^applications/$', views.ListAllApplicationView.as_view(), name='applications'),
    url(r'^manage-applications/$', views.ManageApplicationView.as_view(), name='manage_applications'),
    url(r'^approved-applications/$', views.ApprovedApplications.as_view(), name='approved_applications'),
    ]
