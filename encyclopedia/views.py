from django.conf.urls import handler400
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import widgets
from django.forms.fields import CharField

from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from . import util
import re
import random
import markdown2


#making form for index page
class search_form(forms.Form):
    q=forms.CharField(widget=forms.TextInput(attrs={"class":"search","placeholder":"Search Encyclopedia" ,"autocomplete":"off"}),label="")

#making form for create page 
class create_form(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control title","placeholder":"Enter the title","autofocus":"","autocomplete":"off"}))
    data=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control content","placeholder":"Enter the content"}))

#making form for edit page
class edit_form(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control title"}))
    data=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control content"}))


#function for index page
def index(request):

    #when we submit a form we will enter post method

    if request.method=="POST":
        
        form=search_form(request.POST)
         
        # checking is form valid or not 
        if form.is_valid():

            query=form.cleaned_data["q"]

            #if user typed a query thats not in our db then we will look for words similar like that
            if util.get_entry(query)==None:
    
                #iterating list of enteries in our db and then looking if it conatins any sub string or not in our list string
                #use lower function so that case senssitiveness doesnt matter
                res = [x for x in util.list_entries() if re.search(query, x.lower())]
            
                #checking if our res varaiable contains any items or not that we got from parsing the list in our db
                if len(res)==0:
                    return render(request,"encyclopedia/error.html",{
                        "title":query,
                        })
                # and we got some item in a list then sending it to a new page called search.html
                else:
                    return render(request,"encyclopedia/search.html",{
                        "list":res,
                        "count":len(res),
                        "search_form":search_form()
                    })
            return HttpResponseRedirect(reverse('content', args=[query]))

    # if user  just views the page we renders index page 
    return render(request, "encyclopedia/index.html", {
        "search_form":search_form(),
        "entries": util.list_entries()
    })


# function for route of any title you are searching
def content(request,title):

    #if the user typed any title thats not availiable than we will show error page
    if util.get_entry(title)==None:
        return render(request,"encyclopedia/error.html",{
            "title":title,
        })

    # we will return content by using get_entry function in util.py files 
    # and we are also converting markdown language into html language
    return render(request,"encyclopedia/content.html",{
        "content":markdown2.markdown(util.get_entry(title)),
        "title":title,
        "search_form":search_form()
    })


# function for create html page
def create(request):
    #using bool to pass message later on wether the title they are using availiable or not 
    valid=True
    if request.method=="POST":
        
        form=create_form(request.POST)
        # checking if the form is valid or not 
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["data"]
            
            #checking if  title is already in our entry list or not 
            if util.get_entry(title)!=None:
                valid=False
                # returnining user to createpage with message to change title 
                return render(request,"encyclopedia/createpage.html",{
                    "form":create_form(),
                    "valid":valid,
                    "search_form":search_form()
                })
            # else saving the entry to db
            util.save_entry(title,content)
            # after saving entry redirecting user to content page for that entry 
            return HttpResponseRedirect(reverse('content',args=[title]))
    # sending form, valid bool to createpage on get request 
    return render(request,"encyclopedia/createpage.html",{
        "form":create_form(),
        "valid":valid,
        "search_form":search_form()
    })
def edit(request,title):
    #using bool to pass message later on weather the edited file is sucessfully saved or not
    is_submitted=False
    
    if request.method=="POST":
        
        form=edit_form(request.POST)
        # checking if form is valid or not 
        if form.is_valid():
            
            heading=form.cleaned_data["title"]
            data=form.cleaned_data["data"]
            
            #if user chnages title 
            if heading!=title:
                #deleting the entry with current title 
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
                    

            # and saving entry with new title and content 
            util.save_entry(heading,data)
            #  changing bool to true 
            is_submitted=True
            # on sucessful edit sending user to the edited content page 
            # converting markdown to html too 
            return render(request,"encyclopedia/content.html",{
                "title":heading,
                "content":markdown2.markdown(util.get_entry(heading)),
                "search_form":search_form(),
                "is_submitted":is_submitted,

            })
    
    # if user views page with get request
    # storing data and then providing it to forms as we have to pre-populate the form with the previous content
    data=util.get_entry(title)
    form=edit_form(initial={"title":title,"data":data})
    return render(request,"encyclopedia/edit.html",{
        "form":form,
        "title":title,
        "search_form":search_form()
    })
# function for random button 
def random_page(request):
    # getting all entries in our list
    link= util.list_entries()
    # using random function to genrate a number between 0 to length of (list-1) as in list we start index from 0 not 1
    index=random.randint(0,len(link)-1)
    #redirecting user to content page. By using link[index] we are randomly generating any item in a list
    return HttpResponseRedirect(reverse("content",args=[link[index]]))
