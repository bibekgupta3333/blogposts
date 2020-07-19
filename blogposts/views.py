from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .models import Post
from .forms import PostForm, PostCreateForm
from django.core.paginator import Paginator
from django.db.models import Q


def list_post(request):
    objects = Post.published.all().order_by('-created')
    feartured = Post.published.all().order_by('count')[:6]
    print(request.GET.get('q'))
    if request.GET.get('q'):
        value = request.GET.get('q')
        objects = Post.objects.filter(
            Q(title__icontains=value) | Q(body__icontains=value) | Q(author__username=value))
        objects = objects.order_by('-created')
    users = User.objects.all()
    paginator = Paginator(objects, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogposts/common_list.html',
                  {'objects': page_obj, 'users': users, 'featured': feartured, 'page_obj': page_obj})


def user_post_list(request, author, author_id):
    objects = Post.objects.all().filter(Q(author__username=author)
                                        | Q(author__id=author_id))
    objects = objects.order_by('-created')
    if not request.user.is_authenticated:
        objects = Post.objects.all().filter(status='published').filter(author__username=author).filter(
            author__id=author_id)
        objects = objects.order_by('-created')

    print(objects)
    if request.GET.get('q'):
        value = request.GET.get('q')
        print(value)
        objects = objects.filter(
            Q(title__icontains=value) | Q(body__icontains=value) | Q(author__username=value) | Q(
                status__icontains=value))

    user = get_object_or_404(User, pk=author_id)
    paginator = Paginator(objects, 4)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    return render(request, 'blogposts/user_list.html',
                  {'objects': page_obj, 'page_obj': page_obj, 'user': user, 'counts': objects.count})


def detail_post(request, author, author_id, slug):
    objects = get_object_or_404(
        Post, author__username=author, author__id=author_id, slug=slug)

    objects.count = objects.count + 1
    objects.save()

    return render(request, 'blogposts/detail.html', {'objects': objects})


def create_post(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(
            data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()

            return redirect('blogposts:user_post_list', request.user.username, request.user.id)
    return render(request, 'blogposts/create.html', {'form': form})


def update_post(request, author, author_id, slug):
    obj = get_object_or_404(Post, author__id=author_id,
                            author__username=author, slug=slug)

    form = PostForm(instance=obj)
    if request.method == 'POST':
        form = PostForm(instance=obj, data=request.POST, files=request.FILES)

        print('error p1')
        if form.is_valid():
            print('error2')
            form.save()
            print('erro3')
            return redirect('blogposts:user_post_list', request.user.username, request.user.id)

    return render(request, 'blogposts/update.html', {'form': form})


def delete_post(request, author_id, slug):
    obj = get_object_or_404(Post, author__id=author_id, slug=slug)
    obj.delete()
    return redirect('blogposts:user_post_list', request.user.username, request.user.id)
