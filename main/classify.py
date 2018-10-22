from openpyxl import load_workbook,Workbook

# Register your models here.
from .models import SearchTermsFile,Dictionary 
from spellchecker import SpellChecker
from textblob import Word
from datetime import datetime
from classify_v2 import classify_kws

def load_dict(d="/home/jakamkon/webapps/upwork_search_classification_static/media/dictonaries/Dictonary.xlsx"):
   wb=load_workbook(d)
   ws=wb.active
   st_dict={}
   for r in ws.rows:
       k=r[0].value.lower()
       k=' '.join(k.split())
       st_dict[k]=r[1].value
   return st_dict 

def classify(v, d,sc=None):
   classes=[]
   kwords=str(v).lower().split()
   if sc:
       skwords=kwords[:]
       for i, kw in enumerate(kwords):
           newkw=Word(kw)
           confidence=0.0
           corrected=None
           for sc in newkw.spellcheck():
              if sc[1] < 0.9:
                 continue
              if sc[1] > confidence:
                 confidence=sc[1]
                 corrected=sc[0]
           if confidence > 0.9:
               kwords[i]=kw
           del skwords
           #misspelled=sc.unknown([kw])
           #if len(misspelled) == 0:
           #   continue
           #else:
           #   kw=sc.correction(kw)
           #   kwords[i]=kw
       #del skwords

   v=' '.join(kwords)
   keys=[]
   # Go trough a dictonary sorted by len
   #dkeys=list(d.keys())
   #dkeys.sort(key=len, reverse=True)
   for k in d: #dkeys:
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
   if len(classes) == 0:
       return 'Unclassified',()
   return ' + '.join(list(classes)),','.join(list(keys))

def classify_search_terms(path,out_path,dict_path, log_progress=print):
   sc=SpellChecker()
   wb=load_workbook(path, read_only=True)
   # Choose the first workbook
   ws=wb.active

   out_wb=Workbook(write_only=True)
   out_ws=out_wb.create_sheet()
 
   cls_dict=load_dict(dict_path)
   i=1
   log_progress('Starting processing rows...')
   for row in ws.rows:
       print(i)
       if i < 3:
          r=row
          if i == 2:
             r=[row[0].value,'Classification']+[ _r.value for _r in row[1:] ]
          else:
             r=[ _r.value for _r in r ]
          #print(i,'Header',r) 
          out_ws.append(r)
          i+=1
          continue
       st=row[0].value
       if st is None:
          st=''
       st=str(st).lower().split(' ')
       #clsi,mkeys=classify(st, cls_dict,None)
       clsi=classify_kws(st, cls_dict)
       mkeys=[]
       newrow=[row[0].value,clsi]+[ _r.value for _r in row[1:] ]
       #print('Body',newrow)
       out_ws.append(newrow)
       if i % 1000 == 0:
           n=datetime.now()
           m='%s:generated %d rows.' % (n,i)
           log_progress(m)
           print(m)

       i+=1
       #print(st, clsi)
   log_progress('Saving output file...')
   out_wb.save(out_path) 
