
def perm(n, kw):
    if n>=len(kw):
           return [kw], [ i for i in range(0, len(kw)) ]
    perms=[]
    permi=[]
    # Going trough keywords
    for i in range(0, len(kw)):
           print(i, kw[i])
           ps=[]
           pi=[]
           ps.append(kw[i])
           pi.append(i)
           for ii in range(0, n-1):
              if i+ii+1>len(kw)-1:
                 continue
              print(' ',ii, kw[i+ii+1])
              ps.append(kw[i+ii+1])
              pi.append(i+ii+1)
           if len(ps) < n:
              continue
           perms.append(ps)
           permi.append(pi)
    return perms, permi

def match(sc, d):
     ds=list(d.keys())
     ds.sort(key=len, reverse=True)
     if sc in d:
        return d[sc]
     return None


def classify_kws(kws, kwd):
   kwss=kws[:]
   cls=[]
   cls_kws=[]
   clsi=[]
   if len(kws) == 1:
      c=match(' '.join(kws), kwd)
      if c:
         return c,'full'
      else:
         return 'Unclassified','unclassified'
   for i in reversed(range(1, len(kwss)+1)):
       print('kw=',i)
       p, pi=perm(i, kwss)
       print(p, pi)
       for j, kw in enumerate(p):
           c=match(' '.join(kw), kwd)
           if c:
               print('Match',kw)
               cls.append(c)
               cls_kws.append(' '.join(kw))
               clsi.append(pi[j])
               print('X',kwss,kw)
               del kwss[kwss.index(kw[0]):kwss.index(kw[-1])]
   print('Results:')
   print('No match:',kwss)
   print('Classes:',cls)
   print('KWS match:',cls_kws)
   tof_match=None
   if len(cls) == 0:
      print('Final:')
      print('Unclassified (no match)')
      return 'Unclassified', 'unclassified'
   print(clsi)
   clsss_kws=' '.join(kws)
   clsss=' '.join(kws)
   for i, c in enumerate(cls_kws):
      newc=None
      for p in [' %s ',' %s', '%s ']:
         pi=clsss_kws.find(p % c)
         if pi == -1:
            continue
         # pqrt of the end of the word
         if p == '%s ' and pi != 0:
            continue
         # part of the beginning of the word
         if p == ' %s' and pi+len(p % c) < len(clsss_kws):
            continue
         if pi != -1:
            newc=p % c
            break
      if newc:
         clsss=clsss.replace(newc, ' '+cls[i]+' ')
      print(c, cls[i], clsss)
   # Start from the longest
   kwss.sort(key=len, reverse=True)
   for i, c in enumerate(kwss):
      newc=None
      for p in [' %s ',' %s', '%s ']:
         pi=clsss_kws.find(p % c)
         if pi == -1:
            continue
         # pqrt of the end of the word
         if p == '%s ' and pi != 0:
            print('EOW skip', pi, p % c)
            continue
         # part of the beginning of the word
         if p == ' %s' and pi+len(p % c) < len(clsss_kws):
            continue
         if pi != -1:
            newc=p % c
      if newc:
         clsss=clsss.replace(newc, ' Unclassified ')
         print(c, 'Unclassified',clsss)
   print('Final')
   # When we left some keywords behind
   # just make them unclassified.
   for k in kwss:
       if clsss.find(k) != -1:
           print('Unmatched kw %s -> Unclassfied' % k)
           clsss.replace(k,'Unclassified')
   # Remove duplicates
   while clsss.find('Unclassified Unclassified') != -1:
       clsss=clsss.replace('Unclassified Unclassified','Unclassified')
   clsss=' '.join(clsss.split()).replace(' ',' + ')
   tom='unclassified'
   cf=clsss.find('Unclassified')
   if cf == -1:
       tom='full'
   elif cf != -1:
       tom='partial'
   return clsss, tom

if __name__ == '__main__':
   kws=['best','royal','swimming','pools','kona', 'hawaii']
   kwd1={'best': 'Test',
        'royal swimming pools':'ProductType',
        'hawaii': 'State'}
   classify_kws(kws, kwd1)
   kws="inground pool sale 12 24"
   kwd2={'sale':'PriceSearch', 'inground pool': 'ProductType'}
   classify_kws(kws.split(' '), kwd2)
   # 
   kws="inground pool sale 12 24"
   kwd3={'sale':'PriceSearch', 'inground pool sale': 'ProductType'}
   classify_kws(kws.split(' '), kwd3)
   
   kws="on ground pools in hudson valley"
   kwd4={'pools':'ProductType'} 
   classify_kws(kws.split(' '), kwd4)
  
   kws="sleds snow tubes snow tubes"
   classify_kws(kws.split(' '), {})
   
   kws="water tubes for winter pool cover for use with in ground pools 4 pack of 8 ft double chamber water tubes"
   classify_kws(kws.split(' '), {}) 

