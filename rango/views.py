from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse;
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm
from django.shortcuts import redirect
from django.urls import reverse

def index(request):
    #Get the first 5 categories orderd by likes in desc order
    #- in "-likes" indicates desc order
    category_list = Category.objects.order_by("-likes")[:5]
    pages = Page.objects.order_by("-views")[:5]
    context_dict = {}
    context_dict["boldmessage"] = "Crunchy, creamy, cookie, candy, cupcake!"
    context_dict["categories"] = category_list
    context_dict["pages"] = pages

    return render(request,"rango/index.html",context=context_dict)

def about(request):
    context_dict = {"MEDIA_URL": settings.MEDIA_URL}
    return render(request,"rango/about.html",context=context_dict)

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        #Try getting the categories using its the slug parameter given in url
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict["pages"] = pages
        context_dict["category"] = category
    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request,"rango/category.html",context=context_dict)


def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/rango/")
        else:
            print(form.errors)
    return render(request,"rango/add_category.html",{"form": form})


def add_page(request,category_name_slug):
    print("did work")
    #try to get the category this page should belong to
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    #handle invalid category 
    if category is None:
        return redirect("/rango/")
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse("rango:show_category",kwargs={"category_name_slug": category_name_slug}))
        else:
            print(form.errors)
    context_dict = {"form": form,"category":category}
    return render(request,"rango/add_page.html",context=context_dict)