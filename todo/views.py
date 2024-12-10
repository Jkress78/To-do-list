from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .form import *
from users.forms import EditUserForm
import os
from .models import UserImg, List, ListItem

# Create your views here.
def listSelect(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ListForm(request.POST, request.FILES)
            if form.is_valid():
                new_list = form.save(commit=False)
                new_list.user = request.user
                new_list.create_date = timezone.now()
                new_list.save()
                return redirect("todo:listSelect")
        else:
            form = ListForm()

        return render(request, "todo/dashboard.html", {'user': request.user, 'form': form})

    else:
        return redirect('users:login')

# View for when a user creates a new List
def listCreate(request):
    if request.user.is_authenticated:
        

        if request.method == "POST":
            form = ListForm(request.POST, request.FILES)

            if form.is_valid():
                new_list = form.save(commit=False)
                new_list.user = request.user
                new_list.create_date = timezone.now()
                new_list.save()
                return redirect("todo:listSelect")
        else:
            form = ListForm()

        return render(request, "todo/createList.html", {"form": form})
    
    else:
        return redirect('users:login')
    
def deleteList(request, list_id):
    if request.user.is_authenticated:
        try:
            listt = List.objects.get(pk=list_id)
            if listt.user == request.user:
                os.remove(listt.cover_img.path)
                listt.delete()
                return redirect('todo:listSelect')
            else:
                return redirect('todo:listSelect')
        
        except ObjectDoesNotExist:
            return redirect('todo:listSelect')

    else:
        return redirect('users:login')
    

def editList(request, list_id):
    if request.user.is_authenticated:
        listt = List.objects.get(pk=list_id)
        img = listt.cover_img.path
        
        if request.method == "POST":
            form = ListForm(request.POST, request.FILES, instance=listt)

            if form.is_valid():
                try:
                    os.remove(img)
                    form.save()
                
                except FileNotFoundError:
                    form.save()

            return redirect('todo:listSelect')
        
        else:
            form = ListForm(instance=listt)

        return render(request, 'todo/editList.html', {'form': form, 'list': listt})
        
    else:
        return redirect('users:login')
    


def listDetails(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            listt = get_object_or_404(List, pk=request.POST['list_id'])
        else:
            listt = get_object_or_404(List, pk=request.session['list_id'])
        return render(request, "todo/itemView.html", {"list":listt})
    else:
        return redirect('users:login')

def createItem(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            #make sure empty items are not added
            if request.POST["item_txt"] == "":
                return redirect('todo:listDetails')
            else:
                listt = List.objects.get(pk=request.POST["list_id"])
                new_item = ListItem.objects.create(item_list=listt, item_text=request.POST["item_txt"], add_date=timezone.now())
                new_item.save()
                request.session["list_id"] = request.POST["list_id"]
                return redirect('todo:listDetails')
        else:
            return redirect('todo:listSelect')
    else:
        return redirect('users:login')
    
    
def updateItem(request, item_id):
    if request.user.is_authenticated:
        try:
            item = ListItem.objects.get(pk=item_id)
            if item.is_complete:
                item.is_complete = False
            else:
                item.is_complete = True

            item.save()
            return redirect('todo:listDetails')
        except ObjectDoesNotExist:
            return redirect('todo:listSelect')

    
    else:
        return redirect('users:login')
    

def deleteItem(request, item_id):
    if request.user.is_authenticated:
        try:
            item = ListItem.objects.get(pk=item_id)
            if item.item_list.user == request.user:
                listt = item.item_list
                item.delete()
                request.session["list_id"] = listt.id
                return redirect('todo:listDetails')
            else:
                return redirect('todo:listSelect')
        
        except ObjectDoesNotExist:
            return redirect('todo:listSelect')

    else:
        return redirect('users:login')
    

def userDetails(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditUserForm(request.POST, instance=request.user)

            if form.is_valid():

                form.save()
                if request.FILES:
                    try:
                        img = UserImg.objects.get(user=request.user.id)
                        os.remove(img.prof_img.path)
                        img.delete()
                        UserImg.objects.create(user=request.user, prof_img=request.FILES["prof_img"])

                    except FileNotFoundError:
                        img.delete()
                        UserImg.objects.create(user=request.user, prof_img=request.FILES["prof_img"])
                    
                    except ObjectDoesNotExist:
                        UserImg.objects.create(user=request.user, prof_img=request.FILES["prof_img"])
                   

            return redirect('todo:userDetails')
        
        else:
            form = EditUserForm(instance=request.user)

        
        return render(request, "todo/userProfile.html", {'user': request.user, 'form': form})
    else:
        return redirect('users:login')
