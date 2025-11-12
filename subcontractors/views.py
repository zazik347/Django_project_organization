from django.shortcuts import render
from .models import Subcontractor


def subcontractor_list(request):
    subcontractors = Subcontractor.objects.all()
    return render(request, 'subcontractor_list.html', {
        'subcontractors': subcontractors
    })
