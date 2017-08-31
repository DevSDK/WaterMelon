from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import Pipe
from Data.serializer import RawDataSerializer, HourDataSerializer

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

    data = Pipe.objects.filter(FK_Pipe_ID=pipe)
    serializer = RawDataSerializer(data, many=True)

    return Response(serializer.data)


def GetListDay(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\":\"Invalid Method \"}", status=400)

    if not request.user.is_authenticated():
        return HttpResponse("{\"message\":\"Not authenticated\"}", status=401)

    pipe = request.GET.get('pipe')
    if pipe is None:
        return HttpResponse("{\'message\":\"invalid parameter - pipe\"}", status=400)
    datestr = request.GET.get('date')

    if datestr is None:
        return HttpResponse("{\'message\":\"invalid parameter - date\"}", status=400)

        date = datetime.datetime.strptime(datestr, "%Y-%m-%d").date()
        data = Pipe.objects.filter(FK_Device=pipe)
        endtime = date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        datedata = data.filter(Date__range=[date.strftime("%Y-%m-%d"), endtime.strftime("%Y-%m-%d")])
        serializer = HourDataSerializer(datedata, many=True)
    return Response(serializer.data)



def GetListYear(request):
    pass

