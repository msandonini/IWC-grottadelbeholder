
import json
import mimetypes

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from ProgettoIWC import settings
from grottadelbeholder.models import Content, RaceContent, ClassContent, MonsterContent, SpellContent
from grottadelbeholder.mylib.views.context import Context


BACKUP_FNAME = "backup.json"


# TODO DataTransferView
class DataTransferView(View):
    template_name = "grottadelbeholder/datatransfer.html"

    # Input di più contenuti da json
    def get(self, request):
        context = Context(request).getContext()

        print(request.GET)

        if "backup" in request.GET and request.GET["backup"] == "1":

            backupServer()

            fpath = settings.MEDIA_ROOT + "/" + BACKUP_FNAME

            with open(fpath, "r") as fout:
                mime_type, _ = mimetypes.guess_type(fpath)

                response = HttpResponse(fout, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % BACKUP_FNAME

                return response

        return render(request, self.template_name, context)

    def post(self, request):
        file = request.FILES['data']
        fss = FileSystemStorage()
        fPc = fss.save(file.name, file)
        fUrl = fss.url(fPc)

        '''
        file = request.FILES['data'].file

        data = json.load(file)
        '''
        #todo post

        dataStr = ""
        with open(settings.MEDIA_ROOT + "/" + file.name) as dataFile:
            dataStr = json.load(dataFile)

        return HttpResponse(str(dataStr))


def backupServer():
    dict = {
        "Content": list(Content.objects.values()),
        "Details": {
            "RaceContent": list(RaceContent.objects.values()),
            "ClassContent": list(ClassContent.objects.values()),
            "MonsterContent": list(MonsterContent.objects.values()),
            "SpellContent": list(SpellContent.objects.values())
        }
    }

    json_object = json.dumps(dict, indent=4, default=str)

    fss = FileSystemStorage()
    fss.save(BACKUP_FNAME, ContentFile(b""))

    with open(settings.MEDIA_ROOT + "/" + BACKUP_FNAME, "w") as file:
        file.write(json_object)

        file.close()
