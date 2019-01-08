from rest_framework import viewsets
from .models import People
from .serializers import PeopleSerializer

class PeopleViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a collaborator instance.

    list:
        Return all people, ordered by most recently joined.

    create:
        Create a new collaborator.

    delete:
        Remove an existing collaborator.

    partial_update:
        Update one or more fields on an existing collaborator.

    update:
        Update a collaborator.
    """
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

