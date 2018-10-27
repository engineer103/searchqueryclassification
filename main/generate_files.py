import django
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from main.models import ProcessingQ
from main.classify import classify_search_terms

from django.core.files import File
from datetime import datetime
import sys
import traceback

CF_PATH='/home/jakamkon/webapps/upwork_search_classification_static/media/classification_files'

def run():
    n=datetime.now()
    print('%s:Checking for new files to process...' % str(n))
    processing = ProcessingQ.objects.all().filter(status='processing')
    if len(processing) > 0:
       print('Processing %d jobs, trying later...' % len(processing))
       exit(0)
    to_process = ProcessingQ.objects.all().filter(status='new')
    if len(to_process) > 1:
       to_process=[to_process[0]] 
    for f in to_process:
        inp=f.search_terms_file_paid.search_terms_file.path
        ino=f.search_terms_file_organic.search_terms_file.path
        inn=f.search_terms_file_new.search_terms_file.path
        print(inp)
        outp=os.path.split(inp)
        r,e=os.path.splitext(outp[-1])
        outf=r+'-classified'+e
        outp=os.path.join(CF_PATH,outf)
        print(outp)
        f.status_info='Processing...'
        f.status='processing'
        f.save()
        error=None
        def log_progress(msg):
            f.status_info=msg
            f.save()   
        try:
           # We need to classify organic first
           # since we need to rewrite its stats.
           classify_search_terms([ino,inp,inn],outp,f.dictionary.dictionary_file.path,log_progress)
        except Exception as e: 
           error=str(traceback.format_exc())[-255:]
           f.status='error'
           f.status_info=error
           f.save()
           traceback.print_exc()
        else:
           cf=f.classification_file
           f.classification_file=File(open(outp,'rb'))
           cf.save(outf, open(outp,'rb'))
           f.status='done'
           endn=datetime.now()-n
           f.status_info='Finished without errors,took %s' % str(endn)
           f.save()
      

if __name__ == '__main__':
    run()
