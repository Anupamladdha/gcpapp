from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView,FormView,View,DeleteView
from django.urls import reverse,reverse_lazy
from .models import Room, Booking,Contact,Event
from .forms import AvailabilityForm,PlacesForm
from hotel.booking_functions.availability import check_availability
from hotel.booking_functions.get_room_cat_url_list import get_room_cat_url_list
from hotel.booking_functions.get_room_category_human_format import get_room_category_human_format
from hotel.booking_functions.get_available_rooms import get_available_rooms
from hotel.booking_functions.book_room import book_room
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import math
import math
from hotel.booking_functions import util
import time
from  hotel.booking_functions import tsp_bb
from  hotel.booking_functions import test
# from . import demods.csv
# Create your views here.


def RoomListView(request):
    get_room_category_url_list=get_room_cat_url_list()
    context={
        "room_list":get_room_category_url_list,
    }
    # print(context["room_list"])
    return render(request,'room_list_view.html',context)

def EventBookView(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone') 
        eventtype=request.POST.get('eventtype') 
        eventdate=request.POST.get('eventdate') 
        desc=request.POST.get('desc') 
        event=Event(name=name,email=email,phone=phone,eventtype=eventtype,eventdate=eventdate,desc=desc,date=datetime.today())
        event.save()
        messages.success(request, 'Your message has been sent')
    return render(request,'event_book_view.html')

def base(request):
    return render(request,'base.html')

def places(request):
    if request.method == "POST":
        # print("sjjkdas hdbkasjhmdsh")
        form = PlacesForm(request.POST)
        if form.is_valid():
            # print("-----------")
            numberofdays = form.cleaned_data['numberofdays']
            place1 = form.cleaned_data["place1"]
            place2 = form.cleaned_data["place2"]
            place3 = form.cleaned_data["place3"]
            place4 = form.cleaned_data["place4"]    
            place5 = form.cleaned_data["place5"]
            place6 = form.cleaned_data["place6"]
            place7 = form.cleaned_data["place7"]
            place8 = form.cleaned_data["place8"]
            place9 = form.cleaned_data["place9"]
            place10 = form.cleaned_data["place10"]
            place11 = form.cleaned_data["place11"]
            place12 = form.cleaned_data["place12"]
            place13 = form.cleaned_data["place13"]
            place14 = form.cleaned_data["place14"]
            place15 = form.cleaned_data["place15"]
            place16 = form.cleaned_data["place16"]
            place17 = form.cleaned_data["place17"]
            place18 = form.cleaned_data["place18"]
            place19 = form.cleaned_data["place19"]
            place20 = form.cleaned_data["place20"]
            place21 = form.cleaned_data["place21"]
            placeslist=[place1,place2,place3,place4,place5,place6,place7,place8,place9,place10,place11,place12,place13,place14,place15,place16,place17,place18,place19,place20,place21]
            noofplaces=0
            for place in placeslist:
                if(place):
                    noofplaces+=1
            if (noofplaces<numberofdays):
                context={
                }
                context["error"]=True
                context["errormsg"]="Number of Days should be less than number of places selected"
                return render(request,'places.html',context)
            else:
                dataset = pd.read_csv(r"C:\Users\anupa\Desktop\Hotel_Booking_website\Hotel_Booking_Website-main\hotel\templates\demods.csv")
                inputdf = pd.DataFrame(columns=['Name','Latitude','Longitude'])
                for i in range(0,21):
                    if(placeslist[i]):
                        inputdf = inputdf.append(dataset.iloc[i],ignore_index=True)
                
                print('----INPUT DF-----')
                print(inputdf)
                print('---------')
                places_lat_long = inputdf[['Latitude', 'Longitude']].values.tolist()
                kmeans = KMeans(n_clusters=int(numberofdays), random_state=0).fit(places_lat_long)
                group = list(kmeans.labels_)
                inputdf['cluster'] = pd.Series(group, index=inputdf.index)
                inputdf = inputdf.sort_values(by="cluster")
                inputdf.rename(columns={'cluster': 'Day'}, inplace=True)
                inputdf['Day'] += 1
                df_list = list()
                
                for i in range(1, int(numberofdays)+1):
                    df_list.append(inputdf[inputdf['Day'] == i][['Name', 'Latitude', 'Longitude']])
                f_pos = list()
                print('----CLUSTER DF-----')
                print(inputdf)
                print('---------')
                for day_df in df_list:
                    # print(day_df)
                    pos = list()
                    for x in day_df.iterrows():
                        pos.append(list([x[1][1], x[1][2]]))
                    f_pos.append(pos)

                k = len(f_pos)
                # hotel's lat and long
                start_lat, start_lng = 29.478502880470412, 79.1495345337684

                for days in f_pos:
                    days.insert(0,list([start_lat, start_lng]))
                print('----F POS-----')
                print(f_pos)
                print('---------')
                pathlist=[]
                for day in range(0,k):
                    mat = []
                    for i in range(0, len(f_pos[day])):
                        mat2 = []
                        # f_pos[k].insert(0, list([start_lat, start_lng]))
                        for j in range(0, len(f_pos[day])):
                            mat2.append(util.pathlen(
                                f_pos[day][i][0], f_pos[day][i][1], f_pos[day][j][0], f_pos[day][j][1]))
                        mat.append(mat2)

                    print('----DISTANCE MATRIX-----')
                    print(mat)
                    print('---------')
                    optimalList = test.calc(mat)
                    print('----TSP PATH-----')
                    print(optimalList)
                    print('---------')
                    nameList = ['Himalayan Bliss']
                    for idx in optimalList:
                        if idx != 0:
                            nameList.append(df_list[day].iloc[idx-1]['Name'])
                    nameList.append('Himalayan Bliss')
                    print('----TSP PATH NAMES-----')
                    print(nameList)
                    pathlist.append(nameList)
                    print('---------')
                    numberofdayslist=[]
                    for i in range(1,numberofdays+1):
                        numberofdayslist.append(i)
                context={
                    'pathlist':pathlist,
                    'numberofdays':numberofdays,
                    'numberofdayslist':numberofdayslist
                }
                return render(request,'schedule.html',context)
    return render(request,'places.html')

def SpaView(request):
    return render(request,'spa_view.html')

def GalleryView(request):
    return render(request,'gallery_view.html')

def ThingsView(request):
    return render(request,'things2do.html')

def RoomFullView(request):
    return render(request,'room_full_view.html')

def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone') 
        desc=request.POST.get('desc') 
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent')
    return render(request,'contactus_view.html')

class BookingListView(ListView):
    model=Booking
    # template_name = 'booking_list_view.html'
    def get(self,request,*args,**kwargs):
        if self.request.user.is_staff:
            booking_list=Booking.objects.all()
            # return booking_list
            context={
                'booking_list':booking_list,
            }
            return render(request,'booking_list_view.html',context)
        else:
            if self.request.user.is_anonymous:
                return redirect('/accounts/login')
            booking_list=Booking.objects.filter(user=self.request.user)
            # return booking_list
            context={
                'booking_list':booking_list,
            }
            return render(request,'booking_list_view.html',context)

class RoomDetailView(View):
    def get(self,request,*args,**kwargs):
        if self.request.user.is_anonymous:
            return redirect('/accounts/login')
        
        category = self.kwargs.get('category', None)
        human_format_room_category=get_room_category_human_format(category)
        form=AvailabilityForm()
        if human_format_room_category is not None:
            room_rate=Room.objects.filter(category=category)[0].rate
            room_descs=dict(Room.ROOM_DESCS)
            room_desc=room_descs.get(category)
            room_details=dict(Room.ROOM_DETAILS)
            room_detail=room_details.get(category)
            context={
                'room_category':human_format_room_category,
                'category':category,
                'form':form,
                'room_rate':room_rate,
                'room_desc':room_desc,
                'room_detail':room_detail

            }
            return render(request,'room_detail_view.html',context)
        else:
            return  HttpResponse("Category does not exists")


    def post(self,request,*args,**kwargs):
        category = self.kwargs.get('category',None)
        
        form=AvailabilityForm(request.POST)

        if form.is_valid():
            data=form.cleaned_data

        client = razorpay.Client(auth=("rzp_test_XGgRqJjQqXkwb4", "L1IDvwV3WhofyxQ9gHOToTs2"))
        callback_url = 'http://127.0.0.1:8000/success/'
        email = self.request.user.email

        date_format = "%Y-%m-%d"
        a = datetime.strptime(str(data['check_in']), date_format)
        b = datetime.strptime(str(data['check_out']), date_format)
        delta = b - a
        print(delta.days)
        # print(data['check_in'])
        available_rooms=get_available_rooms(category,data['check_in'],data['check_out'])
        print(available_rooms)

        
        if available_rooms is not None:
            print(f'------{available_rooms[0].rate}-----')
            rate = available_rooms[0].rate
            room_categories=dict(available_rooms[0].ROOM_CATEGORIES)
            room_category=room_categories.get(available_rooms[0].category)
            order = client.order.create(dict(amount = rate*100*delta.days, currency = 'INR', payment_capture = '0' ))
            print(f'------{order}-----')
            book_room(request,available_rooms[0],data['check_in'],data['check_out'], order['id'], rate*delta.days)

            return render(self.request, 'payment_summary.html', {'order' : order,'check_in' : data['check_in'],'check_out' : data['check_out'], 'room' : room_category,'amount' : rate*delta.days, 'id' : order['id'], 'email' : email, 'callback_url' : callback_url})
        else:
            return redirect('hotel:RoomFullView')
        


@csrf_exempt
def success(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=("rzp_test_XGgRqJjQqXkwb4", "L1IDvwV3WhofyxQ9gHOToTs2"))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        room_book = Booking.objects.get(order_id=response['razorpay_order_id'])
        room_book.payment_id = response['razorpay_payment_id']
        room_book.paid = True
        room_book.save()
        return redirect('hotel:BookingListView')
    except:
        return render(request, "success.html")
    return render(request, "success.html")

def payment(request):
    return render(request, "payment_summary.html")


class CancelBookingView(DeleteView):
    model=Booking
    template_name='booking_cancel_view.html'
    success_url=reverse_lazy('hotel:BookingListView')

def booking_render_pdf_view(self,*args, **kwargs):
    pk=kwargs.get('pk')
    booking=get_object_or_404(Booking,pk=pk)
    room_categories=dict(booking.room.ROOM_CATEGORIES)
    room_category=room_categories.get(booking.room.category)
    template_path = 'booking_print_view.html'
    context = {'booking': booking,'room_category':room_category}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view(request):
    template_path = 'booking_print_view.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
