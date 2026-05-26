from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Post, Category, Comment, Like
from .forms import PostForm, CommentForm, UserRegisterForm


def home(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(published=True).select_related('author', 'category')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(category__name__icontains=query) |
            Q(author__username__icontains=query)
        )

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')
    featured = Post.objects.filter(published=True).order_by('-likes')[:3] if not query else []

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'featured': featured,
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.select_related('author').all()
    comment_form = CommentForm()
    user_liked = False

    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', slug=slug)

    related_posts = Post.objects.filter(
        published=True,
        category=post.category
    ).exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Post "{post.title}" created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Update', 'post': post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Post "{title}" deleted.')
        return redirect('dashboard')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author or request.user == comment.post.author:
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, 'Comment deleted.')
        return redirect('post_detail', slug=post_slug)
    messages.error(request, 'Permission denied.')
    return redirect('home')


@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    count = post.likes.count()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': count})
    return redirect('post_detail', slug=slug)


@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).annotate(
        likes_total=Count('likes'),
        comment_count_ann=Count('comments')
    ).order_by('-created_at')

    total_posts = user_posts.count()
    total_likes = sum(p.likes_total for p in user_posts)
    total_comments = sum(p.comment_count_ann for p in user_posts)
    published_count = user_posts.filter(published=True).count()

    context = {
        'user_posts': user_posts,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'published_count': published_count,
    }
    return render(request, 'blog/dashboard.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True).select_related('author')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.annotate(post_count=Count('posts'))
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
