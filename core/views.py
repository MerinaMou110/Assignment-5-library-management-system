from django.shortcuts import render
from django.views.generic import TemplateView
from Library.models import Book
from category.models import Category

# Create your views here.
# class HomeView(TemplateView):
#     template_name = 'index.html'

def home(request, category_slug = None): # initially dhore nicchi je category_slug None thakbe karon hocche user first time home page e asle se normal page dekhbe, se filter korte chaile category te click korlei sei category er slug ta capture korbo ar seta tokhn ar None thakbe na
    
    data = Book.objects.all() # sob post gula ke niye aslam
    if category_slug is not None: # ekhn category slug jodi None na hoy tar mane sekhane value ache
        category = Category.objects.get(slug = category_slug) # slug je field model e likhechilam seta = amader category slug kore dilam taile ekhn kon category er slug sei category object peye jabo
        data = Book.objects.filter(category  = category) # post er category te category object bosiye filter korlam, ager data er sathe overright hoye jabe
    categories = Category.objects.all() # sob category dekhabo
    return render(request, 'index.html', {'data' : data, 'category' : categories})