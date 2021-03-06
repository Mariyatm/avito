import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from avito import settings
from users.models import User, Location
from users.serializers import LocationSerializer, UserCreateSerializer


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request,  *args, **kwargs)

        search_text = request.GET.get("username", None)
        if search_text:
            self.object_list = self.object_list.filter(username=search_text)

        self.object_list = self.object_list.prefetch_related("locations").order_by("username")

        user_qs = self.object_list.annotate(total_ads=Count("ad"))
        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                # "first_name": user.first_name,
                # "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
                "total_ads":user.total_ads,
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
        })



class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name",  "age",  "username"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.first_name = ad_data["first_name"]
        self.object.last_name = ad_data["last_name"]
        self.object.last_name = ad_data["age"]

        user = self.object
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all())),
        })


class LocationsViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer