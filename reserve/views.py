from django.shortcuts import render
from reserve.models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
# from reserve.forms import UserForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.db.models import Q
from django.db import connections
from datetime import date, datetime
# Create your views here.

def index(request):
    return render(request, 'reserve/index.html')

def hotel(request):
    if "member_id" in request.session:
        context={}
        context.update(csrf(request))
        hotels = Hotel.objects.all()
        context['hotels'] = hotels
        return render(request, 'reserve/hotel.html', context)
    else:
        context={}
        context.update(csrf(request))
        return render_to_response("/reserve/login/",context)

def hotel_view(request):
    if "member_id" in request.session:
        if request.method == 'POST':
            context={}
            context.update(csrf(request))
            hotel_id = request.POST['h_id']
            hotel = Hotel.objects.get(pk=hotel_id)
            image = Hotel_Image.objects.raw('select * from reserve_hotel_image where hotel_f_id_id = %s' % hotel_id)
            context['hotels'] = hotel
            context['images'] = image
            return render(request, "reserve/hotel_view.html",context)
    else:
        context={}
        context.update(csrf(request))
        return render(request, "/reserve/login/",context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/reserve/")
    else:
        form = UserCreationForm()
    return render(request, "reserve/register.html", {
        'form': form,
    })

def login_view(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():  #to test if cookie enabled or not
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                request.session['member_id'] = user.username
                # Redirect to a success page.
                print  user.username
                return HttpResponseRedirect("/reserve/")
            else:
                return render(request,'reserve/login1.html')
        else:
            return HttpResponse("Please enable cookies and try again.") # if cookie not enabled
    else:
        request.session.set_test_cookie()
        return render(request,'reserve/login.html')

def logout_view(request):
    auth.logout(request)
    del request.session['member_id']
    return HttpResponseRedirect("/reserve/hotel/")

def reservation(request):
    if "member_id" in request.session:
        return render(request, 'reserve/reservation.html')
    else:
        return HttpResponseRedirect("/reserve/login/")

def reservation1(request):
    if "member_id" in request.session:
        return render(request, 'reserve/reservation1.html')
    else:
        return HttpResponseRedirect("/reserve/login/")

def result(request):
    if "member_id" in request.session:
        if request.method == 'POST':
            h_name = request.POST.get( 'hotel_name' )
            result = Hotel.objects.filter(Q( hotel_name__icontains = h_name ))
            in_date = request.POST.get('check_in')
            out_date = request.POST.get('check_out')
            now = datetime.now()
            date_now = now.strftime("%Y-%m-%d")
            # print date_now
            # print in_date
            # print out_date
            if out_date < in_date:
                return HttpResponseRedirect('/reserve/reservation1/')
            if in_date < date_now:
                return HttpResponseRedirect('/reserve/reservation1/')
            a = datetime.strptime(in_date, '%Y-%m-%d')
            b = datetime.strptime(out_date, '%Y-%m-%d')
            days = (b-a).days
            print days
            context={}
            context.update(csrf(request))
            context['hotel'] = result
            context['name'] = h_name
            context['date_in'] = in_date
            context['date_out'] = out_date
            context['days'] = days
            # context = {'hotel': result, 'name':h_name, 'date_in': in_date, 'date_out': out_date}
            return render(request, 'reserve/result.html', context)
        else:
            c={}
            c.update(csrf(request))
            return render(request, 'reserve/reservation.html',c)
    else:
        return HttpResponseRedirect("/reserve/login/")

def booking(request):
    if "member_id" in request.session:
        if request.method == 'POST':
            context={}
            context.update(csrf(request))
            hotel_name = request.POST['hotel_name']
            check_in = request.POST['check_in']
            check_out = request.POST['check_out']
            days = request.POST['days']
            hotel_id = request.POST['hotel_id']
            hotel_data = Hotel.objects.get(pk=hotel_id)
            # related_data = Hotel.objects.select_related('rate').get(id=hotel_id)
            rate = Rate.objects.raw("select * from reserve_rate where hotel_f_id_id=%s" % (hotel_id) )
            rate_result = 0.0
            count = 1.0
            for x in rate:
                count =+ 1
                y = int(x.rate)
                z = float(y)
                rate_result =+ z
            rate_result = rate_result/count
            print rate_result
            user_id = request.session['member_id']
            comment = Comment.objects.raw("select * from reserve_comment where hotel_f_id_id=%s" % (hotel_id) )
            image = Hotel_Image.objects.raw("select * from reserve_hotel_image where hotel_f_id_id=%s" % (hotel_id))
            context['hotel_data'] = hotel_data
            context['rates'] = rate
            context['avg_rate'] = rate_result
            context['comments'] = comment
            context['images'] = image
            context['name'] = hotel_name
            context['date_in'] = check_in
            context['date_out'] = check_out
            context['days'] = days
            context['hotel_id'] = hotel_id
            return render(request, "reserve/booking.html", context)
        else:
            c={}
            c.update(csrf(request))
            return render(request, 'reserve/reservation.html',c)
    else:
        return HttpResponseRedirect("/reserve/login/")

def confirm(request):
    if "member_id" in request.session:
        if request.method == 'POST':
            hotel_id = request.POST['hotel_id']
            comment = request.POST['comment']
            print "comment = %s" % (comment)
            if comment == '':
                print"yeeeees"
            else:
                username = request.session['member_id']
                comment = username +":"+comment
                insert_comment = Comment.objects.create(comment = comment, hotel_f_id_id = hotel_id)
            rate = request.POST['rate']
            rate = int(rate)
            insert_rate = Rate.objects.create(rate = rate, hotel_f_id_id = hotel_id)
            rate = int(rate)
            single = request.POST['single']
            double = request.POST['double']
            triple = request.POST['triple']
            suite = request.POST['suite']
            date_in = request.POST['date_in']
            date_out = request.POST['date_out']
            days = request.POST['days']
            context={}
            context.update(csrf(request))
            hotel_data = Hotel.objects.raw("select * from reserve_hotel where id =%s" % (hotel_id))
            for x in hotel_data:
                h_single = x.num_of_singles
                h_double = x.num_of_doubles
                h_triple = x.num_of_triples
                h_suite = x.num_of_suites
                single_price = x.single_price
                double_price = x.double_price
                triple_price = x.triple_price
                suite_price = x.suite_price
            h_single = int(h_single)
            h_double = int(h_double)
            h_triple = int(h_triple)
            h_suite = int(h_suite)
            single = int(single)
            double = int(double)
            triple = int(triple)
            suite = int(suite)
            days = int(days)
            single_price = int(single_price)
            double_price = int(double_price)
            triple_price = int(triple_price)
            suite_price = int(suite_price)
            r_single = Reserved_Room.objects.filter(Q(room_type__icontains = 'single'),Q(check_in_date__gte = date_in))
            r_double = Reserved_Room.objects.filter(Q(room_type__icontains = 'double'),Q(check_in_date__gte = date_in))
            r_triple = Reserved_Room.objects.filter(Q(room_type__icontains = 'triple'),Q(check_in_date__gte = date_in))
            r_suite = Reserved_Room.objects.filter(Q(room_type__icontains = 'suite'),Q(check_in_date__gte = date_in))
            res_single = 0
            res_double = 0
            res_triple = 0
            res_suite = 0
            for r in r_single:
                x = r.num_of_rooms
                x = int(x)
                res_single =+ x
            for r in r_double:
                x = r.num_of_rooms
                x = int(x)
                res_double =+ x
            for r in r_triple:
                x = r.num_of_rooms
                x = int(x)
                res_triple =+ x
            for r in r_suite:
                x = r.num_of_rooms
                x = int(x)
                res_suite =+ x
############### single no of rooms that wanted by client, h_single total number in db, res_single reserved room ##########
            rest_single = h_single - res_single - single
            rest_double = h_double - res_double - double
            rest_triple = h_triple - res_triple - triple
            rest_suite = h_suite - res_suite - suite
            print "triple_tot %d" % h_triple
            print "triple_res %d" % res_triple
            print "rest  %d" % triple
            print "aaaaaa %d" % rest_triple
            context={}
            context.update(csrf(request))
            if rest_suite == 0:
                context['z_suite'] = 'zero'
            if rest_triple == 0:
                context['z_triple'] = 'zero'
                print " aaaaaaaaaaa"
            if rest_double == 0:
                context['z_double'] = 'zero'
            if rest_single == 0:
                context['z_single'] = 'zero'
            dict = {}
            total_price = days*single*single_price + days*double*double_price + days*triple*triple_price + days*suite*suite_price
            offer = Company_Offer.objects.filter(Q(start__gte = date_in),Q(hotel_f_id_id = hotel_id))

            for x in offer:
                name = x.company_name
                dis = x.discount
                dis = float(dis)
                print dis
                discount =  dis/100
                dis_per = discount*total_price
                print "dis_per %s" % dis_per
                price_after = total_price - dis_per
                print price_after
                dict[name] = price_after
            print "price %d" % (total_price)
            context['offer'] = offer
            context['dict'] = dict
            context['total_price'] = total_price
            context['hotel_id'] = hotel_id
            context['single'] = single
            context['double'] = double
            context['triple'] = triple
            context['suite'] = suite
            context['date_in'] = date_in
            context['date_out'] = date_out
            return render(request, 'reserve/ok.html',context)
        else:
            c={}
            c.update(csrf(request))
            return render(request, 'reserve/reservation.html',c)
    else:
        return HttpResponseRedirect("/reserve/login/")

def finishing(request):
    if "member_id" in request.session:
        if request.method == 'POST':
            single = request.POST['single']
            double = request.POST['double']
            triple = request.POST['triple']
            suite = request.POST['suite']
            date_in = request.POST['date_in']
            date_out = request.POST['date_out']
            hotel_id = request.POST['hotel_id']
            single = int(single)
            double = int(double)
            triple = int(triple)
            suite = int(suite)
            if single != 0:
                single_res = Reserved_Room.objects.create(room_type = 'single', num_of_rooms = single,check_in_date = date_in, check_out_date = date_out, hotel_f_id_id = hotel_id)
            if double != 0:
                double_res = Reserved_Room.objects.create(room_type = 'double', num_of_rooms = double,check_in_date = date_in, check_out_date = date_out, hotel_f_id_id = hotel_id)
            if triple != 0:
                triple_res = Reserved_Room.objects.create(room_type = 'triple', num_of_rooms = triple,check_in_date = date_in, check_out_date = date_out, hotel_f_id_id = hotel_id)
            if suite != 0:
                suite_res = Reserved_Room.objects.create(room_type = 'suite', num_of_rooms = suite,check_in_date = date_in, check_out_date = date_out, hotel_f_id_id = hotel_id)
            c={}
            c.update(csrf(request))
            return render(request, 'reserve/index.html',c)
        else:
            return HttpResponseRedirect("/reserve/login/")
    else:
        return HttpResponseRedirect("/reserve/index/")

def offer_month(request):
    if "member_id" in request.session:
        d=date.today()
        x=d.month
        print x
        c={}
        c.update(csrf(request))
        offer = Company_Offer.objects.filter(Q(start__month = x))
        for x in offer:
            h_id = x.hotel_f_id
            print "nammmme %s" % h_id
        c['offer_month'] = offer
        return render(request, 'reserve/offer_month.html',c)
    else:
            return HttpResponseRedirect("/reserve/login/")

def offer_all(request):
    if "member_id" in request.session:
        c={}
        c.update(csrf(request))
        offer = Company_Offer.objects.all()
        c['offer_month'] = offer
        return render(request, 'reserve/offer.html',c)
    else:
        return HttpResponseRedirect("/reserve/login/")
