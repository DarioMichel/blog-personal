from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            image=image
        )
        messages.success(request, 'Post creado exitosamente!')
        return redirect('blog:index')
    return redirect('blog:index')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' and post.author == request.user:
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        messages.success(request, 'Post actualizado exitosamente!')
    return redirect('blog:index')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' and post.author == request.user:
        post.delete()
        messages.success(request, 'Post eliminado exitosamente!')
    return redirect('blog:index')

