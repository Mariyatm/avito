import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Cat
from avito import settings
from users.models import User


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request,  *args, **kwargs)

        search_text = request.GET.get("name", None)
        if search_text:
            self.object_list = self.object_list.filter(name=search_text)

        self.object_list = self.object_list.select_related("user").order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.user.username,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            "id": ad.id,
            "author_id": ad.user_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data['description'],
            is_published=ad_data['is_published']
        )
        ad.category = get_object_or_404(Cat, pk=ad_data["category_id"])
        ad.user = get_object_or_404(User, pk=ad_data["author_id"])
        ad.save()

        return  JsonResponse({
            "name": ad.name,
            "id": ad.id,
            "author_id": ad.user_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.name=ad_data["name"]
        self.object.price=ad_data["price"]
        self.object.description=ad_data['description']
        self.object.is_published=ad_data['is_published']
        self.object.save()

        return  JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.user_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "image": self.object.image.url if self.object.image else None,
        })


class CatListView(ListView):
    model = Cat

    def get(self, request, *args, **kwargs):
        super().get(request,  *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        response = []
        for cat in self.object_list.all():
            response.append({
                "id": cat.id,
                "name": cat.name,
            })
        return JsonResponse(response, safe=False)

class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Cat
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        cat = Cat.objects.create(
            name=ad_data["name"],
        )
        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Cat
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })



