from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import RedirectView, TemplateView

from webapp.forms import ScholarshipApplicationForm
from webapp.models import ScholarshipApplication


class RegisterView(View):
    template_name = 'website/pages/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'request': request})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check if account exists
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.error(request,
                           f'You already have an existing account with username {username}.Login instead')
            return render(request, template_name=self.template_name, context={'request': request})
        else:
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                username=username,
                email=request.POST['email']
            )
            user.set_password(password)
            user.save()
            login(request, user)
            redirect_route = '/'
            messages.success(request, 'Account created successfully. Login to proceed')
            return HttpResponseRedirect(redirect_to=redirect_route)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


class LoginView(View):
    template_name = 'website/pages/login.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '').strip()
        user = request.user
        if user.is_authenticated and next_url != '':

            return HttpResponseRedirect(next_url)
        elif user.is_authenticated and next_url != '':

            return HttpResponseRedirect('/')
        else:
            return render(request, template_name=self.template_name, context={'request': request})

    def post(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '').strip()
        data = request.POST
        user = authenticate(request=request, username=data.get('username'),
                            password=data.get('password'))
        if user is not None:
            if user.is_active:
                request.session['phone_number'] = data.get('phone_number')
                login(request, user)
                if next_url != '':
                    messages.success(request, 'Login was successful')

                    return HttpResponseRedirect(next_url)
                else:
                    messages.success(request, 'Login was successful')
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Invalid username/password')
                return render(request, template_name=self.template_name, context={'request': request})
        else:
            messages.error(request, "Invalid username/password")
            return render(request, template_name=self.template_name, context={'request': request})


class LogoutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        messages.info(request, "You are now logged out login again to access the website")
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ScholarshipApplicationView(View):
    template_name = 'website/pages/apply_page.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ScholarshipApplicationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'request': request})

    def post(self, request, *args, **kwargs):

        # Check if the user has already applied
        user = request.user
        record_exists = ScholarshipApplication.objects.filter(email=request.POST.get('email')).exists()
        if record_exists:
            messages.error(request, 'You have already applied')
            return HttpResponseRedirect('/')

        # perform simple data validation
        else:
            form = ScholarshipApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Application Submitted successfully. "
                                          "You will be notified via email when the application is approved.")
                return HttpResponseRedirect('/')
            else:
                print(form.errors)
                messages.error(request, "Form data invalid. please check you form and submit again ")
                return HttpResponseRedirect('/')


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'request': request})


class ListAllApplicationView(TemplateView):
    template_name = 'website/pages/applications.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListAllApplicationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        applications = ScholarshipApplication.objects.all()

        return render(request, template_name=self.template_name,
                      context={'request': request, 'applications': applications})


class ManageApplicationView(View):
    template_name = 'website/pages/applications.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ManageApplicationView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        application_id = request.POST.get('id')
        application = get_object_or_404(ScholarshipApplication, id=application_id)

        operation = request.POST.get('operation')

        if operation == 'approve':
            application.application_status = 'approved'
        if operation == 'reject':
            application.application_status = 'rejected'

        application.save()
        messages.success(request, 'Application updated successfully')
        return render(request, template_name=self.template_name, context={'request': request})


class AdminDashboard(TemplateView):
    template_name = 'website/pages/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'request': request})


class ApprovedApplications(TemplateView):
    template_name = 'website/pages/approved_applications.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ApprovedApplications, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        applications = ScholarshipApplication.objects.filter(application_status='approved')

        return render(request, template_name=self.template_name,
                      context={'request': request, 'applications': applications})
