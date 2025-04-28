# app_blog/urls.py
from django.urls import path

# Імпортуємо представлення, які створимо пізніше
from .views import (HomePageView, ArticleDetail,
                    ArticleList, ArticleCategoryList)

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # URL для головної сторінки (вже був)
    path(r'', HomePageView.as_view(), name='home'),

    # URL для списку всіх публікацій
    path(r'articles/', ArticleList.as_view(), name='articles-list'),

    # URL для списку публікацій за категоріями (використовуємо slug категорії)
    path(r'articles/category/<slug:slug>/', ArticleCategoryList.as_view(), name='articles-category-list'), # Змінено <slug> на <slug:slug> для іменованого захоплення

    # URL для детальної сторінки окремої публікації (використовуємо рік, місяць, день та slug)
    path(r'articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', ArticleDetail.as_view(), name='news-detail'), # Змінено типи захоплення та імена
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)