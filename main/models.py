from django.db import models

# Create your models here.
from django.db import models

class Dictionary(models.Model):
    description = models.CharField(max_length=255, blank=True)
    dictionary_file = models.FileField(upload_to='dictonaries/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label='main'
        verbose_name_plural='dictionaries'
    def __str__(self):
       return str(self.dictionary_file)
	
class ProcessingQ(models.Model):
    search_terms_file = models.OneToOneField('SearchTermsFile', unique=True,on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='new', choices=(('new','new'),('start','start'),('processing','processing'),('done','done'),('error','error')))
    status_info = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True,null=True)

    def __str__(self):
       return str(self.search_terms_file)+' '+self.status_info

class SearchTermsFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    search_terms_file = models.FileField(upload_to='search_terms_file/')
    classification_file = models.FileField(blank=True, null=True, upload_to='classification_files/')
    dictionary = models.ForeignKey(Dictionary,blank=True,null=True,on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    has_been_processed = models.BooleanField(default=False)
    class Meta:
        app_label='main'
    def __str__(self):
       status=''
       pq=ProcessingQ.objects.filter(search_terms_file=self)
       if len(pq) == 0:
          status='Add it to the ProcessingQ to process'
       else:
          status=pq[0].status_info
       return self.description+'   |   '+str(self.search_terms_file)+'   |   Status:'+status
