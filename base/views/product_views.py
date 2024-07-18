from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from base.models import Product,Review
from base.serializers import ProductSerializer
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from rest_framework import status

# @api_view(['GET'])

# def getProducts(request):
#     return Response(products)
@api_view(['GET'])
def getProducts(request):
    # Retrieve the 'keyword' from the query parameters
    query = request.query_params.get('keyword')
    
    if query is None:
        query = ''
    
    # Filter products based on the keyword; 
    # This searches the Product table for all entries 
    # where the name field contains the substring specified by query
    
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def getTopProducts(request):
        #products=Product.objects.filter(rating__gt=4).order_by('-rating')[0:5]

    products = Product.objects.all()
    ratings = [product.rating for product in products]
    ratings.sort(reverse=True)  # Sort ratings in descending order
    
    # Get top 4 products based on ratings
    top_products = Product.objects.filter(rating__in=ratings[:4])
    
    serializer = ProductSerializer(top_products, many=True)
    return Response(serializer.data)







@api_view(['GET'])
# def getSingle(request,pk):
#     product=None
#     for i in products:
#         if i['_id']==pk:
#             product=i
#             break
#     return Response(product)
def getSingle(request,pk):
    product=Product.objects.get(_id=pk)
    serializer=ProductSerializer(product,many=False) #one product so many=false
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user=request.user
    data=request.data
    product=Product.objects.create(
        # user=user
        # name=data['name']
        # price=data['price']
        # description=data['description']
        # category=data['category']
        # brand=data['brand']
        # countInStock=data['countInStock']
        user=user,
        name='Sample name',
        price=29.99,
        description='Sample description',
        category='Sample category',
        brand='Sample brand',
        countInStock=1
    )
    serializer=ProductSerializer(product,many=False) #one product so many=false
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request,pk):
    data=request.data
    product=Product.objects.get(_id=pk)
    
    product.name=data['name']
    product.price=data['price']
    product.description=data['description']
    product.category=data['category']
    product.brand=data['brand']
    product.countInStock=data['countInStock']
    product.save()
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)




@api_view(['DELETE'])

def deleteProduct(request,pk):
    product=Product.objects.get(_id=pk)
    product.delete()
    return Response('product Deleted')


@api_view(['POST'])

def uploadImage(request):
    data=request.data
    product_id=data['product_id']
    product=Product.objects.get(_id=product_id)
    product.image=request.FILES.get('image')
    product.save()
    return Response('Image Uploaded')



#reviews

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    data = request.data
    product = Product.objects.get(_id=pk)
    
    # 1. Check if review already exists
    already_exists = product.review_set.filter(user=user).exists()
    if already_exists:
        content = {'detail': 'Review already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. Check if rating exists or is 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 3. Create a new review
    else:
        review = Review.objects.create(
            user = user,
            product = product,
            name = user.first_name,
            rating = data['rating'],
            comment = data['comment']
        )
        reviews = product.review_set.all()  # to know how many reviews a product has
        product.numReviews = len(reviews)
        
        total = 0
        for i in reviews:
            total += i.rating
        
        product.rating = total / len(reviews)
        product.save()
        return Response('Review Added')
