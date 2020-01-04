from django.shortcuts import render, redirect
from django.http import HttpResponse


# Comment App ve Message App ile ilgili importlar
import datetime
from django.contrib import messages
from comments import models as commentModel
from movies.models import Movie
from random import sample
from django.db.models import Q



import smtplib
#servere baglanmak icin bu modul kullanilir.
from email.mime.multipart import MIMEMultipart
#mailin yapisini olusturur.Govde gibi
from email.mime.text import MIMEText
#mailde ne yazacagini bu modulle ayarliyoruz,
import sys
#hata mesajini sterror ile cevirecegiz


from movies.views import get_slider, get_on_imdb

# Create your views here.


def index(request):
    context = {}
    movies1 = get_movie_queryset('')
    movies = Movie.objects.all()
    context['movies1'] = movies1
    context['movies'] = movies

    get_slider(context)
    get_on_imdb(context)

    return render(request, 'pages/index.html', context)


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def sendMessage(request):

    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = request.POST['email']
    # eger kullanici giris yaptiysa mevcut kullanici emailini al, degilse post edilen emaili al

    name = request.POST['name']
    surname = request.POST['surname']
    message = request.POST['message']
    date = datetime.datetime.now().date()

    newMessage = commentModel.Message(
        email=email, name=name, surname=surname, message=message, created_date=date)
    newMessage.save()
    # message tablosuna yeni veriler kaydettik

    # oto mail gonderme ------------------------------
   

    mesaj=MIMEMultipart()
    mesaj["From"]="zeydustaogllu@gmail.com"
    mesaj["To"]="zeydustaogllu@gmail.com"
    mesaj["Subject"]="Message from PyMovies"

    yazi= """
    name:  {} 
    Surname:  {}   
    Email: {} 
    Message: {}
    """.format(newMessage.name, newMessage.surname, newMessage.email,newMessage.message)

    print(yazi)

    mesaj_govdesi=MIMEText(yazi,"plain")

    mesaj.attach(mesaj_govdesi)

    try:
        mail=smtplib.SMTP("smtp.gmail.com",587)
        mail.ehlo()
        mail.starttls()
        mail.login("zeydustaogllu@gmail.com" , "38develiZu.")
        mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
        print("Mail Basari ile gonderildi..")
        mail.close()
        messages.success(request, 'Mail Basari ile gonderildi..')

    except:
        sys.stderr.write("Bir sorun olustu...")
        sys.stderr.flush()
    




    return redirect('contact')


def get_movie_queryset(query=None):
    queryset = []
    movies = Movie.objects.filter(Q(turu__contains=query)).distinct()
    for movie in movies:
        queryset.append(movie)
    queryset_new = sample(queryset, 20)
    return list(set(queryset_new))
