from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Person, Union, ParentChild
from .serializers import PersonSerializer, TreeUnionSerializer


@api_view(['GET'])
def get_tree(request):
    people = Person.objects.all()
    unions = Union.objects.prefetch_related('children').all()
    return Response({
        'people': PersonSerializer(people, many=True, context={'request': request}).data,
        'unions': TreeUnionSerializer(unions, many=True).data,
    })


def _optional_photo(request):
    photo = request.data.get('photo')
    if photo in (None, '', 'undefined', 'null'):
        return None
    return photo


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_relative(request):
    name = (request.data.get('name') or '').strip()
    relation_type = request.data.get('relation_type')
    target_person_id = request.data.get('target_person_id')
    union_id = request.data.get('union_id')

    if not name or not target_person_id or not relation_type:
        return Response(
            {'error': 'name, target_person_id, and relation_type are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if relation_type not in ('spouse', 'child'):
        return Response({'error': 'relation_type must be spouse or child.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        target_person = Person.objects.get(id=target_person_id)
    except Person.DoesNotExist:
        return Response({'error': 'Target person not found.'}, status=status.HTTP_404_NOT_FOUND)

    new_person = Person.objects.create(name=name, photo=_optional_photo(request))

    if relation_type == 'spouse':
        Union.objects.create(partner_1=target_person, partner_2=new_person)
    else:
        if union_id:
            try:
                union = Union.objects.get(id=union_id)
            except Union.DoesNotExist:
                new_person.delete()
                return Response({'error': 'Union not found.'}, status=status.HTTP_404_NOT_FOUND)
            if union.partner_1_id != target_person.id and union.partner_2_id != target_person.id:
                new_person.delete()
                return Response(
                    {'error': 'Union does not include the target person.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            union = Union.objects.create(partner_1=target_person, partner_2=None)

        ParentChild.objects.create(union=union, child=new_person)

    serializer = PersonSerializer(new_person, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def create_person(request):
    name = (request.data.get('name') or '').strip()
    if not name:
        return Response({'error': 'name is required.'}, status=status.HTTP_400_BAD_REQUEST)

    person = Person.objects.create(name=name, photo=_optional_photo(request))
    serializer = PersonSerializer(person, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_person(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found.'}, status=status.HTTP_404_NOT_FOUND)

    person.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@ensure_csrf_cookie
def tree_view(request):
    return render(request, 'index.html')
