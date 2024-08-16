from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import F


from user.models import MyUser
from .models import Cap, Banner, Brand
from .serializers import (
    CapListSerializer, BannerListSerializer, BrandListSerializer, DiscountListSerializer,
    CapDetailSerializer, UserProfilSerializer, UserProfilUpdateSerializer
)


class CapListViews(APIView):
    def get(self, request):
        banners = Banner.objects.all()

        brands = Brand.objects.all()

        bestsellers_caps = Cap.objects.all()

        special_caps = Cap.objects.filter(discount_price__lt=F('price'))

        # if 'search' in request.GET:
        #     search = request.GET.get('search')
        #     special_caps = search.filter()

        banners_serializers = BannerListSerializer(banners, many=True)
        brands_serializers = BrandListSerializer(brands, many=True)
        bestsellers_serializers = CapListSerializer(bestsellers_caps, many=True)
        discount_serializers = DiscountListSerializer(special_caps, many=True)

        data = {
            'banners': banners_serializers.data,
            'brands': brands_serializers.data,
            'bestsellers_caps': bestsellers_serializers.data,
            'special_caps': discount_serializers.data
        }

        return Response(data)


class CapDetailViews(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Cap, id=pk)

        categories = product.category.all()

        recommendations = Cap.objects.filter(category__in=categories).exclude(id=pk).distinct()

        serializer = CapDetailSerializer(product)
        recommendations_serializer = CapListSerializer(recommendations, many=True)

        data = {
            'product': serializer.data,
            'recommendations': recommendations_serializer.data,
        }

        return Response(data)

    def delete(self, request, pk):
        product = get_object_or_404(Cap, id=pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserProfilViews(APIView):
    def get(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfilSerializer(user)

        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfilUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
