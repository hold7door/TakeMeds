# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from  django.core.exceptions import ObjectDoesNotExist


import MySQLdb
database = MySQLdb.connect(user = os.environ['DB_USER'] , passwd = os.environ['DB_PASS'] , db = os.environ['DB_NAME'])
db = database.cursor()

def search_results(request):
    if (request.method == 'POST'):
        try:
            la = request.session['lat']
            ln = request.session['lon']
        except KeyError:
            return HttpResponse('<script>alert(\'Location Required\');</script>')
        query = request.POST['search_input']
        db.execute("""Select * from generic_medicine where locate(%s,name) > 0""" , (query,))
        in_generic = db.fetchall()
        db.execute("""Select * from brand_medicine where locate(%s,name) > 0""",(query,))
        in_brand = db.fetchall()
        if len(in_generic) > 0:  # search For Generic Form
            medicine_name_generic = in_generic[0][0]
            medicine_id = in_generic[0][2]
            query_type = "Generic"
            print (query_type)
            return search(medicine_id,request,la,ln)
        elif len(in_brand):  # Search is brand Form
            medicine_name_brand = in_brand[0][0]
            medicine_id = in_brand[0][2]
            query_type = "Brand"
            print (query_type)
            db.execute("""Select g_id from brand_medicine where b_id = %s""",(medicine_id,))
            medicine_gen_id = db.fetchall()[0][0]
            return search(medicine_gen_id,request,la,ln)
        else: # medicine not found
            context = {'query': request.POST['search_input'] , 'user': request.user}
            return render(request , "places/med_not_found.html" , context=context)
    else:
        return HttpResponse("Query Not Found.")
def search(di,request,la,ln):
    db.execute("""select * from store_to_generic where g_id = %s""" , (di,))
    res = db.fetchall()
    if len(res): # store found for the searched generic medicine
        stores_avail_id = [i[0] for i in res ]
        db.execute("""Select a.name,a.address,a.store_id,a.rating,round((6371*acos(cos(radians(%s))*cos(radians(a.lat))*cos(radians(a.lng)-radians(%s))+sin(radians(%s))*sin(radians(a.lat)))),3) as distance from all_stores a where a.store_id in %s having distance<20 order by distance""" ,(la,ln,la,stores_avail_id,))    #Haversine Formula Used
        stores_avail = list(db.fetchall())  #Stores with both brand and generic type
        stores_avail = [list(i) for i in stores_avail]
        address = [k[1][:k[1].find(' India')] for k in stores_avail]
        address_format = [i.split(',') for i in address]   
        fl = 0
        for m in stores_avail:      #Address Field split into list   
            m[1] = address_format[fl]
            fl+=1
        db.execute("""Select * from brand_medicine where g_id = %s""",(di,))
        brand_types = list(db.fetchall())
        stores_with_brand = {}
        id_stores_with_brand = []
        if len(brand_types):
            brand_ids = tuple([i[2] for i in brand_types])
            db.execute("""Select b.store_id,b.b_id,round((6371*acos(cos(radians(%s))*cos(radians(a.lat))*cos(radians(a.lng)-radians(%s))+sin(radians(%s))*sin(radians(a.lat)))),3) as distance from brand_store b inner join all_stores a on a.store_id = b.store_id where b.b_id in %s having distance<20 order by distance """ , (la,ln,la,brand_ids,))
            result = list(db.fetchall())
            for st,b,distance in result:
                db.execute("""Select b.name from brand_medicine b where b_id = %s""",(b,))
                n = db.fetchall()
                if st not in stores_with_brand:
                    stores_with_brand[st] = [n[0][0]]
                    id_stores_with_brand.append(st)
                else:
                    stores_with_brand[st].append(n[0][0])
        context = {'stores_avail': stores_avail ,'stores_avail_id':stores_avail_id ,'stores_with_brand':stores_with_brand ,'id_stores_with_brand':id_stores_with_brand ,'user':request.user}
        return render(request , 'places/results.html' ,context=context)
    else:
        context = {'query': request.POST['search_input'],'user':request.user}
        return render(request , 'places/store_not_found.html' , context=context)

