from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile
from users.utils import paginate
from .models import Post, Tag, Category
from .forms import PostForm, CommentForm
from .utils import search_posts


def get_tags_categories(posts):
    categories = set()
    tags = set()

    for post in posts:
        categories.add(post.category)

        for tag in post.tags.all():
            tags.add(tag)

    return tags, categories


@login_required
def create_post(request):
    profile = request.user.profile

    form = PostForm()

    if request.method == 'POST':
        request.POST.getlist('tags')

        new_tags = request.POST.get('new_tags').replace(',', ' ').split()

        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save()

            post.owner = profile

            post.save()

            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)

                post.tags.add(tag)

            return redirect('blog:my_blog')

    context = {
        'form': form
    }

    return render(request, 'blog/post-form.html', context)


@login_required
def user_blog(request, username):
    profile = Profile.objects.get(username=username)

    posts = profile.post_set.all()

    tags, categories = get_tags_categories(posts)

    custom_range, posts = paginate(request, posts, 3)

    context = {
        'profile': profile,
        'posts': posts,
        'tags': tags,
        'categories': categories,
        'custom_range': custom_range
    }

    return render(request, 'blog/user_blog.html', context)


@login_required
def post(request, post_slug):
    post = Post.objects.get(slug=post_slug)

    profile = request.user.profile

    comments = post.comments.filter(approved=True)

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        comment = form.save(commit=False)
        comment.post = post
        comment.owner = request.user.profile
        comment.save()

        messages.success(request, 'Your comment will appear after verification by a moderator')

        return redirect('blog:post', post_slug=post.slug)

    context = {
        'post': post,
        'profile': profile,
        'comments': comments,
        'form': form
    }

    return render(request, 'blog/single-post.html', context)


@login_required
def my_blog(request):
    profile = request.user.profile

    posts = profile.post_set.all()

    tags, categories = get_tags_categories(posts)

    custom_range, posts = paginate(request, posts, 3)

    context = {
        'profile': profile,
        'posts': posts,
        'custom_range': custom_range,
        'tags': tags,
        'categories': categories
    }

    return render(request, 'blog/my-blog.html', context)


@login_required
def update_post(request, pk):
    profile = request.user.profile

    post = profile.post_set.get(id=pk)

    form = PostForm(instance=post)

    if request.method == 'POST':
        new_tags = request.POST.get('new_tags').replace(',', ' ').split()

        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()

            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)

                post.tags.add(tag)

            return redirect('blog:my_blog')

    context = {
        'form': form,
        'post': post
    }

    return render(request, 'blog/post-form.html', context)


@login_required
def delete_post(request, pk):
    profile = request.user.profile

    post = profile.post_set.get(id=pk)

    if request.method == 'POST':
        post.delete()

        return redirect('blog:my_blog')

    context = {
        'object': post
    }

    return render(request, 'delete.html', context)


@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)

        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)

            post.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        post.likes.remove(request.user)

        post.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def bookmark_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)

        if not post.bookmarks.filter(id=request.user.id).exists():
            post.bookmarks.add(request.user)

            post.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        post.bookmarks.remove(request.user)

        post.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def friends(request):
    profile = request.user.profile

    posts = Post.objects.filter(owner__in=profile.follows.all())

    tags, categories = get_tags_categories(posts)

    posts, search_query = search_posts(request)

    custom_range, posts = paginate(request, posts, 3)

    context = {
        'profile': profile,
        'posts': posts,
        'search_query': search_query,
        'custom_range': custom_range,
        'tags': tags,
        'categories': categories
    }

    return render(request, 'blog/post-list.html', context)


@login_required
def user_bookmarks(request):
    profile = request.user.profile

    user = request.user

    posts = Post.objects.filter(bookmarks__in=[user])

    tags, categories = get_tags_categories(posts)

    custom_range, posts = paginate(request, posts, 3)

    context = {
        'profile': profile,
        'posts': posts,
        'custom_range': custom_range,
        'tags': tags,
        'categories': categories
    }

    return render(request, 'blog/post-list.html', context)


@login_required
def posts_by_category(request, category_slug):
    profile = request.user.profile

    category = get_object_or_404(Category, slug=category_slug)

    posts = Post.objects.filter(category__slug__contains=category_slug)

    tags, categories = get_tags_categories(posts)

    custom_range, posts = paginate(request, posts, 3)

    context = {
        'profile': profile,
        'posts': posts,
        'custom_range': custom_range,
        'tags': tags,
        'category': category,
        'categories': categories
    }

    return render(request, 'blog/post-list.html', context)


@login_required
def posts_by_tag(request, tag_slug):
    profile = request.user.profile

    tag = get_object_or_404(Tag, slug=tag_slug)

    posts = Post.objects.filter(tags__in=[tag])

    tags, categories = get_tags_categories(posts)

    custom_range, posts = paginate(request, posts, 3)

    context = {
        'profile': profile,
        'posts': posts,
        'custom_range': custom_range,
        'tags': tags,
        'tag': tag,
        'categories': categories
    }

    return render(request, 'blog/post-list.html', context)
