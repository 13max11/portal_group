from django.shortcuts import render, redirect
from portfolio_system.models import Project

def project_details(request, pk):
    project = Project.objects.get(id=pk)
    context = {
        'project': project
    }
    return render(request, 'portfolio_sys/project_details.html', context)


