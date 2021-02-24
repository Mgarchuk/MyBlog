from django.views.generic import CreateView
from .models import Post, Photo
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, PhotoForm, CommentForm, AuthUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import logging
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from multiprocessing import Process

logger = logging.getLogger('django')


def main_page(request):
    logger.info('Main page loaded')
    return render(request, 'blog/main_page.html')


def post_list(request):
    logger.info('posts')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    logger.info('post')
    post = Post.objects.get(pk=pk)
    comments = post.comments.filter(status=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.published_date = timezone.now()
            new_comment.post = post
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def edit_post(request):
    logger.info('edit_post')
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_edit.html', {'post_list': posts})


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            logger.info('post created')
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def create_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info('photo created')
            photo = form.save(commit=False)
            photo.author = request.user
            photo.published_date = timezone.now()
            photo.save()
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'blog/create_photo.html', {'form': form})


def photo_list(request):
    if request.method == 'GET':
        logger.info("Get photo list")
        pic = Photo.objects.all()
        return render(request, 'blog/photo_list.html', {'photo': pic})


def update_post(request, pk):
    get_form = Post.objects.get(pk=pk)
    if request.method == "POST":
        logger.info("Post updated")
        form = PostForm(request.POST, instance=get_form)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    form = PostForm(instance=get_form)
    return render(request, 'blog/post_edit.html', {'get_post': get_form, 'update': True, 'form': form})


def delete_post(request, pk):
    Post.objects.filter(pk=pk).delete()
    logger.info('post deleted')
    return redirect(reverse('post_edit'))


class MyProjectLoginView(LoginView):
    template_name = "blog/entry.html"
    form_class = AuthUserForm
    success_url = reverse_lazy('post_edit')

    def get_success_url(self):
        return self.success_url


def log_process():
    logger.info('successfully send token')

def RegisterUserView(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            logger.info('registration completed')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            #username = form.cleaned_data['username']
            #raw_password = form.cleaned_data['password']

            current_site = get_current_site(request)
            email_subject = 'Активация аккаунта'
            message = render_to_string('blog/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])

            sending_process = Process(target=email.send)

            sending_process.start()

            sending_process.join()

            #email.send()
            #user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_edit')
    else:
        form = RegisterUserForm()

    return render(request, 'blog/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        logger.info('activation completed')
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('main_page')




