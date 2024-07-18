from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,Order,OrderItem,ShippingAddress,Review
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True) #It is used when you want to include a custom field in a serializer class that does not correspond directly to a model attribute but instead requires custom logic to determine its value.
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin']
    def get_name(self,obj): #overriding i.e returning custom attribute name The function overrides the default behavior of serializing the name attribute of an object (obj) with custom logic.This is useful when you want to customize how specific attributes of an object are serialized into JSON or other formats, based on certain conditions or requirements.
        name=obj.first_name
        if name=='':
            name=obj.email
        return name
    def get__id(self,obj): #overriding i.e returning custom attribute
        return obj.id
    def get_isAdmin(self,obj):
        return obj.is_staff

class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin','token']
    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)


class ReviewSeerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer): #this will trunout data into json format
    reviews=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Product
        fields='__all__'
    
    def get_reviews(self,obj):
        reviews = obj.review_set.all() #here obj means product model i.e product.review_set.all()
        #This is Django’s way of accessing related objects through reverse relationships. When you have a foreign key relationship (e.g., Review has a foreign key to Product), Django automatically creates a related manager on the Product model.In this case, review_set allows you to access all Review instances that are linked to the specific Product instance.
        #In review_set, the review part refers to the related model name, which in this case is Review.By default, Django appends _set to the lowercase name of the related model. So if your model is named Review, the reverse relationship from Product would be accessed using review_set.
        serializer = ReviewSeerializer(reviews, many=True)
        return serializer.data
        
        
        
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        #This is Django’s way of accessing related objects through reverse relationships. When you have a foreign key relationship (e.g., OrderItem has a foreign key to Order), Django automatically creates a related manager on the Order model.In this case, orderitem_set allows you to access all OrderItem instances that are linked to the specific Order instance.
        #In orderitem_set, the orderitem part refers to the related model name, which in this case is OrderItem.By default, Django appends _set to the lowercase name of the related model. So if your model is named OrderItem, the reverse relationship from Order would be accessed using orderitem_set.
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
            # you're retrieving the shipping address details (like address, city, postal code, etc.) for that particular order.
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
