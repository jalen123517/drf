from django.urls import path, re_path
from collect import views

urlpatterns = [
    # 不要在同一个路由的as_view中书写两个同样的键的http请求，会产生覆盖！！！
    # ViewSet
    path('student1/', views.Student1ViewSet.as_view({"get": "get_5"})),
    path('student1/get_3_girl/', views.Student1ViewSet.as_view({"get": "get_3_girl"})),
    re_path(r'^student1/(?P<pk>\d+)/$', views.Student1ViewSet.as_view({"get": "get_one"})),

    # GenericViewSet
    path('student2/', views.Student3GenericViewSet.as_view({"get": "get_5"})),
    path('student2/get_3_girl/', views.Student3GenericViewSet.as_view({"get": "get_3_girl"})),
    # GenericViewSet，可以和模型类进行组合快速生成基本的API接口
    path("student3/", views.Student4GenericViewSet.as_view({'get': "list", "post": 'create'})),
    # ModelViewSet 默认提供了5个API接口
    path('student4/', views.Student5ModelViewSet.as_view({'get': "list", "post": 'create'})),
    re_path(r'^student4/(?P<pk>\d+)/$', views.Student5ModelViewSet.as_view({"get": 'retrieve', "put": "update", "delete": "destroy"})),
    # ReadOnlyModelViewSet
    path('student5/', views.Student6ReadOnlyModelViewSet.as_view({"get": "list"})),
    re_path(r'^student5/(?P<pk>\d+)/$', views.Student6ReadOnlyModelViewSet.as_view({"get": 'retrieve'})),

    # 一个视图类中调用多个序列化器
    path("student8/", views.Student8GenericAPIView.as_view()),

    # 一个视图集中调用多个序列化器
    path("student9/", views.Student9ModelViewSet.as_view({"get": "list"})),
    re_path(r"^student9/(?P<pk>\d+)/$", views.Student9ModelViewSet.as_view({"get": "retrieve"})),
]

from rest_framework.routers import DefaultRouter, SimpleRouter

# router = SimpleRouter()
router = DefaultRouter()  # 多了API——root

router.register("student6", views.Student7ModelViewSet)


# print("@@@@", router.urls)

urlpatterns += router.urls
