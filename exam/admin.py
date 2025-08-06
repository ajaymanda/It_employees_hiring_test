
from django.contrib import admin
from .models import Employee, Photo ,Question ,UserAnswer,ExamWarning,Snapshot
from django.utils.html import format_html

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'phone_no']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'image', 'created_at']
    list_filter = ['employee']


admin.site.register(Question)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('employee', 'question', 'selected_option', 'is_correct', 'submitted_at')
    list_filter = ('employee', 'is_correct', 'submitted_at')
    search_fields = ('employee__user_name', 'question__text')
    
@admin.register(ExamWarning)
class ExamWarningAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reason', 'timestamp')
    list_filter = ('reason', 'timestamp')
    search_fields = ('employee__user_name', 'reason')


from django.shortcuts import render
from .models import Employee, Snapshot

def employee_snapshots(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    snapshots = Snapshot.objects.filter(employee=employee).order_by('-timestamp')
    return render(request, 'admin_snapshots.html', {
        'employee': employee,
        'snapshots': snapshots
    })



@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    fields = ('employee', 'image', 'timestamp')
    readonly_fields = ('timestamp',)
    list_display = ('employee', 'timestamp', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"
    image_tag.short_description = 'Image'

