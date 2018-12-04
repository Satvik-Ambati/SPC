from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm, DocumentForm
from django.views.decorators.csrf import csrf_exempt
from .models import Document

# Create your views here.
def home(request):
	return render(request, 'accounts/home.html')

@csrf_exempt
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Your account has been created! You can now login as '+username)
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'accounts/register.html', {'form': form})

@csrf_exempt
def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		# username = form.cleaned_data.get('username')
		# password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				#files=File.objects.filter(user=request.user)
				return render(request, 'accounts/home.html',{'form':form})
			else:
				return render(request, 'accounts/login.html',{'form':form})
		else:
			messages.error(request, 'invalid credentials')     #login error message not created html
			return redirect('login')
	else:
		form = UserLoginForm()
	return render(request, 'accounts/login.html',{'form':form})

def user_logout(request):
	logout(request)
	return render(request, 'accounts/logout.html')


@login_required
def allfiles(request):
	info = Document.objects.filter(username=request.user)
	#files=[]
	#for i in info:
	#	files.append(i)
		#print(reldirname)
	return render(request, 'accounts/allfiles.html',{'info':info})


@login_required
def profile(request):
	info = Document.objects.filter(username=request.user)
	files=[]
	folders=[]
	for i in info:
		if "/" not in i.description :
			files.append(i)
		else:
			reldirname = i.description.split('/')[0]
			if reldirname not in folders:
				folders.append(reldirname)
			#print(reldirname)
	return render(request, 'accounts/profile.html',{'files':files , 'folders':folders, 'paths':''})


@login_required
def profile2(request , paths):
	#print(paths)
	username = request.user
	if paths[0]=='/':
		paths=paths[1:]
	#if paths[-1]=='/' :
		#paths=paths[:-1]
	info = Document.objects.filter(username=request.user).filter(description__startswith=paths)
	#print(paths)
	#print(info)
	files=[]
	folders=[]
	for i in info:
		filepath = str(i.description)

		filepath=filepath.replace(paths,'')
		filepath = filepath[1:]
	#	print(filepath)
		if "/" not in filepath :
			files.append(i)
		else:
			reldirname = filepath.split('/')[0]
			#print(reldirname)
			if reldirname not in folders:
				folders.append(reldirname)

	return render(request, 'accounts/profile2.html',{'files':files , 'folders':folders , 'paths':paths})


def delete(request, file):
	list=Document.objects.filter(id=file)
	list.delete()
	return redirect('profile')



@login_required
@csrf_exempt
def upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			for l in request.FILES.getlist('document'):
				newdoc = Document(document=l, username=request.user, description=form.cleaned_data.get('description'),filename=l.name)
				newdoc.save()
			info = Document.objects.filter(username=request.user)
			return render(request,'accounts/profile.html',{'info' : info})
	else:
		form = DocumentForm()
	return render(request, 'accounts/upload.html', {'form': form})
