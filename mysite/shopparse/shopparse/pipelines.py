# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#need to import django settings
#sys.path.append(os.path.join(base_dir, 'web'))
#os.environ['dkango_settings_module'] = 'web.settings.django.setup()'

#better - use celary,transimt item as a task, and then create

#inside django
#class BaseView(View):
    #def post(self, result):
        #spider_name =result.POST['spider']
        #scr-redis.lpush('spider_name:start_url target_site')

#!!! need to be placed inside django app

from __future__ import absolute_import
from scrapy.utils.serialize import ScrapyJSONEncoder
_encoder = ScrapyJSONEncoder()

from main.tasks import added_item



class ShopParsePipeline(object):
    def process_item(self, item, spider):
        added_item.delay(_encoder.encode(item))
        return item
