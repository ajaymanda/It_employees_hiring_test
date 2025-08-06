
from django.urls import path
from django.urls import path
from .views import login_view, web_cam_view,upload_photos,exam_page,submit_exam,log_exam_warning,save_snapshot,employee_snapshots
urlpatterns = [
    path('', login_view, name='login'),
    path('webcam/', web_cam_view, name='webcam'),
    path('upload_photos/',upload_photos, name='upload_photos'),
    path('exam/', exam_page, name='exam_page'),
    path('submit_exam/', submit_exam, name='submit_exam'),
    path('log-warning/', log_exam_warning, name='log_exam_warning'),
    path('employee/<int:employee_id>/snapshots/', employee_snapshots, name='employee_snapshots'),
    path('save-snapshot/', save_snapshot, name='save_snapshot'),
    path('employee/<int:employee_id>/snapshots/', employee_snapshots, name='employee_snapshots'),

]