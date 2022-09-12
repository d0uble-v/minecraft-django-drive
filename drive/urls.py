from django.urls import path
from .views import UploadSnapshotAPIView, get_latest_snapshot_view

urlpatterns = [
    path(
        'snapshots/latest',
        get_latest_snapshot_view,
        name='get-latest-snapshot',
    ),
    path(
        'snapshots/upload',
        UploadSnapshotAPIView.as_view(),
        name='upload-snapshot',
    ),
]