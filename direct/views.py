from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from .models import Message

@login_required
def inbox(request):
    messages = Message.get_messages(user=request.user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, recipient=message['user'])
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    return render(request, 'direct/direct.html', context)

@login_required
def directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    other_user = get_object_or_404(User, username=username)
    directs = Message.objects.filter(user=user, recipient=other_user)
    directs.update(is_read=True)
    
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    return render(request, 'direct/direct.html', context)

@login_required
def new_conversation(request, username):
    try:
        to_user = get_object_or_404(User, username=username)
        if to_user != request.user:
            Message.send_message(request.user, to_user, '')
            return redirect('directs', username=username)
        return redirect('usersearch')
    except User.DoesNotExist:
        return redirect('usersearch')

@login_required
def send_direct(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body', '').strip()
    
    if not body:
        return redirect('directs', username=to_user_username)
    
    try:
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
    except User.DoesNotExist:
        pass
    
    return redirect('directs', username=to_user_username)

@login_required
def user_search(request):
    query = request.GET.get('q', '').strip()
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(username=request.user.username)[:15]

    context = {
        'users': users,
        'query': query,
    }

    return render(request, 'direct/search_user.html', context)

# Optional: Add this to context_processors.py or keep it in views.py
def checkDirects(request):
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(user=request.user, is_read=False).count()
        return {'directs_count': directs_count}
    return {'directs_count': 0}
