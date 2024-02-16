from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Profile, Interest
from .forms import CustomUserCreationForm, ProfileForm, InterestForm, MessageForm
from .utils import paginate, search_profiles



def home(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    profiles, search_query = search_profiles(request)

    custom_range, profiles = paginate(request, profiles, 3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }

    return render(request, 'home.html', context)


def home_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Invalid user name or password')

    return redirect('home')


def profiles(request):
    profiles, search_query = search_profiles(request)

    custom_range, profiles = paginate(request, profiles, 3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }

    return render(request, 'users/profiles.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/auth.html')


def logout_user(request):
    logout(request)

    messages.info(request, 'You have logged out of your account')

    return redirect('login')


def signup_user(request):
    page = 'signup'

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Account created')

            login(request, user)

            return redirect('edit_account')

        else:
            messages.error(request, 'An error occurred during sign up')

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/auth.html', context)


def user_profile(request, username):
    profile = Profile.objects.get(username=username)

    interests = profile.interest_set.all()
    profiles = profile.follows.all()

    custom_range, profiles = paginate(request, profiles, 3)

    context = {
        'profile': profile,
        'profiles': profiles,
        'interests': interests,
        'custom_range': custom_range
    }

    return render(request, 'users/user_profile.html', context)


@login_required
def profiles_by_interest(request, interest_slug):
    interest = Interest.objects.filter(slug__icontains=interest_slug)
    profiles = Profile.objects.exclude(user=request.user).distinct().filter(Q(interest__in=interest))

    context = {
        'profiles': profiles
    }

    return render(request, 'users/profiles.html', context)


@login_required
def user_account(request):
    profile = request.user.profile

    interests = profile.interest_set.all()
    profiles = profile.follows.all()

    custom_range, profiles = paginate(request, profiles, 3)

    context = {
        'profile': profile,
        'profiles': profiles,
        'interests': interests,
        'custom_range': custom_range
    }

    return render(request, 'users/account.html', context)


@login_required
def edit_account(request):
    profile = request.user.profile

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/profile-form.html', context)


@login_required
def create_interest(request):
    profile = request.user.profile

    form = InterestForm()

    if request.method == 'POST':
        form = InterestForm(request.POST)

        if form.is_valid():
            interest = form.save(commit=False)

            interest.description = request.POST.get('description')

            interest.profile = profile

            try:
                interest.save()

                messages.success(request, 'Interest added')

                return redirect('account')

            except IntegrityError:
                form.add_error('name', 'You already have that interest')

    context = {
        'form': form
    }

    return render(request, 'users/interest-form.html', context)


@login_required
def update_interest(request, interest_slug):
    profile = request.user.profile

    interest = profile.interest_set.get(slug=interest_slug)

    form = InterestForm(instance=interest)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)

        if form.is_valid():
            form.save()

            messages.success(request, 'Interest updated')

            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/interest-form.html', context)


@login_required
def delete_interest(request, interest_slug):
    profile = request.user.profile

    interest = profile.interest_set.get(slug=interest_slug)

    if request.method == 'POST':
        interest.delete()

        messages.success(request, 'Interest deleted')

        return redirect('account')

    context = {
        'object': interest
    }

    return render(request, 'delete.html', context)


@login_required
def inbox(request):
    profile = request.user.profile

    message_requests = profile.messages.all()

    unread_count = message_requests.filter(seen=False).count()

    context = {
        'message_requests': message_requests,
        'unread_count': unread_count
    }

    return render(request, 'users/inbox.html', context)


@login_required
def view_message(request, pk):
    profile = request.user.profile

    message = profile.messages.get(id=pk)

    if not message.seen:
        message.seen = True
        message.save()

    context = {
        'message': message
    }

    return render(request, 'users/message.html', context)


def create_message(request, username):
    recipient = Profile.objects.get(username=username)

    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, 'Message sent')

            return redirect('user_profile', username=recipient.username)

    context = {
        'recipient': recipient,
        'form': form
    }

    return render(request, 'users/message-form.html', context)


@login_required
def toggle_follow(request, username):
    profile = Profile.objects.get(username=username)

    if request.method == 'POST':
        current_user_profile = request.user.profile

        data = request.POST

        action = data.get('follow')

        if action == 'follow':
            current_user_profile.follows.add(profile)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)

        current_user_profile.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
