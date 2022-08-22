from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import AppForm
from django.contrib.auth.decorators import login_required
#from .formsets import AppFormset
from .models import AppModel, Issues, AppStats, Comments, Rating
from django.db.models import Sum

# Create your views here.


@login_required
def app_form(request):
    
    if request.method == 'POST':
     
        form = AppForm(request.POST, request.FILES)
        print(form.errors)

        if form.is_valid():
            form.save()
            print("VALID")
        

    form = AppForm()
    return render(request, 'apps/app_upload.html', {'form':form})




def apps_and_comments(request):

    rating_obj = Rating.objects.all()
    avg_rating = Rating.objects.aggregate(total_rating=Sum('rating'))
    avgr = avg_rating['total_rating'] / 2


    return {'context_appmodel': AppModel.objects.all(),
            'context_comments': Comments.objects.all(),
            'context_rating': avgr}


class AppView(DetailView):
    model = AppModel
    model_comments = Comments
    template_name = 'apps/app_page.html'
    context_object_name = 'apps'
    slug_url_kwarg = 'slug'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['issues'] = Issues.objects.all()
        context['stats'] = AppStats.objects.all()
        context['comments'] = Comments.objects.all()
        return context




class AppListView(ListView):
    model = AppModel
    template_name = 'apps/homepage.html'
    context_object_name= 'apps_list'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        app_data = self.model.objects.all()
        return app_data


def SearchList(request):
    if request.method == 'GET':
        search_text = request.GET.get('search')

        mydata = AppModel.objects.filter(appname__contains=search_text).values() 

        if mydata.exists():
            return render(request, 'apps/tools/searchlist.html', {'result':mydata})
        else: return render(request, 'apps/tool/searchlist.html', {'result':'not searching'})




