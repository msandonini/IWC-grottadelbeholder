from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views import View

from .models import User, Admin, Content
from .forms import ClassContentForm

import hashlib

LOGGED_USER_KEY = 'loggedUser'
ADMIN_TYPE_KEY = 'adminType'

class IndexView(View):
    template_name = "grottadelbeholder/index.html"

    def get(self, request):
        context = contextSetup(request)

        if "filter" in request.GET:
            context["filter"] = request.GET["filter"]
            return render(request, self.template_name, context)

        return render(request, self.template_name, context)


class ReviewView(View):
    template_name = "grottadelbeholder/review.html"

    def get(self, request):
        context = contextSetup(request)

        if userIsLogged(request):
            return "ok"

        return "none"


class SigninView(View):
    template_name = "grottadelbeholder/signin.html"

    def get(self, request):
        context = {}

        if userIsLogged(request):
            return HttpResponseRedirect(redirect_to="./")

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}

        if userIsLogged(request):
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

                request.session[LOGGED_USER_KEY] = username
                context[LOGGED_USER_KEY] = request.session.get(LOGGED_USER_KEY)
                return HttpResponseRedirect(redirect_to="./")
        else:
            context["msg"] = "Inserire valori validi"

        return render(request, self.template_name, context)


class LoginView(View):
    template_name = "grottadelbeholder/login.html"

    def get(self, request):
        context = {}

        if 'loggedUser' in request.session:
            context[LOGGED_USER_KEY] = request.session.get(LOGGED_USER_KEY)
            return HttpResponseRedirect(redirect_to="./")

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}

        if userIsLogged(request):
            context[LOGGED_USER_KEY] = request.session.get(LOGGED_USER_KEY)
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
                        request.session[LOGGED_USER_KEY] = user.username
                        context[LOGGED_USER_KEY] = request.session.get(LOGGED_USER_KEY)

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
        if LOGGED_USER_KEY in request.session:
            del request.session[LOGGED_USER_KEY]

        return HttpResponseRedirect(redirect_to="./")


class InfoView(View):
    template_name = "grottadelbeholder/info.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)


class UserView(View):
    template_name = "grottadelbeholder/user.html"

    def get(self, request):

        if not userIsLogged(request):
            return HttpResponseRedirect(redirect_to="grottadelbeholder/login.html")

        context = contextSetup(request)

        return render(request, self.template_name, context)


class AdminView(View):
    template_name = "grottadelbeholder/admin.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)


class CreateContentView(View):
    template_name = "grottadelbeholder/create.html"

    def get(self, request):
        context = contextSetup(request)

        context['classForm'] = ClassContentForm()

        return render(request, self.template_name, context)


class AddContentView(View):
    def post(self, request):
        redirect = ''

        #TODO inserire redirect alla pagina del contenuto appena creato

        return HttpResponseRedirect(redirect_to=redirect)


class UserContentView(View):
    template_name = "grottadelbeholder/usercontent.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)


def contextSetup(request):
    context = {}

    if userIsLogged(request):
        context[LOGGED_USER_KEY] = request.session.get(LOGGED_USER_KEY)

    adminType = userAdminType(request)

    if not adminType is None:
        context[ADMIN_TYPE_KEY] = adminType

    return context


def userIsLogged(request):
    if LOGGED_USER_KEY in request.session:
        return True
    return False


def userAdminType(request):
    admins = Admin.objects.all()

    if userIsLogged(request):
        for admin in admins:
            if admin.user.username == request.session[LOGGED_USER_KEY]:
                return admin.type

    return None