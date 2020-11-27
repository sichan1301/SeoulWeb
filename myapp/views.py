from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from datetime import datetime
from django.utils.dateformat import DateFormat
import requests 
import urllib.request
from .models import Blog
from .forms import NewBlog
from .feed import popularParse,seoulParse,yongsanParse,newsParse,coronaParse,weatherParse,centralParse,sooseoParse,dongseoulParse,gangnamParse
import math

# Create your views here.
def index(request):
    today = DateFormat(datetime.now()).format('Y년m월d일')
    return render(request,'myapp/index.html',{'today':today})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('loginsuccess')
        else:
            return render(request, 'myapp/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'myapp/login.html')

def logout(request):
    response = render(request, 'myapp/logout.html')
    response.delete_cookie('username')
    response.delete_cookie('password')
    auth.logout(request)
    return response

def signup(request):
    if request.method=="POST":
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user( username=request.POST['username'], password=request.POST['password1'],last_name=request.POST['lastname'])
            return redirect('signupsuccess')
        else:
            return redirect('fail')
    return render(request,'myapp/signup.html')


def loginsuccess(request):
    return render(request,'myapp/loginsuccess.html')       

def signupsuccess(request):
    return render(request,'myapp/signupsuccess.html')   

def change_suc(request):
    return render(request,'myapp/change_suc.html')

def fail(request):
    if request.method=="POST":
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user( username=request.POST['username'], password=request.POST['password1'])
        return redirect('index')
    return render(request,'myapp/fail.html')

def change(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect('login')
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, "myapp/change.html",context)

def read(request):
    blogs = Blog.objects.all()
    blog_list = Blog.objects.all()
    # 모든 Blog 글을 대상으로
    paginator = Paginator(blog_list, 5)
    # 블로그 객체 3개 한페이지로 자르기
    page = request.GET.get('page')
    # request된 페이지가 뭔지 알아낸다 (request페이지를 변수에 담는다)
    posts = paginator.get_page(page)
    # request된 페이지를 얻어온 뒤 return 해준다
    return render(request,'myapp/read.html',{'blogs':blogs,'posts':posts})

def create(request):
    if request.method =="POST":
        form = NewBlog(request.POST)
        if form.is_valid:
            post = form.save(commit = False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('read')
    else:
        form = NewBlog()
        return render(request,'myapp/create.html',{'form':form})

def delete(request,pk):
    blog = get_object_or_404(Blog, pk = pk)
    blog.delete()
    return redirect('read')

def update(request,pk):
    blog = get_object_or_404(Blog,pk=pk)
    form = NewBlog(request.POST, instance=blog)

    if form.is_valid():
        form.save()
        return redirect('read')
    
    return render(request,'myapp/create.html',{'form':form})

def weather(request):
    weath = weatherParse()
    tempMain = weath['main']
    temp = tempMain['temp']
    humid = tempMain['humidity']
    w = weath['weather']
    w = w[0]
    dayW = w['main']
    wind = weath['wind']
    windSpeed = wind['speed']
    cloudAll = weath['clouds']
    cloud = cloudAll['all']
    return render(request, 'myapp/weather.html', {'humid':humid, 'temp':math.floor(temp-272.15), 'weather':dayW, 'wind':windSpeed, 'cloud':cloud})

def corona(request):   
    webpage = urllib.request.urlopen('https://www.seoul.go.kr/coronaV/coronaStatus.do')
    soup = BeautifulSoup(webpage,'html.parser')

    total = soup.find('div','num num1').find('p','counter').get_text()  
    plus = soup.find('div','num-wrap-new').find('p','counter').get_text()
    iso_ing = soup.find('div','num num8').find('p','counter').get_text()
    iso_clear_plus = soup.find('div','cell cell5').find('div','num num11').find('p','counter').get_text()
    iso_clear = soup.find('div','cell cell5').find('div','num num8').find('p','counter').get_text()
    death = soup.find('div','cell cell6').find('div','num num9').find('p','counter').get_text()    


    return render(request,'myapp/corona.html',{'total':total,'plus':plus,'iso_ing':iso_ing,'iso_clear':iso_clear,'death':death,'iso_clear_plus':iso_clear_plus})


    # cor = coronaParse()
    # num = {}
    # for number in range(0,5):
    #     num[cor[number]['CORONA19_AREA']] = cor[number]['CORONA19_NO']
    
    # return render(request,'myapp/corona.html',{'num':num})


def subway(request):

    sub_seoul = seoulParse()
    realtime_seoul = sub_seoul['realtimeArrivalList']
    
    real0_seoul = realtime_seoul[0]
    direction0_seoul = real0_seoul['trainLineNm']
    arrive0_seoul= real0_seoul['arvlMsg2']

    real1_seoul = realtime_seoul[1]
    direction1_seoul = real1_seoul['trainLineNm']
    arrive1_seoul= real1_seoul['arvlMsg2']

    real2_seoul = realtime_seoul[2]
    direction2_seoul = real2_seoul['trainLineNm']
    arrive2_seoul= real2_seoul['arvlMsg2']
    
    real3_seoul = realtime_seoul[3]
    direction3_seoul = real3_seoul['trainLineNm']
    arrive3_seoul= real3_seoul['arvlMsg2']

    real4_seoul = realtime_seoul[4]
    direction4_seoul = real4_seoul['trainLineNm']
    arrive4_seoul= real4_seoul['arvlMsg2']


    sub_yongsan=yongsanParse()
    realtime_yongsan = sub_yongsan['realtimeArrivalList']
    
    real0_yongsan = realtime_yongsan[0]
    direction0_yongsan = real0_yongsan['trainLineNm']
    arrive0_yongsan= real0_yongsan['arvlMsg2']

    real1_yongsan = realtime_yongsan[1]
    direction1_yongsan = real1_yongsan['trainLineNm']
    arrive1_yongsan= real1_yongsan['arvlMsg2']

    real2_yongsan = realtime_yongsan[2]
    direction2_yongsan = real2_yongsan['trainLineNm']
    arrive2_yongsan= real2_yongsan['arvlMsg2']
    
    real3_yongsan = realtime_yongsan[3]
    direction3_yongsan = real3_yongsan['trainLineNm']
    arrive3_yongsan= real3_yongsan['arvlMsg2']

    real4_yongsan = realtime_yongsan[4]
    direction4_yongsan = real4_yongsan['trainLineNm']
    arrive4_yongsan= real4_yongsan['arvlMsg2']


    sub_central=centralParse()
    realtime_central = sub_central['realtimeArrivalList']
    
    real0_central = realtime_central[0]
    direction0_central = real0_central['trainLineNm']
    arrive0_central= real0_central['arvlMsg2']

    real1_central = realtime_central[1]
    direction1_central = real1_central['trainLineNm']
    arrive1_central= real1_central['arvlMsg2']

    real2_central = realtime_central[2]
    direction2_central = real2_central['trainLineNm']
    arrive2_central = real2_central['arvlMsg2']
    
    real3_central = realtime_central[3]
    direction3_central = real3_central['trainLineNm']
    arrive3_central= real3_central['arvlMsg2']

    real4_central = realtime_central[4]
    direction4_central = real4_central['trainLineNm']
    arrive4_central= real4_central['arvlMsg2']


    sub_sooseo=sooseoParse()
    realtime_sooseo = sub_sooseo['realtimeArrivalList']
    
    real0_sooseo = realtime_sooseo[0]
    direction0_sooseo = real0_sooseo['trainLineNm']
    arrive0_sooseo = real0_sooseo['arvlMsg2']

    real1_sooseo = realtime_sooseo[1]
    direction1_sooseo = real1_sooseo['trainLineNm']
    arrive1_sooseo= real1_sooseo['arvlMsg2']

    real2_sooseo = realtime_sooseo[2]
    direction2_sooseo = real2_sooseo['trainLineNm']
    arrive2_sooseo = real2_sooseo['arvlMsg2']
    
    real3_sooseo = realtime_sooseo[3]
    direction3_sooseo = real3_sooseo['trainLineNm']
    arrive3_sooseo= real3_sooseo['arvlMsg2']

    real4_sooseo = realtime_sooseo[4]
    direction4_sooseo = real4_sooseo['trainLineNm']
    arrive4_sooseo= real4_sooseo['arvlMsg2']   


    sub_dongseoul = dongseoulParse()
    realtime_dongseoul = sub_dongseoul['realtimeArrivalList']
    
    real0_dongseoul = realtime_dongseoul[0]
    direction0_dongseoul = real0_dongseoul['trainLineNm']
    arrive0_dongseoul= real0_dongseoul['arvlMsg2']

    real1_dongseoul = realtime_dongseoul[1]
    direction1_dongseoul = real1_dongseoul['trainLineNm']
    arrive1_dongseoul= real1_dongseoul['arvlMsg2']

    real2_dongseoul = realtime_dongseoul[2]
    direction2_dongseoul = real2_dongseoul['trainLineNm']
    arrive2_dongseoul= real2_dongseoul['arvlMsg2']
    
    real3_dongseoul = realtime_dongseoul[3]
    direction3_dongseoul = real3_dongseoul['trainLineNm']
    arrive3_dongseoul= real3_dongseoul['arvlMsg2']

    sub_gangnam = gangnamParse()
    realtime_gangnam = sub_gangnam['realtimeArrivalList']
    
    real0_gangnam = realtime_gangnam[0]
    direction0_gangnam = real0_gangnam['trainLineNm']
    arrive0_gangnam= real0_gangnam['arvlMsg2']

    real1_gangnam = realtime_gangnam[1]
    direction1_gangnam = real1_gangnam['trainLineNm']
    arrive1_gangnam= real1_gangnam['arvlMsg2']

    real2_gangnam = realtime_gangnam[2]
    direction2_gangnam = real2_gangnam['trainLineNm']
    arrive2_gangnam= real2_gangnam['arvlMsg2']
    
    real3_gangnam = realtime_gangnam[3]
    direction3_gangnam = real3_gangnam['trainLineNm']
    arrive3_gangnam= real3_gangnam['arvlMsg2']

    real4_gangnam = realtime_gangnam[3]
    direction4_gangnam = real4_gangnam['trainLineNm']
    arrive4_gangnam= real4_gangnam['arvlMsg2']    

    return render(request,"myapp/subway.html",{'direction0_seoul':direction0_seoul,'arrive0_seoul':arrive0_seoul,'direction1_seoul':direction1_seoul,'arrive1_seoul':arrive1_seoul,'direction2_seoul':direction2_seoul,'arrive2_seoul':arrive2_seoul,'direction3_seoul':direction3_seoul,'arrive3_seoul':arrive3_seoul,'direction4_seoul':direction4_seoul,'arrive4_seoul':arrive4_seoul,'direction0_yongsan':direction0_yongsan,'arrive0_yongsan':arrive0_yongsan,'direction1_yongsan':direction1_yongsan,'arrive1_yongsan':arrive1_yongsan,'direction2_yongsan':direction2_yongsan,'arrive2_yongsan':arrive2_yongsan,'direction3_yongsan':direction3_yongsan,'arrive3_yongsan':arrive3_yongsan,'direction4_seoul':direction4_yongsan,'arrive4_yongsan':arrive4_yongsan,'direction0_central':direction0_central,'arrive0_central':arrive0_central,'direction1_central':direction1_central,'arrive1_central':arrive1_central,'direction2_central':direction2_central,'arrive2_central':arrive2_central,'direction3_central':direction3_central,'arrive3_central':arrive3_central,'direction4_central':direction4_central,'arrive4_central':arrive4_central,'direction0_sooseo':direction0_sooseo,'arrive0_sooseo':arrive0_sooseo,'direction1_sooseo':direction1_sooseo,'arrive1_sooseo':arrive1_sooseo,'direction2_sooseo':direction2_sooseo,'arrive2_sooseo':arrive2_sooseo,'direction3_sooseo':direction3_sooseo,'arrive3_sooseo':arrive3_sooseo,'direction4_sooseo':direction4_sooseo,'arrive4_sooseo':arrive4_sooseo,'direction0_dongseoul':direction0_dongseoul,'arrive0_dongseoul':arrive0_dongseoul,'direction1_dongseoul':direction1_dongseoul,'arrive1_dongseoul':arrive1_dongseoul,'direction2_dongseoul':direction2_dongseoul,'arrive2_dongseoul':arrive2_dongseoul,'direction3_dongseoul':direction3_dongseoul,'arrive3_dongseoul':arrive3_dongseoul,'direction0_gangnam':direction0_gangnam,'arrive0_gangnam':arrive0_gangnam,'direction1_gangnam':direction1_gangnam,'arrive1_gangnam':arrive1_gangnam,'direction2_gangnam':direction2_gangnam,'arrive2_gangnam':arrive2_gangnam,'direction3_gangnam':direction3_gangnam,'arrive3_gangnam':arrive3_gangnam,'direction4_gangnam':direction4_gangnam,'arrive4_gangnam':arrive4_gangnam
    })

    
    # city = ["seoul","yongsan"]
    
    # for i in city(0,len(city),1):
    #     sub[i]=[i]Parse()
        
    #     realtime_[i] = sub_[i]['realtimeArrivalList']
        
    #     real0_[i] = realtime_[i][0]
    #     direction0_[i] = real0_[i]['trainLineNm']
    #     arrive0_[i]= real0_[i]['arvlMsg2']

    #     real1_[i] = realtime_[i][1]
    #     direction1_[i] = real1_[i]['trainLineNm']
    #     arrive1_[i]= real1_[i]['arvlMsg2']

    #     real2_[i] = realtime_[i][2]
    #     direction2_[i] = real2_[i]['trainLineNm']
    #     arrive2_[i]= real2_[i]['arvlMsg2']
        
    #     real3_[i] = realtime_[i][3]
    #     direction3_[i] = real3_[i]['trainLineNm']
    #     arrive3_[i]= real3_[i]['arvlMsg2']

    #     real4_[i] = realtime_[i][4]
    #     direction4_[i] = real4_[i]['trainLineNm']
    #     arrive4_[i]= real4_[i]['arvlMsg2']


def news(request):
    neww = newsParse()
    new = neww['SeoulNewsList']
    roww = new['row']
    row = roww[0]
    title = row['POST_TITLE']
    content = row['POST_CONTENT']
    return render(request,'myapp/news.html',{'title':title,'content':content})

def detail(request,detail_id):
    details = get_object_or_404(Blog,pk=detail_id)
    return render(request,'myapp/detail.html',{'details':details})