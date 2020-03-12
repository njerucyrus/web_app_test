from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


class RegisterView(View):
    template_name = 'register.html'

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
            redirect_route = '/login/'
            messages.success(request, 'Account created successfully. Login to proceed')
            return HttpResponseRedirect(redirect_to=redirect_route)
