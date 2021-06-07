from django.contrib.auth.models import User
from django.http import HttpResponse
from .serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer
from .models import MainCycle, Boost
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import services


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CycleList(generics.ListAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializer


class BoostList(generics.ListAPIView):
    queryset = Boost
    serializer_class = BoostSerializer
    def get_queryset(self):
        return Boost.objects.filter(main_cycle=self.kwargs['main_cycle'])


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail


class CycleDetail(generics.RetrieveAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializerDetail


@api_view(['POST'])
def upgrade_boost(request):
    main_cycle, level, price, power = services.clicker_services.upgrade_boost(request)
    return Response({'click_power': main_cycle.click_power,
                     'coins_count': main_cycle.coins_count,
                     'auto_click_power': main_cycle.auto_click_power,
                     'level': level,
                     'price': price,
                     'power': power})


@api_view(['POST'])
def set_main_cycle(request):
    coins_count, boosts = services.clicker_services.set_main_cycle(request)
    return Response({"coins_count": coins_count,
                     "boosts": boosts})
