from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter

from django.db.models import F, Q


from .models import Cap, Banner, Brand, Cart
from .serializers import (
    CapIndexSerializer, BannerListSerializer, BrandSerializer, DiscountListSerializer,
    CapDetailSerializer, CapListSerializer,
    CapDetailUpdateSerializer, CapCreateSerializer, CartCreateSerializer
)
from .filters import CapFilter


class CapIndexViews(APIView):

    def get(self, request):
        banners = Banner.objects.all().order_by('-id')

        brands = Brand.objects.all().order_by('-id')

        bestsellers_caps = Cap.objects.all().order_by('-id')

        special_caps = Cap.objects.filter(discount_price__lt=F('price'))


        if 'search' in request.GET:
            search = request.GET.get('search')
            bestsellers_caps = bestsellers_caps.filter(title__icontains=search)


        banners_serializers = BannerListSerializer(banners, many=True)
        brands_serializers = BrandSerializer(brands, many=True)
        bestsellers_serializers = CapIndexSerializer(bestsellers_caps, many=True)
        discount_serializers = DiscountListSerializer(special_caps, many=True)

        special_caps_data = [item for item in discount_serializers.data if item is not None]

        data = {
            'banners': banners_serializers.data,
            'brands': brands_serializers.data,
            'bestsellers_caps': bestsellers_serializers.data,
            'special_caps': special_caps_data
        }

        return Response(data)


class BrandListView(APIView):
    @swagger_auto_schema(responses={200: CapListSerializer()})
    def get(self, request, *args, **kwargs):
        brand_name = request.GET.get('brand')
        if brand_name:
            caps = Cap.objects.filter(brands__title=brand_name)
        else:
            caps = Cap.objects.all()

        serializer = CapListSerializer(caps, many=True)
        return Response(serializer.data)



class Bestsellers_capsListView(generics.ListAPIView):
    queryset = Cap.objects.all()
    serializer_class = CapIndexSerializer


class Special_capsListView(generics.ListAPIView):
    serializer_class = DiscountListSerializer

    def get_queryset(self):
        # Основной фильтр по скидке, использующий фильтрацию на уровне базы данных
        return Cap.objects.filter(discount_price__lt=F('price'))

    def list(self, request, *args, **kwargs):
        # Получаем стандартный ответ
        response = super().list(request, *args, **kwargs)

        # Исключаем объекты, где сериализация вернула None
        response.data = [item for item in response.data if item is not None]
        return response


class CapDetailViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cap.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CapDetailSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return CapDetailUpdateSerializer


    def get(self, request, *args, **kwargs):
        product = self.get_object()

        categories = product.category.all()

        recommendations = Cap.objects.filter(category__in=categories).exclude(id=product.id).distinct()

        serializer = CapDetailSerializer(product)
        recommendations_serializer = CapListSerializer(recommendations, many=True)

        data = {
            'product': serializer.data,
            'recommendations': recommendations_serializer.data,
        }

        return Response(data)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Cap, id=pk)
    #     product.delete()
    #
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class CapUpdateAPIView(generics.UpdateAPIView):
#     queryset = Cap.objects.all()
#     serializer_class = CapDetailSerializer



class CapListAPIView(generics.ListAPIView):

    serializer_class = CapListSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CapFilter
    ordering_fields = ['created_date', 'price']
    search_fields = ['title']

    def get_queryset(self):

        queryset = Cap.objects.filter(discount_price__lt=F('price'), is_active=True)

        return queryset


class CapCreateAPIView(generics.CreateAPIView):
    queryset = Cap.objects.all()
    serializer_class = CapCreateSerializer

class CartCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer


