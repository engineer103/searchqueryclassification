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
    search_terms_file_paid = models.OneToOneField('SearchTermsFile', blank=True, null=True, unique=True,on_delete=models.CASCADE, related_name='search_terms_file_paid')
    search_terms_file_organic = models.OneToOneField('SearchTermsFile', blank=True, null=True, unique=True,on_delete=models.CASCADE, related_name='search_terms_file_organic')
    search_terms_file_new = models.OneToOneField('SearchTermsFile', blank=True, null=True,unique=True,on_delete=models.CASCADE, related_name='search_terms_file_new')
    classification_file = models.FileField(blank=True, null=True, upload_to='classification_files/')
    dictionary = models.ForeignKey(Dictionary,blank=True,null=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, default='new', choices=(('new','new'),('start','start'),('processing','processing'),('done','done'),('error','error')))
    status_info = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True,null=True)

    def __str__(self):
       return self.status_info

class SearchTermsFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    search_terms_file = models.FileField(upload_to='search_terms_file/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    has_been_processed = models.BooleanField(default=False)
    class Meta:
        app_label='main'
    def __str__(self):
       return self.description
