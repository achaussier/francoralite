import sys
import subprocess
import django
from rest_framework import views
from rest_framework.response import Response
from ..version import __version__

import os


class VersionsView(views.APIView):

    def get(self, request, format=None):
        data = {}

        # Git
        stdout, stderr = subprocess.Popen(
            "git rev-parse HEAD",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True
        ).communicate()
        data["git_commit"] = stdout.strip()

        # Python
        data["python"] = sys.version

        # Django
        data["django"] = django.VERSION

        # Application
        data["application"] = __version__


        return Response(data)
