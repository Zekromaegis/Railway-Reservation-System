from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from railwayapp import models

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ('user',)
    
class RegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','profile']
        extra_kwargs = {
            'password' : {
                'write_only':True,
                'style': {'input_type':'password'},
            }
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        profile_data = validated_data.pop('profile')
        obj = super().create(validated_data)
        models.Profile.objects.create(user=obj, **profile_data)
        return obj

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = '__all__'

class TicketCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket2
        fields = '__all__'

class TrainSerializer(serializers.ModelSerializer):
    start_station = StationSerializer()
    end_station = StationSerializer()

    class Meta:
        model = models.Train
        fields = '__all__'

class TrainStatusSerializer(serializers.ModelSerializer):
    train = TrainSerializer()

    class Meta:
        model = models.Trainstatus2
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    trainstatus_id = TrainStatusSerializer()

    class Meta:
        model = models.Ticket2
        exclude = ("user", "ticket_id")