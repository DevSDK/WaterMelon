import datetime
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from Data.models import RawData, HourData
from Data.serializer import RawDataSerializer, HourDataSerializer
from Pipe.models import Pipe

'''
Raw Data Field 는 10만개 유지(변동가능)


GET	/data/current/raw		response: Get CurrentData
GET	/data/current/hour		response: Get CurrentHourData
GET	/data/current/day		response: Get CurrentDay
GET	/data/current/year		response: GET CurrentYear

GET	/data/list/hour		Parameter:date=YYYY-mm-dd	response: hour data from day (24)
GET	/data/list/year		Parameter:date=YYYY-mm-dd	response: hour data list from year(8,760)

POST	/data/push		Body { Temp = 온도, Data = 흐름량L/sec, Pipe=파이프}

POST	/user/login		BODY { ID = 아이디, Password = 페스워드}

GET	/user/profile		response: Profile  Info {Name,Etc...}

'''


def GetAverageRange(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\":\"Invalid POST sMethod \"}", status=400)
    if not request.user.is_authenticated():
        return HttpResponse("{\"message\":\"Not authenticated\"}", status=401)

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if start_date_str is None:
        return HttpResponse("{\"message\":\"start_date must require\"}", status=401)

    if end_date_str is None:
        date = datetime.datetime.now().date()
        startdate = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        datedata = RawData.objects.filter(DateTime__range = [startdate.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d")])
        data_sum = 0.0
        temp_sum = 0.0


        if datedata.count() == 0 :
            return HttpResponse("{\"average_data\":\"" + str(0.0)+ "\",\"average_temp\":\"" + str(0.0) + "\"}");

        for i in datedata:
            data_sum += i.Data
            temp_sum += i.Temp

        average_data = data_sum/datedata.count()
        average_temp = temp_sum/datedata.count()

        return HttpResponse("{\"average_data\":\""+ average_data.__str__()+"\",\"average_temp\":\""+average_temp.__str__()+"\"}");



    startdate = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    endtime = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    datedata = HourData.objects.filter(DateTime__range=[startdate.strftime("%Y-%m-%d"), endtime.strftime("%Y-%m-%d")])
    data_sum = 0.0
    temp_sum = 0.0

    if datedata.count() == 0:
        return HttpResponse("{\"average_data\":\"" + str(0.0) + "\",\"average_temp\":\"" + str(0.0) + "\"}");

    for i in datedata:
        data_sum += i.Data
        temp_sum += i.Temp

    average_data = data_sum / datedata.count()
    average_temp = temp_sum / datedata.count()

    return HttpResponse("{\"average_data\":\""+ average_data.__str__()+"\",\"average_temp\":\""+average_temp.__str__()+"\"}");


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def GetListRange(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\":\"Invalid POST sMethod \"}", status=400)
    if not request.user.is_authenticated():
        return HttpResponse("{\"message\":\"Not authenticated\"}", status=401)

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if start_date_str is None:
        return HttpResponse("{\"message\":\"start_date must require\"}", status=401)


    if end_date_str is None:
        date = datetime.datetime.now().date() + datetime.timedelta(days=1)
        startdate = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        datedata = HourData.objects.filter(DateTime__range = [startdate.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d")])
        serializer = HourDataSerializer(datedata, many=True)
        return Response(serializer.data)

    startdate = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    endtime = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date() + datetime.timedelta(days=1)
    datedata = HourData.objects.filter(DateTime__range=[startdate.strftime("%Y-%m-%d"), endtime.strftime("%Y-%m-%d")])
    serializer = HourDataSerializer(datedata, many=True)
    return Response(serializer.data)




@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def GetCurrentData(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\":\"Invalid Method \"}", status=400)

    if not request.user.is_authenticated():
        return HttpResponse("{\"message\":\"Not authenticated\"}", status=401)

    pipe = request.GET.get('pipe')
    if pipe is None:
        return HttpResponse("{\'message\":\"require parameter - pipe\"}", status=400)

    data = RawData.objects.filter(FK_Pipe_ID=pipe).last()
    serializer = RawDataSerializer(data)

    return Response(serializer.data)

@csrf_exempt
def PostData(request):
    if request.method == 'GET':
        return HttpResponse("{\"message\": \"Invalid GET Method\"}", status=400)
    if request.user is None:
        return HttpResponse("{\"message\": \"not allowed user session\"}", status=400)
    if request.user.is_authenticated() == False:
        return HttpResponse("{\"message\": \"Should be login\"}", status=400)

    temp = request.POST.get("Temp")
    value = request.POST.get("Data")
    pipe = request.POST.get("Pipe")


    if temp is None or value is None or pipe is None:
        return HttpResponse("{\"message\": \"parameter required Temp, Data, Pipe\"}", status=400)

    if Pipe.objects.filter(id = pipe, FK_User=request.user) is None:
        return HttpResponse("{\"message\": \"Invalid Pipe\"}", status=400)

    saved_average = HourData.objects.filter(id = pipe).last()

    add_data = RawData.objects.create(Temp = temp, Data = value, FK_Pipe_ID = Pipe.objects.filter(id=pipe).first())
    add_data.save()

    return HttpResponse("{\"message\": \"Success\"}")


