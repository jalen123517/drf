from django.urls import path, re_path
from ser import views


urlpatterns = [
    # 来反去序
    # 序列化操作（响应时）
    re_path(r"student/(?P<pk>\d+)/", views.Student1View.as_view()),  # 返回一条数据
    re_path(r"student/", views.Student2View.as_view()),  #　返回所有数据

    # 数据校验
    path('student3/', views.Student3View.as_view()),
    re_path(r'^student3/(?P<pk>\d+)/$', views.Student3View.as_view()),

    # 合并使用序列化器
    path('student4/', views.Student4View.as_view()),
    re_path(r'^student4/(?P<pk>\d+)/$', views.Student5View.as_view()),

    # 模型类序列化器类
    path("student5/", views.Student6View.as_view()),
    re_path(r'^student5/(?P<pk>\d+)/$', views.Student7View.as_view()),
]