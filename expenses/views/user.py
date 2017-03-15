"""
      ______                       __         ______   __   ______
     /      \                     /  |       /      \ /  | /      \
    /$$$$$$  |  ______    _______ $$ |____  /$$$$$$  |$$ |/$$$$$$  | __   __   __
    $$ |  $$/  /      \  /       |$$      \ $$ |_ $$/ $$ |$$$  \$$ |/  | /  | /  |
    $$ |       $$$$$$  |/$$$$$$$/ $$$$$$$  |$$   |    $$ |$$$$  $$ |$$ | $$ | $$ |
    $$ |   __  /    $$ |$$      \ $$ |  $$ |$$$$/     $$ |$$ $$ $$ |$$ | $$ | $$ |
    $$ \__/  |/$$$$$$$ | $$$$$$  |$$ |  $$ |$$ |      $$ |$$ \$$$$ |$$ \_$$ \_$$ |
    $$    $$/ $$    $$ |/     $$/ $$ |  $$ |$$ |      $$ |$$   $$$/ $$   $$   $$/
     $$$$$$/   $$$$$$$/ $$$$$$$/  $$/   $$/ $$/       $$/  $$$$$$/   $$$$$/$$$$/

    File name: user.py
    Authors: Alexander Viklund <viklu@kth.se>
             Mauritz Zachrisson <mauritzz@kth.se>
    Python version: 3.5
"""

import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cashflow.dauth import has_permission
from expenses.models import Person


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class UserViewSet(GenericViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BaseSerializer
    lookup_field = 'username'
    lookup_value_regex = '[0-9a-z]+'

    """

    """
    def list(self, request, **kwargs):
        """
        List all usernames

        :param request:     HTTP request
        """
        return Response({'users': User.objects.all().values('username')})

    """
    Returns a JSON representation of the user with the specified username
    """
    def retrieve(self, request, username, **kwargs):
        print("Username: " + username)
        try:
            person = Person.objects.get(user__username=username)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if person.user is request.user or has_permission("pay", request):
            return Response({'user': person.to_dict()})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    """
    Returns a JSON representation of the current user
    """
    @list_route()
    def current(self, request, **kwargs):
        return Response({'user': Person.objects.get(user=request.user).to_dict()})

    """
    Update the user with the specified id with the bank information and settings from a JSON object
    """
    def partial_update(self, request, username, **kwargs):
        try:
            person = Person.objects.get(user__username=username)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if person.user is not request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            json_args = json.loads(request.PATCH['json'])

            if 'bank_account' in json_args:
                person.bank_account = json_args['bank_account']

            if 'sorting_number' in json_args:
                person.sorting_number = json_args['sorting_number']
            if 'bank_name' in json_args:
                person.bank_name = json_args['bank_name']
            if 'default_account' in json_args:
                person.default_account_id = json_args['default_account']

            person.save()
            return Response({'user': person.to_dict()})
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)