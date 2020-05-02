# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from math import acos, cos, radians, sin


from  django.core.exceptions import ObjectDoesNotExist


import MySQLdb
database = MySQLdb.connect(user = os.environ['DB_USER'] , passwd = os.environ['DB_PASS'] , db = os.environ['DB_NAME'])
db = database.cursor()

class Store:
    def __init__(self, store_id, name, rating, lat, lng, distance):
        self.id = store_id
        self.name = name
        self.address = []
        self.rating = rating
        self.lat = lat
        self.lng = lng
        self.medicine_in_store = []
        self.distance = distance
    def set_address(self, full_add):
        for line in full_add.split(', '):
           self.address.append(line)
    def add_medicine(self, medicine_name):
        self.medicine_in_store.append(medicine_name)


def apply_haversine(results, la, ln):
    filtered = []
    for r in results:
        rla = radians(float(la))
        rln = radians(float(ln))
        rsla = radians(float(r[4]))
        rsln = radians(float(r[5]))
        #print(la, ln, rla, rln, r[4], r[5], rsla, rsln)
        value = (6371 * acos(cos(rla) * cos(rsla) * cos(rsln-rln) + sin(rla) * sin(rsla)))
        #print(value)
        if value < 115:
            filtered.append((r, round(value, 2)))
    return filtered

def create_obj(results):
    final = {}
    for r, distance in results:
        print(r, distance)
        if r[0] not in final:
            st = Store(r[0], r[1], r[3], r[4], r[5], distance)
            st.set_address(r[2])
            st.add_medicine(r[7])
            final[r[0]] = st
        else:
            final[r[0]].add_medicine(r[7])

    return final.values()




# Process Request and find whether search is of type Generic or Brand and find generic id of drug 
def search_results(request):
    if (request.method == 'POST'):
        try:
            la = request.session['lat']
            ln = request.session['lon']
        except KeyError:
            return HttpResponse('<script>alert(\'Location Required\');</script>')
        query = request.POST['search_input']

        #Find medicine in Generic Table
        db.execute("""Select * from generic_medicine where locate(%s,name) > 0""" , (query,))
        in_generic = db.fetchall()

        # Find medicine in Brand Table
        db.execute("""Select * from brand_medicine where locate(%s,name) > 0""",(query,))
        in_brand = db.fetchall()

        if len(in_generic) > 0:  # search is for Generic name
            #medicine_name_generic = in_generic[0][0]
            medicine_id = in_generic[0][2]
            #query_type = "Generic Name"
            #print (query_type)
            return search(medicine_id,request,la,ln)
        elif len(in_brand):  # Search is for brand name
            #medicine_name_brand = in_brand[0][0]
            medicine_id = in_brand[0][2]
            #query_type = "Brand Name"
            #print (query_type)
            # Select Generic Id of brand medicine
            db.execute("""Select g_id from brand_medicine where b_id = %s""",(medicine_id,))
            medicine_generic_id = db.fetchall()[0][1]
            return search(medicine_generic_id,request,la,ln)
        else: # Search Result Empty
            context = {'query': request.POST['search_input'] , 'user': request.user}
            return render(request , "places/med_not_found.html" , context=context)
    else:
        return HttpResponse("Query Not Found.")


def search(di,request,la,ln):
    
    
    db.execute("""select als.store_id, als.name as StoreName, als.address as Address, als.rating as Rating, als.lat as LAT,  als.lng as
        LNG, store_medicine.g_id as MedicineID, store_medicine.name as MedicineName from all_stores als 

        inner join

        (
            select sg.store_id, ifnull(sb.g_id, sg.g_id) as g_id, ifnull(sb.name, sg.name) as name 

        from 

        (select stg.store_id, stg.g_id, gm.name from store_to_generic stg inner join generic_medicine gm on gm.g_id = stg.g_id where gm.g_id = %s) sg

        left join 

        (select bs.store_id, bs.b_id, bm.name, bm.g_id from brand_store bs inner join brand_medicine bm on bs.b_id = bm.b_id where bm.g_id = %s) sb 

        on sg.store_id = sb.store_id

        ) store_medicine

        on als.store_id = store_medicine.store_id order by als.rating desc""" , (di, di))



    results = db.fetchall()

    if len(results): # store found for the searched generic medicine
        nearest_stores = apply_haversine(results, la, ln)
        #print(nearest_stores)
        stores_available = create_obj(nearest_stores)
        #print([s.medicine_in_store for s in stores_available])

        context = {'stores_available': stores_available , 'user':request.user}
        return render(request , 'places/results.html' ,context=context)
    else:
        context = {'query': request.POST['search_input'],'user':request.user}
        return render(request , 'places/store_not_found.html' , context=context)

