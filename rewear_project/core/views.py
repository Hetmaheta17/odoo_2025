# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ItemForm
from .models import Item, User

# Helper function to check for admin
def is_admin(user):
    return user.is_staff

# --- Main Pages ---
def landing_page(request):
    featured_items = Item.objects.filter(approved=True, status='available').order_by('-created_at')[:4]
    return render(request, 'core/landing.html', {'featured_items': featured_items})

def browse_page(request):
    browse_items = Item.objects.filter(approved=True, status='available').order_by('-created_at')
    return render(request, 'core/browse.html', {'browse_items': browse_items})

@login_required
def dashboard_page(request):
    user_items = Item.objects.filter(uploader=request.user)
    return render(request, 'core/dashboard.html', {'user_items': user_items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id, approved=True)
    return render(request, 'core/item_detail.html', {'item': item})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploader = request.user
            item.save()
            # Award points for listing
            request.user.points += 10
            request.user.save()
            messages.success(request, 'Item submitted for approval! You earned 10 points.')
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'core/add_item.html', {'form': form})

# --- Authentication Views ---
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome bonus: {user.points} points.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('landing')

# --- Admin Panel Views ---
@user_passes_test(is_admin)
def admin_panel(request):
    pending_items = Item.objects.filter(approved=False)
    stats = {
        'total_items': Item.objects.count(),
        'active_users': User.objects.count(),
        'pending_items_count': pending_items.count(),
    }
    return render(request, 'core/admin_panel.html', {'stats': stats, 'pending_items': pending_items})

@user_passes_test(is_admin)
def approve_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.approved = True
    item.save()
    # Award bonus points to uploader
    uploader = item.uploader
    uploader.points += 20
    uploader.save()
    messages.success(request, f'Item "{item.title}" approved. 20 bonus points awarded to {uploader.username}.')
    return redirect('admin_panel')

@user_passes_test(is_admin)
def reject_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.error(request, 'Item rejected and removed.')
    return redirect('admin_panel')