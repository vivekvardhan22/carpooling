from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from post.forms import NewPostForm
from post.models import Stream, Post, Tag
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authy.models import Profile
from django.db.models import Q
from .forms import SearchForm


# Create your views here.
@login_required
def index(request):
    user = request.user
    
    # Get all post ids that appear in the stream of the current user
    post_ids = Stream.objects.filter(user=user).values_list('post', flat=True)
    
    # Fetch posts that are in the user's stream, ordered by the most recent
    post_items = Post.objects.filter(id__in=post_ids).order_by('-posted')

    # Render the template with the context
    context = {
        'post_items': post_items,
    }
    
    return render(request, 'index.html', context)


@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    template = loader.get_template('post_detail.html')

    context = {
        'post': post,
    }

    return HttpResponse(template.render(context, request))



@login_required
def NewPost(request):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Cleaned data from the form
            content = form.cleaned_data.get('content')
            leaving_from = form.cleaned_data.get('leaving_from')
            going_to = form.cleaned_data.get('going_to')
            date_time = form.cleaned_data.get('date_time')
            transport_mode = form.cleaned_data.get('transport_mode')
            tags_form = form.cleaned_data.get('tags')

            # Handle tags (comma-separated string)
            tags_list = [tag.strip() for tag in tags_form.split(',')]  # Split and strip whitespace
            tags_objs = []

            for tag_title in tags_list:
                # Get or create tags based on the provided list
                tag, created = Tag.objects.get_or_create(title=tag_title)
                tags_objs.append(tag)

            # Create the Post object
            post = Post.objects.create(
                user=user,
                content=content,
                leaving_from=leaving_from,
                going_to=going_to,
                date_time=date_time,
                transport_mode=transport_mode
            )

            # Assign tags to the post
            post.tags.set(tags_objs)  # Many-to-Many relation
            post.save()

            return redirect('index')  # Redirect to the index page after successful creation
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)

@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    
    return render(request, 'tag.html', context)

@login_required
def search_view(request):
    form = SearchForm()
    context = {'form': form}
    return render(request, 'search.html', context)

@login_required
def search_results(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            leaving_from = form.cleaned_data.get('leaving_from')
            going_to = form.cleaned_data.get('going_to')
            date_time = form.cleaned_data.get('date_time')
            
            # Build query
            query = Q()
            if leaving_from:
                query &= Q(leaving_from__icontains=leaving_from)
            if going_to:
                query &= Q(going_to__icontains=going_to)
            if date_time:
                # Search for posts on the same date
                query &= Q(date_time__date=date_time.date())
            
            posts = Post.objects.filter(query).order_by('-posted')
            
            return render(request, 'search_results.html', {
                'posts': posts,
                'form': form
            })
    
    return redirect('search')
