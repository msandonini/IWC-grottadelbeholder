import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from grottadelbeholder.models import User
from grottadelbeholder.mylib.views.context import Context, LOGGED_USER_ID, LOGGED_USER_NAME


class SigninView(View):
    template_name = "grottadelbeholder/signin.html"

    def get(self, request):
        context = {}

        if Context(request).userIsLogged():
            return HttpResponseRedirect(redirect_to="./")

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}

        if Context(request).userIsLogged():
            return HttpResponseRedirect(redirect_to="./")

        if ("email" in request.POST) and ("username" in request.POST) and ("password" in request.POST):
            email = request.POST["email"]
            username = request.POST["username"]
            password = request.POST["password"]

            users = User.objects.all()
            emailInDb = False
            usernameInDb = False
            for user in users:
                if email == user.mail:
                    emailInDb = True
                    break
                if username == user.username:
                    usernameInDb = True
                    break

            if emailInDb:
                context["msg"] = "Email già associata a un account"
            elif usernameInDb:
                context["msg"] = "Username già associato a un account"

            if "msg" not in context:
                password = hashlib.sha256(password.encode()).digest()

                user = User(mail=email, username=username, password=password)
                user.save()

                request.session[LOGGED_USER_ID] = user.id
                request.session[LOGGED_USER_NAME] = username
                context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)
                return HttpResponseRedirect(redirect_to="./")
        else:
            context["msg"] = "Inserire valori validi"

        return render(request, self.template_name, context)

class LoginView(View):
    template_name = "grottadelbeholder/login.html"

    def get(self, request):
        context = {}

        if LOGGED_USER_ID in request.session:
            context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)
            return HttpResponseRedirect(redirect_to="./")

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}

        if Context(request).userIsLogged():
            context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)
            return HttpResponseRedirect(redirect_to="./")

        context = {}

        if "username" in request.POST and "password" in request.POST:
            userMailOrName = request.POST["username"]
            password = str(hashlib.sha256(request.POST["password"].encode()).digest())

            print("Username or mail: " + userMailOrName)
            print("Password: " + password)
            for user in User.objects.all():
                print(user.mail)
                print(user.username)
                print(user.password)
                if user.mail == userMailOrName or user.username == userMailOrName:
                    if password == user.password:
                        request.session[LOGGED_USER_NAME] = user.username
                        request.session[LOGGED_USER_ID] = user.id
                        context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)

                        return HttpResponseRedirect(redirect_to="./")
                    else:
                        context["msg"] = "Password errata"
                        break
            if "msg" not in context:
                context["msg"] = "Utente non registrato"
        else:
            context["msg"] = "Inserire valori validi"

        return render(request, self.template_name, context)

class LogoutView(View):

    def get(self, request):
        if LOGGED_USER_ID in request.session:
            del request.session[LOGGED_USER_ID]

        if LOGGED_USER_NAME in request.session:
            del request.session[LOGGED_USER_NAME]

        return HttpResponseRedirect(redirect_to="./")
