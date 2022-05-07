import json

from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from ads.models import Ad, Cat
from ads.serializers import AdDetailSerializer, AdListSerializer, AdCreateSerializer


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    def get(self, request, *args, **kwargs):
        cats = request.GET.getlist("cat", None)
        cats_q = None
        for cat in cats:
            if cats_q is None:
                cats_q = Q(category__name__icontains=cat)
            else:
                cats_q |= Q(category__name__icontains=cat)
        if cats_q:
            self.queryset = self.queryset.filter(cats_q)

        search_text = request.GET.get("text", None)
        if search_text:
            self.queryset = self.queryset.filter(
                name__icontains=search_text
            )

        search_location = request.GET.get("location", None)
        if search_location:
            self.queryset = self.queryset.filter(
                user__locations__name__icontains=search_location
            )

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


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



