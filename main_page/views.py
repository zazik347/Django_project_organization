import requests
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from contracts.models import Contract
from projects.models import Project


# Create your views here.

def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def avtomatiz(request):
    return render(request, 'avtomatiz.html')
def contacts(request):
    return render(request, 'contacts.html')
def reviews(request):
    return render(request, 'reviews.html')
def search_choose(request):
    return render(request, 'search_choose.html')

# def search(request):
#     query = request.GET.get('q', '').strip()
#
#     contracts = Contract.objects.filter(number__icontains=query) if query else Contract.objects.none()
#     projects = Project.objects.filter(title__icontains=query) if query else Project.objects.none()
#
#     return render(request, 'search_results.html', {
#         'query': query,
#         'contracts': contracts,
#         'projects': projects,
#     })
def search(request):
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', '')  # 'contract' или 'project'
    print(search_type, query)

    contracts = []
    projects = []

    if search_type == 'contract':
        # Ищем только по номеру договора
        contracts = Contract.objects.filter(number__icontains=query)

    elif search_type == 'project':
        # Ищем только по названию проекта
        projects = Project.objects.filter(title__icontains=query)

    else:
        # Если не указан тип — ищем и по договорам, и по проектам
        contracts = Contract.objects.filter(number__icontains=query)
        projects = Project.objects.filter(title__icontains=query)

    return render(request, 'search_results.html', {
        'query': query,
        'search_type': search_type,
        'contracts': contracts,
        'projects': projects,
    })

def search_by_contract_number(request):
    pass
