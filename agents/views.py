from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AgentForm
from .models import Agent

# Create your views here.
@login_required
def add_agent(request):
    if not request.user.is_staff:
        messages.warning(request, "Only Staff may access this page")
        return render(request, 'access-denied.html')

    
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.save()
            return redirect('agent-details', pk=agent.pk)
    else:
        form = AgentForm()
    return render(request, 'add-agent.html', {'form': form})


def agent_details(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    return render(request, 'agent-details.html', {'agent': agent})


def find_agent(request):
     agents = Agent.objects.all()

     return render(request, 'find-agent.html', {'agents': agents})