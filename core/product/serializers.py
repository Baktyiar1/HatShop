from rest_framework import serializers

from .models import Cap, Category, Banner, Image, Brand, Size, Cart



class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'




class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title',)


class CapIndexSerializer(serializers.ModelSerializer):

    category = CategoryListSerializer(many=True)

    class Meta:
        model = Cap
        fields = (
            'id',
            'title',
            'price',
            'discount_price',
            'category',
            'logo'
        )



class DiscountListSerializer(serializers.ModelSerializer):

    category = CategoryListSerializer(many=True)


    class Meta:
        model = Cap
        fields = (
            'id',
            'title',
            'price',
            'discount_price',
            'category',
            'logo',
        )

    def to_representation(self, instance):
        # Проверяем условие внутри представления данных
        if instance.discount_price and instance.discount_price < instance.price:
            return super().to_representation(instance)
        return None

class CapCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cap
        fields = (
            'title',
            'description',
            'logo',
            'price',
            'discount_price',
            'category',
            'sizes',
            'images',
            'brands',
        )


class ImageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id',
                  'image'
                  )


class SizeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ('name',)

class CapDetailSerializer(serializers.ModelSerializer):

    category = CategoryListSerializer(many=True)
    images = ImageDetailSerializer(many=True)
    brands = BrandSerializer(many=True)
    sizes = SizeDetailSerializer(many=True)

    class Meta:
        model = Cap
        fields = (
            'category',
            'sizes',
            'images',
            'brands',
            'title',
            'description',
            'logo',
            'price',
            'discount_price',
            'created_date'
        )

class CapDetailUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cap
        fields = (
            'title',
            'description',
            'logo',
            'price',
            'discount_price'
        )


class CapListSerializer(serializers.ModelSerializer):

    category = CategoryListSerializer(many=True)
    class Meta:
        model = Cap
        fields = (
            'id',
            'title',
            'price',
            'discount_price',
            'category',
            'logo',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Проверяем, если скидки нет, то удаляем discount_price из данных
        if not instance.discount_price or instance.discount_price >= instance.price:
            representation.pop('discount_price', None)

        return representation

class CartCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Cart
        fields = (
            'user',
            'cap',
            'quantity',
            'address'
        )
