import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .auth import ServerAuth


def get_drive_root():
    '''
    '''
    # Create the folder if it doesn't exist
    try:
        os.mkdir(os.path.join(settings.DRIVE_ROOT))
    except:
        pass
    return settings.DRIVE_ROOT


def get_latest_snapshot_view(request):
    '''
    '''
    if request.method != 'GET':
        return Http404()

    try:
        ServerAuth.verify_auth_header(request)
    except AuthenticationFailed as err:
        return HttpResponse(str(err), status=status.HTTP_401_UNAUTHORIZED)

    snapshot = None
    for file_path in os.listdir(get_drive_root()):
        file_path = get_drive_root() / file_path
        if not snapshot:
            snapshot = file_path
            continue

    # Check if any file was found
    if snapshot == None:
        return HttpResponse(
            'No server files were found on the drive.',
            status=status.HTTP_400_BAD_REQUEST,
        )

    file = default_storage.open(file_path, 'rb')
    response = HttpResponse(file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="server.zip"'
    return response


class UploadSnapshotAPIView(views.APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        '''
        '''
        ServerAuth.verify_auth_header(request)

        snapshot = request.data.get('file', None)
        if not snapshot:
            return Response(
                'File is required.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = timezone.now()
        file_name = ('snapshot_'
                     f'{now.strftime("%d-%b-%Y")}_'
                     f'{int(now.timestamp())}.zip')
        file_path = get_drive_root() / file_name

        try:
            with default_storage.open(file_path, 'wb+') as output:
                for chunk in snapshot.chunks():
                    output.write(chunk)

        except Exception as ex:
            Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

        # Respond
        return Response(status=status.HTTP_204_NO_CONTENT)