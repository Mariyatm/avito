
from rest_framework import serializers

from ads.models import Ad, Selection


class AdListSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=20)
    class Meta:
        model = Ad
        fields = ["id", "name", "price", "is_published", "username"]


class AdSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Ad
        fields = ["id", "name", "price", "is_published"]

class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["name", "price", "is_published"]


class AdDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = "__all__"


class  SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"



    # name = models.CharField(max_length=50)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # price = models.IntegerField()
    # description = models.CharField(max_length=1500, null=True)
    # is_published = models.BooleanField()
    # image = models.ImageField(upload_to='images/', null=True)
    # category = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)