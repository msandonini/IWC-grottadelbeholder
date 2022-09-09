from grottadelbeholder.models import User, Admin

LOGGED_USER_ID = 'loggedUserID'
LOGGED_USER_NAME = 'loggedUser'
ADMIN_TYPE_KEY = 'adminType'

class Context():
    def __init__(self, request):
        self.request = request

    def getContext(self):
        context = {}

        try:
            if self.userIsLogged():
                context[LOGGED_USER_NAME] = User.objects.get(id=self.request.session[LOGGED_USER_ID]).username

            adminType = self.userAdminType()

            if not adminType is None:
                context[ADMIN_TYPE_KEY] = adminType

        except:
            del self.request.session[LOGGED_USER_ID]
            del self.request.session[LOGGED_USER_NAME]
            del self.request.session[ADMIN_TYPE_KEY]

        return context

    def userIsLogged(self):
        if LOGGED_USER_ID in self.request.session:
            return True
        return False

    def userAdminType(self):
        admins = Admin.objects.all()

        if self.userIsLogged():
            for admin in admins:
                if admin.user_id == self.request.session[LOGGED_USER_ID]:
                    return admin.type

        return None