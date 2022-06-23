from rest_framework import serializers
from Faculty.models import Faculty,Comment,CommitteeMember,Suggested_topics


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model=Faculty
        fields="__all__"

class CommitteeMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommitteeMember
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"

class SugestedTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Suggested_topics
        fields="__all__"