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

class SearchDictionary(models.Model):
    name = models.CharField(max_length=255, blank=True)
    attribute = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_dictionary"

class SearchPortfolio(models.Model):
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_portfolio"
    def __str__(self):
       return str(self.name)

class SearchTerm(models.Model):
    query = models.CharField(max_length=510, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    impressions = models.IntegerField(null=True, blank=True)
    avg_position = models.FloatField(null=True, blank=True)
    cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    conversions = models.FloatField(null=True, blank=True)
    total_conv = models.FloatField(null=True, blank=True)
    search_portfolio = models.ForeignKey(SearchPortfolio, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_term"

class SearchClassification(models.Model):
    query = models.CharField(max_length=16320, blank=True)
    search_dictionary_ids = models.CharField(max_length=16320, blank=True)
    portfolio_ids = models.CharField(max_length=255, blank=True)
    paid_impressions = models.IntegerField(null=True, blank=True)
    paid_clicks = models.IntegerField(null=True, blank=True)
    paid_cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    paid_conversions = models.FloatField(null=True, blank=True)
    paid_total_conv = models.FloatField(null=True, blank=True)
    organic_clicks = models.IntegerField(null=True, blank=True)
    organic_impressions = models.IntegerField(null=True, blank=True)
    organic_avg_position = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_classification"


class SearchMatchTotal(models.Model):
    full = models.FloatField(null=True, blank=True)
    partial = models.FloatField(null=True, blank=True)
    unclassified = models.FloatField(null=True, blank=True)
    unclassified_partial = models.IntegerField(null=True, blank=True)
    partial_full = models.IntegerField(null=True, blank=True)
    unclassified_full = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "search_match_total"

class SearchMatch(models.Model):
    full = models.FloatField(null=True, blank=True)
    partial = models.FloatField(null=True, blank=True)
    unclassified = models.FloatField(null=True, blank=True)
    search_portfolio = models.ForeignKey(SearchPortfolio, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "search_match"