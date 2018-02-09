from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm


# main page view:
def index(request):
    # Construct a dictionary to pass to the template engine as its context
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    # return a rendered response to send to the client
    # first param is the template we wish to use
    return render(request, 'rango/index.html', context_dict)


def about(request):
    # return HttpResponse("Rango says here is the about page <br/>"
    #                    "<a href='/rango/'>Index</a>")
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    # a HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # id provided form valid?
        if form.is_valid():
            # save the new category to the database
            cat = form.save(commit=True)

            return index(request)
        else:
            # the form was invalid
            # print error message
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist():
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
