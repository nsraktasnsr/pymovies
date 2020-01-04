from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Movie 
import datetime
from django.contrib import messages
from comments import models as commentModel
from django.db.models import Q
from random import sample
from django.core.paginator import Paginator


def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    context = {
    "movies": movies
    }
    get_slider(context)  # slider eklemek istediginiz sayfaya context ten sonra ekliyorsunuz. 
                         # bu fonksiyon sayfaya gonderilen context bilgisine sliderda kullanilacak son eklenen 9 filmi ekliyor   
    get_on_imdb(context) # imdb puanina gore ilk 10 filmi bulup contexte ekleyen fonksiyon
    
    return render(request, 'movies/list.html', context)

def category(request):
    # print(request.__dict__)
    title = request.POST['category'] + ' Movies'
    context = {
        "title":title
    }
    movies = get_movie_queryset(request.POST['category'])
    context['movies'] = movies
    return render(request, 'movies/movielist.html', context)

def older(request):
    context = {}
    movies = get_movie_queryset_older('')
    context['movies'] = movies
    return render(request, 'movies/movielist.html', context)

def imdb(request):
    context = {}
    movies = get_movie_queryset_imdb("")
    if len(movies) > 12:
        paginator = Paginator(movies, 12)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        context['movies'] = movies
    else:
        context['movies'] = movies
    return render(request, 'movies/movielist.html', context)

def get_movie_queryset(query=None):
    queryset = []
    movies = Movie.objects.filter(Q(yil__contains=query) | Q(turu__contains=query)).distinct()
    for movie in movies:
        queryset.append(movie)
    return list(set(queryset))

def get_movie_queryset_imdb(query=None):
    movies = Movie.objects.filter(imdb__gte=7).order_by('-imdb')
    return movies

def get_movie_queryset_older(query=None):
    queryset = []
    movies = Movie.objects.filter(Q(yil__contains=query)).distinct()
    for movie in movies:
        if int(movie.yil) < 2010:
            queryset.append(movie)
    return list(set(queryset))

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    try:
        comments = commentModel.Comment.objects.filter(
            movie_id=movie_id).order_by('-created_date')
    except:
        comments = None
    # db den mavcut filme yapilan yorumlari tarihe gore siralayarak cektik
    totalRate = 0
    for i in comments:
        totalRate = totalRate + int(i.rating)
    # filme yapilan puanlari topladik
    avarate = round(totalRate/len(comments), 1) if totalRate > 0 else 0
    # puan toplamlarini yorum adedine bolerek ortalamasini bulduk. sifira bolunme hatasi almamak icin kosul olusturduk
    context = {
        'movie': movie,
        'comments': comments,
        'averate': avarate
    }
    return render(request, 'movies/detail.html', context)

def addComment(request):
    comment = request.POST['comment']
    rating = request.POST['rating']
    movieid = request.POST['movieid']
    userid = request.POST['userid']
    date = datetime.datetime.now().date()
    newComment = commentModel.Comment(
        comment=comment, rating=rating, movie_id=movieid, user_id=userid, created_date=date)
    newComment.save()
    messages.success(request, 'Yorumunuz basariyla eklendi.')
    return redirect('detail', movie_id=movieid)

def delComment(request):
    commentid = request.POST['commentid']
    movieid = request.POST['movieid']
    comment = commentModel.Comment.objects.get(id=commentid)
    comment.delete()
    messages.success(request, 'Yorumunuz basariyla silindi.')
    return redirect('detail', movie_id=movieid)


def search(request):
    context = {}   # Bos bir liste olusturulur
    if request.GET:  # eger searchbar da get yapilmissa
        query = request.GET['q']  #aranan yaziyi degiskene ata
        context['query'] = str(query)  # aranan yazi degerini sayfada kullanabilmek icin sozluge ekle
    movies = get_movie_queryset_search(query) # aranan yazi degeri ile fonksiyon calistirilir
    context['movies'] = movies         # sorgu sonucunda bulunan objeleri sozluge aktarir.
    return render(request, 'movies/search.html',context)

def get_movie_queryset_search(query=None):    # searchbar da aranan yazi degerine gore kayitlarin isim ve aciklama kisimlarinda sorgu yapan fonksiyon
    queries = query.strip().split(" ") # girilen yaziyi kelimelere ayiriyor ve degiskene atiyor.
                                       # onemli not: ".split(" ")" bunu eklemezsek sadece ".split()" yapilirsa searchbar bos iken arama butonuna basidiginda
                                                    # hicbir veri getirmiyor. bu sekilde tum kayitlari listeliyor.
    # asagidaki map fonksiyonu yukarida queries degiskenindeki kelimeleri, her kelime icin isim ve aciklama alanlarinda 
        # veritabaninda sorgulama yapiyor.
    queryset = map(lambda x: Movie.objects.filter(Q(name__contains = x) | Q(description__contains = x) | Q(turu__contains = x) | Q(yil__contains = x) | Q(imdb__contains = x)), queries) 
    queryset = list(queryset)[0]  # Movie.objects.filter() fonksiyonu sonuclari liste olarak donduruyor. 
                                    # map fonksiyonundan sonuclari almamiz icin liste yapmamiz gerekiyor, bu sekilde liste icinde liste oluyor.
                                    # bu problemi asmak icin map fonksiyonda bulunan ilk elemani alip degiskenimize atiyoruz. liste icinde listeden kurtulmus oluyoruz.
    return list(set(queryset))     # bu aramalar esnasinda bazi objeler iki veya daha fazla listede bulunabilir. bunu set() ile hr kaydin bir defa listelenmesini sagliyoruz.

def get_slider(context):        # slider icin ilgili sayfanin contextine son eklenen 9 filmi ekleyen fonksiyon.
    slider_images = Movie.objects.order_by('-yil')    # filmleri olusturulma tarihine gore tersten siraliyoruz
    slider_images = slider_images[0:15]                          # olusan listeden sliderda gostermek istedigimiz kadar film elemani seciyoruz. biz 9 olarak belirledik
    context['slider_images'] = slider_images                    # bunu sozluk yapisina ekliyoruz.

def get_on_imdb(context):
    on_imdb = Movie.objects.order_by('-imdb')  # order_by ile siralama yaptik..(_imdb ) ile azalan siralama yaptik
    on_imdb = on_imdb[0:10]                     # imdb en yuksekten dusuge dogru ilk 10 nu aldik
    context['on_imdb'] = on_imdb  