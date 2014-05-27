#-*- coding:utf-8 -*-
from django.shortcuts import redirect, render

from bookshare.apps.books.models import Course
from django.http import HttpResponse
import forms
import models
import requests
import json
import pprint

# Create your views here.
def request_rent(request):
    if request.method == "GET":
        context = {
            "form": forms.RentRequestForm()
        }
        return render(request, "request_rent.html", context)

    if request.method == "POST":
        form = forms.RentRequestForm(request.POST)
        if form.is_valid():
            models.request_rent(form.cleaned_data["actor"], form.cleaned_data["book"])
            return redirect('books:index')

def deliver_stock(request):
    if request.method == "GET":
        context = {
            "form": forms.StockDeliverForm()
        }
        return render(request, "deliver_stock.html", context)

    if request.method == "POST":
        form = forms.StockDeliverForm(request.POST)
        if form.is_valid():
            models.deliver_stock(form.cleaned_data["actor"],
                                form.cleaned_data["book"],
                                form.cleaned_data["condition"])
            return redirect('books:index')

def process_rent_request(request):
    if request.method == "GET":
        context = {
            "form": forms.RentRequestProcessForm()
        }
        return render(request, "process_rent_request.html", context)

    if request.method == "POST":
        form = forms.RentRequestProcessForm(request.POST)
        if form.is_valid():
            models.process_rent_request(form.cleaned_data["request"])
            return redirect('books:index')


def make_dummy_data(request):
    url = 'https://portal.hanyang.ac.kr/sugang/SgscAct/findSuupSearchSugangSiganpyo.do'

    payload = {"skipRows":"0","maxRows":"74","strLocaleGb":"ko","strIsSugangSys":"true","strDetailGb":"0","notAppendQrys":"true","strSuupOprGb":"0","strJojik":"Y0000316","strSuupYear":"2014","strSuupTerm":"10","strIlbanCommonGb":"2","strIsuGbCd":"","strHaksuNo":"","strGwamok":"","strDaehak":"Y0000361","strHakgwa":"Y0000383","strYeongyeok":""}

    headers = {'POST':'/sugang/SgscAct/findSuupSearchSugangSiganpyo.do HTTP/1.1','Host':' portal.hanyang.ac.kr','Connection':' keep-alive','Content':'Length: 330','Accept':' application/json, text/javascript, */*; q=0.01','Origin':' https://portal.hanyang.ac.kr','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36','Content-Type': 'application/json+sua; charset=UTF-8','Referer': 'https://portal.hanyang.ac.kr/sugang/sulg.do','Accept-Encoding': 'gzip,deflate,sdch','Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4','Cookie': 'WMONID=GfaUXVyTzP4; LMS_JSESSIONID=LLHdTCBDJY24Kzqp2T6Nrcwpp9JKgHLh35mtLTnszm47y2v3P1hH!-128003781!2117203880; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=ko; HYIN_JSESSIONID=3z7sTGWhJq83TP89kTQZcL8Dv8RWM8cKpLfjLyQf4l4DJLqWqg1G!1175962333!201147940; _ga=GA1.3.2416065.1383920534; newLoginStatus=PORTALe38b899b-d40e-4f2e-b361-b0e56490d150; COM_JSESSIONID=gqN0TGWXghJG8R1nMYP81r7k4tzGD1NFZyjdJxQmRKLpFYX5jLnh!-1993710250!-1739781991; HAKSA_JSESSIONID=JcpQTGWhHH2PpdjJwPpwKY1LT8vqjT4rJTQ7YZjqhQ7GyLwpbLDs!-653343242!1971840233; ipSecGb=MQ%3D%3D; loginUserId=MjAwODAzNjAzOA%3D%3D; SUGANG_JSESSIONID=pRTHTGYT4L7QYzh1ck8hQ59n5BbGCBJblPYgbhTYSvQpczM40tcJ!1794595370!692021351'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    computer_science = json.loads(r.content)['DS_SUUPGS03TTM01'][0]['list']

    for each in computer_science:
        Course.objects.get_or_create(title=each['gwamokNm'], department=each['gnjSosokNm'], year=each['suupYear'], semester='first')
        
    return HttpResponse(computer_science)
    

