# app_blog/views.py
from django.shortcuts import render, get_object_or_404 # Додано get_object_or_404, хоча в прикладі views його немає, але часто використовується з DetailView
from django.views.generic import TemplateView, ListView, DateDetailView

from .models import Article, Category # Імпортуємо Category також

# Оновлене представлення для головної сторінки
class HomePageView(ListView):
    model = Category # В цьому варіанті HomePageView використовує модель Category
    template_name = 'index.html'
    context_object_name = 'categories' # Змінено назву змінної контексту

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Використовуйте super().get_context_data()
        # Додаємо до контексту 5 найновіших статей, позначених як main_page=True
        context['articles'] = Article.objects.filter(main_page=True).order_by('-pub_date')[:5] # Додано order_by для сортування
        return context

    def get_queryset(self, *args, **kwargs):
        # Повертаємо всі категорії для відображення на головній
        categories = Category.objects.all()
        return categories


# Представлення для детальної сторінки окремої статті
class ArticleDetail(DateDetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'item' # Змінна, під якою об'єкт статті буде доступний в шаблоні
    date_field = 'pub_date' # Поле моделі, яке використовується для дати в URL
    query_pk_and_slug = True # Дозволяє використовувати slug та primary key в URL
    month_format = '%m' # Формат місяця в URL
    allow_future = True # Дозволяє відображати статті з майбутньою датою публікації

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs) # Використовуйте super().get_context_data()
        try:
            # Додаємо до контексту зображення, пов'язані зі статтею
            context['images'] = context['item'].images.all()
        except:
            pass # Якщо зображень немає, просто пропускаємо

        return context


# Представлення для списку всіх статей
class ArticleList(ListView):
    model = Article
    template_name = 'articles_list.html'
    context_object_name = 'items' # Змінна, під якою список статей буде доступний в шаблоні
    # За замовчуванням ListView повертає всі об'єкти моделі, але ми можемо перевизначити get_queryset

    def get_queryset(self, *args, **kwargs):
        # Повертаємо всі статті, відсортовані за датою публікації
        articles = Article.objects.all().order_by('-pub_date') # Додано order_by для сортування
        return articles

    # Метод get_context_data з документа для ArticleList виглядає, ніби він призначений для ArticleCategoryList.
    # Якщо цей код викликає помилку або виглядає зайвим для списку всіх статей, можливо, його потрібно прибрати або перенести.
    # Згідно з документом, цей метод додає об'єкт категорії до контексту, що логічніше для списку статей за категорією.
    # Тому залишимо його, але майте на увазі його призначення.
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs) # Використовуйте super().get_context_data()
        try:
            # Спроба отримати категорію зі slug з URL.
            # Це потрібно, якщо ArticleList використовується як базова в ArticleCategoryList.
            # Якщо ArticleList використовується сам по собі, цей блок може викликати помилку, якщо в URL немає slug.
            # Або ж документ має на увазі, що ArticleList завжди використовується у спадок.
            context['category'] = Category.objects.get(
                slug=self.kwargs.get('slug')) # Може викликати помилку, якщо slug немає в self.kwargs
        except Exception:
            context['category'] = None
        return context


# Представлення для списку статей за певною категорією
class ArticleCategoryList(ArticleList): # Успадковуємось від ArticleList
    # template_name та context_object_name успадковуються від ArticleList

    def get_queryset(self, *args, **kwargs):
        # Фільтруємо статті за slug категорії, отриманим з URL
        articles = Article.objects.filter(
            category__slug=self.kwargs['slug'] # Виправлено category_slug_in на category__slug для фільтрації за полем slug зв'язаної категорії
        ).order_by('-pub_date') # Додано order_by для сортування
        # .distinct() # .distinct() може бути корисним, якщо є дублювання, але зазвичай не потрібен при фільтрації за ForeignKey

        return articles