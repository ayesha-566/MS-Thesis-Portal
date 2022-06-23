from rest_framework import serializers
from Thesis.models import Thesis,Domain,DomainInfo,Conference

class ThesisSerializer(serializers.ModelSerializer):
    class Meta:
        model=Thesis
        fields="__all__"
    
class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model=Domain
        fields="__all__"

class DomainInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=DomainInfo
        fields="__all__"

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Conference
        fields="__all__"

