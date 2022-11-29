from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from users.auth import JWTAuthentication
class FileUploadView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self,
             request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url': 'http://localhost:8000' + url
        })