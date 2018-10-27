from django.contrib import admin
from django.http import HttpResponse
from .models import *
from openpyxl import load_workbook,Workbook

# Register your models here.
from .models import SearchTermsFile,Dictionary,ProcessingQ

def load_dict(d="/home/jakamkon/webapps/upwork_search_classification_static/media/dictonaries/Dictonary.xlsx"):
   wb=load_workbook(d)
   ws=wb.active
   st_dict={}
   for r in ws.rows:
       k=r[0].value.lower()
       k=' '.join(k.split())
       st_dict[k]=r[1].value
   return st_dict 

def classify(v, d):
   classes=[]
   v=' '.join(v.lower().split())
   keys=[]
   for k in d:
       ks=k.split()
       # For single words we want to match
       # them using spaces to make sure that
       # we match the whole word.
       if len(ks)==1:
           kl=[' %s ' % k,'%s ' % k,' %s' % k]
           for kk in kl:
              if kk in v:
                  keys.append(k)
                  classes.append(d[k])
       else:
           if k in v:
               keys.append(k)
               classes.append(d[k])
   classes=set(classes)
   keys=set(keys)
   return ' + '.join(list(classes)),','.join(list(keys))

def classify_search_terms(modeladmin, request, queryset):
   f=queryset[0].search_terms_file.path
   #f=open(f, 'rb')
   wb=load_workbook(f)
   ws=wb['data']
   c=ws['B']
   out_wb=Workbook()
   out_ws=out_wb.active
   #raise Exception(out_ws.sheet_state)
   cls_dict=load_dict(queryset[0].dictionary.dictionary_file.path)
   for row in c:
       st=row.value
       clsi,mkeys=classify(st, cls_dict)
       out_ws.append([st, clsi, mkeys])
   #raise Exception([ r.value for r in c])
   outf=f.split('.')[0]+'-classification.xlsx'
   out_wb.save(outf)
   return HttpResponse(open(outf,'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


classify_search_terms.short_description = "Classify search terms"

def process(modeladmin, request, queryset):
   for stf in queryset:
      pq=ProcessingQ.objects.filter(search_terms_file=stf)
      if len(pq) == 0:
         pq=ProcessingQ(search_terms_file=stf, status_info='Just added to the ProcessingQ, waiting for processing...')
         pq.save()
      else:
         pq=pq[0]
         pq.status_info='Just added to the ProcessingQ, waiting for processing...'
         pq.status='new'
         pq.save()
          
process.short_description='Process file (add it to the ProcessingQ)'

class ClassifySearchTermsAdmin(admin.ModelAdmin):
    #actions = [process]
    pass

class PQAdmin(admin.ModelAdmin):
    list_fields = ('search_terms_file_paid','status_info')

admin.site.register(SearchTermsFile,ClassifySearchTermsAdmin)
admin.site.register(ProcessingQ,PQAdmin)
admin.site.register(Dictionary)
