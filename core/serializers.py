from rest_framework import serializers
from .models import Person, Union


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'photo', 'created_at']


class TreeUnionSerializer(serializers.ModelSerializer):
    partner_1 = serializers.UUIDField(source='partner_1_id')
    partner_2 = serializers.UUIDField(source='partner_2_id', allow_null=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Union
        fields = ['id', 'partner_1', 'partner_2', 'children']

    def get_children(self, obj):
        return [str(link.child_id) for link in obj.children.all()]
