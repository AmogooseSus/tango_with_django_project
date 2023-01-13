import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","tango_with_django_project.settings")

import django
django.setup()
from rango.models import Category,Page

def populate():
    #List of pages
    python_pages = [ {"title": "Official Python Tutorial", "url": "http://docs.python.org/3/tutorial/", "views": 20},
        {"title": "How to Think like a Computer Scientist", "url": "http://www.greenteapress.com/thinkpython/", "views":16},
        {"title": "Learn Python in 10 Minutes", "url": "http://www.korokithakis.net/tutorials/python/", "views":19}, 
    ]

    django_pages = [        {"title": "Official Django Tutorial","url": "https://docs.djangoproject.com/en/2.1/intro/tutorial01/", "views":5},
        {"title": "Django Rocks","url": "http://www.djangorocks.com/", "views":7},
        {"title": "How to Tango with Django", "url": "http://www.tangowithdjango.com/", "views":18}]

    other_pages = [{"title": "Bottle","url": "http://bottlepy.org/docs/dev/", "views":5}, {"title": "Flask","url":"http://flask.pocoo.org", "views":17}]

    #Dict mapping categories to list of pages
    categories = {"Python": {"pages": python_pages,"views":128,"likes":64},
                "Django": {"pages": django_pages,"views":64,"likes":32},
                "Other Frameworks": {"pages": other_pages,"views":32,"likes":16}
    }

    #Iterates through each category and adds it to the categories table
    #And for each Categories it addes the associated pages to the Page table
    for categ,categ_data in categories.items():
        c = add_categ(categ,categ_data["views"],categ_data["likes"])
        for p in categ_data["pages"]:
            add_page(c,p["title"],p["url"],p["views"])
            #print out each page we have added and its associated category
            print(f"-{c}: {p}") 



def add_page(categ,title,url,views):
        p = Page.objects.get_or_create(category=categ,title=title)[0]
        p.url=url
        p.views=views
        p.save()
        return p

def add_categ(name,views,likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c
    

if __name__ == "__main__":
    print("Starting Rango population script....")
    populate()


