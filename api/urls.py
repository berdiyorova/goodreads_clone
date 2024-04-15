from django.urls import path

from api.views import BookReviewDetailAPIView, BookReviewListAPIView

#--------------------------------------------------------------------------------------------------------------------
#                       Viewset lardan foydalanilganda
from rest_framework.routers import DefaultRouter

# from api.views import BookReviewViewSet


app_name = 'api'
urlpatterns = [
    path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='review_detail'),
    path('reviews/', BookReviewListAPIView.as_view(), name='review_list'),
]

# router = DefaultRouter()
# router.register('reviews', BookReviewViewSet, basename='review')
# urlpatterns = router.urls
