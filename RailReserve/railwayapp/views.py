from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


def mainpage(request):
    return render(request, "railwayapp/main.html", {'u' : request.user, 'a':False})

def loginpage(request):
    return render(request, "railwayapp/login.html", {'u' : request.user})

def registerpage(request):
    return render(request, "railwayapp/register.html", {'u' : request.user})

def logoutpage(request):
    return render(request, "railwayapp/main.html", {'a' : True})

def historypage(request):
    return render(request, "railwayapp/history.html")

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)

class TrainRouteView(generics.ListAPIView):
    queryset = models.Station.objects.none()
    serializer_class = serializers.StationSerializer
    lookup_field = 'train_name'

    def get_queryset(self):
        
        print(self.kwargs.get(self.lookup_field))
        queryset = models.Station.objects.raw(
            "select station_id, station_name " \
            "from Station natural join Route natural join Train " \
            "where train_name = %s " \
            "order by id",
            (self.kwargs.get(self.lookup_field),),
        )
        return queryset

class TicketHistoryView(generics.ListAPIView):
    queryset = models.Ticket2.objects.none()
    serializer_class = serializers.TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Ticket2.objects.filter(user = self.request.user)

# class TicketView(ListView):
#     model = models.Ticket2
#     # queryset = models.Ticket2.objects.none()
#     # serializer_class = serializers.TicketSerializer
#     permission_classes = []

#     def get_queryset(self):
#         return models.Ticket2.objects.filter(user = self.request.user)

class GeneralSearchView(generics.ListAPIView):
    queryset = models.Train.objects.all()
    serializer_class = serializers.TrainSerializer

    def get_queryset(self):
        train_type = (self.request.data.get("train_type") or "")[:1]
        station_a = (self.request.data.get("station_a") or "")[:30]
        station_b = (self.request.data.get("station_b") or "")[:30]
        print((train_type,station_a,station_b))
        return models.Train.objects.raw(
            "call general_search(%s,%s,%s)",
            (train_type,station_a,station_b),
        )

class GeneralSearch(ListView):
    model = models.Train
    template_name = "railwayapp/search.html"
    # serializer_class = serializers.TrainSerializer

    def get_queryset(self):
        # print(self.request.body)
        print(self.request.GET)
        # data = json.loads(self.request.body)
        data = self.request.GET
        train_type = (data.get("train_type") or "")[:1]
        station_a = (data.get("station_a") or "")[:31]
        station_b = (data.get("station_b") or "")[:31]
        print((train_type,station_a,station_b))
        return models.Train.objects.raw(
            "call general_search(%s,%s,%s)",
            (train_type,station_a,station_b),
        )

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['d_date'] = self.request.GET.get("date")
        return context

# class GeneralSearch2(ListView):
#     model = models.Trainstatus2
#     template_name = "railwayapp/search.html"
#     # serializer_class = serializers.TrainSerializer

#     def get_queryset(self):
#         # print(self.request.body)
#         print(self.request.GET)
#         # data = json.loads(self.request.body)
#         data = self.request.GET
#         train_type = (data.get("train_type") or "")[:1]
#         station_a = (data.get("station_a") or "")[:30]
#         station_b = (data.get("station_b") or "")[:30]
#         date = (data.get("date") or "")[:30]
#         print((train_type,station_a,station_b))
#         qs = models.Train.objects.raw(
#             "call general_search(%s,%s,%s)",
#             (train_type,station_a,station_b),
#         )
#         return models.Trainstatus2.objects.filter(train__in = qs, departure_date = date)


class TrainRoute(ListView):
    model = models.Station
    template_name = 'railwayapp/schedule.html'
    # queryset = models.Station.objects.none()
    # serializer_class = serializers.StationSerializer
    # lookup_field = 'train_name'

    def get_queryset(self):
        data = self.request.GET
        # print(self.kwargs.get(self.lookup_field))
        queryset = models.Station.objects.raw(
            "select station_id, station_name " \
            "from Station natural join Route natural join Train " \
            "where train_name = %s " \
            "order by id",
            (data.get('train_name'),),
        )
        return queryset

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_ticket(request):
    print(request.data)
    train_name = request.data.get('train_name')
    date = request.data.get('date')
    obj = models.Trainstatus2.objects.get(train__train_name=train_name,departure_date=date)
    
    if obj is not None:
        if obj.seats_booked < obj.total_seats:
            print("Confirmed")
            models.Trainstatus2.objects.filter(pk = obj.pk).update(seats_booked = F('seats_booked') + 1)
            print("P2")
            models.Ticket2.objects.create(
                user=request.user, ticket_status="C",
                seat_cost=obj.seat_cost, seat_no=obj.seats_booked,
                trainstatus_id=obj,
            )
            return Response(data={},status=status.HTTP_201_CREATED)
        else:
            print("Waiting")
            models.Trainstatus2.objects.filter(pk = obj.pk).update(seats_booked = F('seats_booked') + 1)
            print("P2")
            models.Ticket2.objects.create(
                user=request.user, ticket_status="W",
                seat_cost=obj.seat_cost, seat_no=obj.seats_booked,
                trainstatus_id=obj,
            )
            return Response(data={},status=status.HTTP_201_CREATED)
    else:
        return Response(data={"error":"Bad data"},status=status.HTTP_400_BAD_REQUEST)
    
    # s = serializers.TicketCreationSerializer(data = )
