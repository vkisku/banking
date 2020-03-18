from email.mime.image import MIMEImage

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from .forms import SignupForm, ProfileForm, LoginForm,PasswordChangeCustomForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
#from .models import profile_extension
from django.core.mail import EmailMessage
from theme import views as homeViews
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponse, JsonResponse


def login(request):
    if request.user.is_authenticated:
        return redirect(homeViews.home)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            rememberMe=request.POST['rememberme']
        except:
            rememberMe = "off"
            pass
        if '@' in username:
            try:
                user=get_object_or_404(User,email=username)
                user = authenticate(username=user.username, password=password)
            except:
                user = authenticate(username=username, password=password)
                pass
        else:
            user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(homeViews.home)
        else:

            messages.error(request,
                           'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect(homeViews.home)
    data = {}

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Miner account.'

            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            data['confirm_registration'] = 'Please confirm your email address to complete the registration'
            return render(request, 'acc_or_not.html', {'data': data})
    else:
        # mine = MineDetails.objects.all()
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def email_embed_image(email, img_content_id, img_data):
    """
    email is a django.core.mail.EmailMessage object
    """
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)

def activate(request, uidb64, token):
    # htmlOpen = '<div class="row"><div class="wrapper fadeInDown"><div id="formContent">';
    # htmlClosed = '</div></div></div>'
    data = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        data['success'] = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request, 'acc_or_not.html', {'data': data})
    else:
        data['err'] = 'Activation link is invalid!'
        return render(request, 'acc_or_not.html', {'data': data})


@login_required
def profile(request,action="overview", template_name='profile.html'):
    current_user = request.user
    active={}
    active['overview']=""
    active['setting']=""
    active['tasks']=""
    active['help']=""
    active[action]="active"
    book = get_object_or_404(User, pk=current_user.id)
    book_extension, created = profile_extension.objects.get_or_create(user_id=book)
    form_extension = ProfileExtensionForm(request.POST or None, request.FILES, instance=book_extension)


    if action=='overview':
        form = ProfileForm(request.POST or None, instance=book)
    elif action == 'setting':
        form = PasswordChangeCustomForm(request.user)
        try:
            if request.method == 'POST':
                form=PasswordChangeCustomForm(request.user,request.POST)
                if form.is_valid():
                    form.save()
                    return render(request, template_name,
                                  {'form': form, 'form_extension': form_extension, 'active': active})
                else:
                    print('I am Here')
                     # form = PasswordChangeCustomForm(request.user)
                    return render(request, template_name,
                              {'form': form, 'form_extension': form_extension, 'active': active})
        except:
            pass
        # print(form)
    # book_extension = get_object_or_404(profile_extension,user_id=current_user.id)


    try:
        if request.method == 'POST':
            if form.is_valid():
                print('form is valid')
                form.save()
            if form_extension.is_valid():
                print('form extension is valid')
                # print(form_extension)
                fs = form_extension.save(commit=False)
                fs.user_id = book
                fs.save()
            return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print('Error MEssage=>', e)

    return render(request, template_name, {'form': form, 'form_extension': form_extension,'active':active})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
