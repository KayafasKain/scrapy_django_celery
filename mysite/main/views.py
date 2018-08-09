from .forms import IndexForm
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
import redis
from django.conf import settings
import pymongo
connection = pymongo.MongoClient(settings.MONGO_SERVER, settings.MONGO_PORT)
redis_server = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)


class Index(FormView):
    template_name = 'main/index.html'
    form_class = IndexForm
    context_object_name = 'main_page'

    def form_valid(self, form):
        redis_server.lpush('aizel:start_urls', form.cleaned_data['link'])
        return HttpResponseRedirect(reverse('items-list'))

index_view = Index.as_view()

class ItemsList(ListView):
    template_name = 'main/items_list.html'
    context_object_name = 'items-list'
    #paginate_by = 10

    def get_queryset(self):
        db = connection[settings.MONGO_DB_NAME]
        db.authenticate(settings.MONGO_USER_NAME, settings.MONGO_USER_PASSWORD)
        return db.scrapped_goods.find({}).sort([('_id', pymongo.DESCENDING)])

items_list = ItemsList.as_view()