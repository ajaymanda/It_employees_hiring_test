from django.shortcuts import render

# Create your views here.
from datetime import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Employee
from django.views.decorators.csrf import csrf_exempt

import base64
import uuid
import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from .models import Photo, Employee



import base64
import uuid
import json
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from .models import Employee, Photo

from .models import Question, UserAnswer,Employee
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ExamWarning  # You'll create this model below

import base64
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.files.base import ContentFile
from .models import Snapshot, Employee
import json

# -------------------------
# Employee Login
# -------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        try:
            employee = Employee.objects.get(user_name=username, password=password)
            request.session['employee_id'] = employee.id
            return redirect('webcam')  # Go to webcam page
        except Employee.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


# -------------------------
# Webcam Page
# -------------------------
def web_cam_view(request):
    if 'employee_id' not in request.session:
        return redirect('login')
    return render(request, 'web_cam.html')


# -------------------------
# Handle Upload of 5 Photos
# -------------------------
def upload_photos(request):
    if request.method == 'POST':
        if 'employee_id' not in request.session:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        employee_id = request.session['employee_id']
        employee = Employee.objects.get(id=employee_id)

        data = json.loads(request.body)
        images = data.get('images', [])

        for img_data in images:
            format, imgstr = img_data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"{employee.user_name}_{uuid.uuid4()}.{ext}"
            img_file = ContentFile(base64.b64decode(imgstr), name=filename)
            Photo.objects.create(employee=employee, image=img_file)

        return JsonResponse({'message': 'Photos uploaded successfully'})


# -------------------------
# Exam Page
# -------------------------


def exam_page(request):
    if 'employee_id' not in request.session:
        return redirect('login')

    employee_id = request.session['employee_id']
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                try:
                    question = Question.objects.get(id=question_id)
                    UserAnswer.objects.create(
                        employee=employee,
                        question=question,
                        selected_option=value
                    )
                except Question.DoesNotExist:
                    continue

        return redirect('submit_exam')  # ✅ Redirect to success page

    questions = Question.objects.all()
    
    return render(request, 'exam_page.html', {
        'employee': employee,
        'questions': questions
    })




def submit_exam(request):
    if request.method == 'POST':
        employee_id = request.session.get('employee_id')
        if not employee_id:
            return redirect('login')  # Redirect if not logged in

        employee = Employee.objects.get(id=employee_id)

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                selected_option = value
                question = Question.objects.get(id=question_id)
                is_correct = selected_option == question.correct_option

                UserAnswer.objects.create(
                    employee=employee,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

        return render(request, 'exam_submitted.html')
    
    return redirect('exam')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ExamWarning, Employee

@csrf_exempt
def log_exam_warning(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reason = data.get('reason')

        # Get employee from session (assuming you store employee ID on login)
        employee_id = request.session.get('employee_id')
        employee = Employee.objects.filter(id=employee_id).first() if employee_id else None

        ExamWarning.objects.create(employee=employee, reason=reason)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid request'}, status=400)



@csrf_exempt
def save_snapshot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data.get('image')
        employee_id = data.get('employee_id')

        if image_data and employee_id:
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                employee = Employee.objects.get(id=employee_id)
                image_file = ContentFile(base64.b64decode(imgstr), name=f'snapshot_{employee_id}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{ext}')
                Snapshot.objects.create(employee=employee, image=image_file)
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'}, status=400)


def employee_snapshots(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    snapshots = Snapshot.objects.filter(employee=employee).order_by('-timestamp')
    return render(request, 'admin_snapshots.html', {
        'employee': employee,
        'snapshots': snapshots
    })
