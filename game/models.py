from django.db import models

class SiteSettings(models.Model):
    footer_contact_text = models.CharField(max_length=100, verbose_name="Текст кнопки у футері", default="Зв'язатися з нами")
    footer_contact_link = models.URLField(verbose_name="Посилання на Telegram у футері", blank=True, null=True)

    def __str__(self):
        return "Глобальні налаштування сайту"

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (для посилання)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фільтр: Категорія"
        verbose_name_plural = "Фільтри: Категорії"

class PlayerCountRange(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Кількість гравців"
        verbose_name_plural = "Фільтри: Кількість гравців"

class AgeGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Вік"
        verbose_name_plural = "Фільтри: Вік"

class GameDuration(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Тривалість"
        verbose_name_plural = "Фільтри: Тривалість"

class PrepLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Рівень підготовки"
        verbose_name_plural = "Фільтри: Рівні підготовки"

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Місце проведення"
        verbose_name_plural = "Фільтри: Місця проведення"

class ActivityLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Рівень активності"
        verbose_name_plural = "Фільтри: Рівні активності"

class InteractionType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Тип взаємодії"
        verbose_name_plural = "Фільтри: Типи взаємодії"

class GameGoal(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Ціль гри"
        verbose_name_plural = "Фільтри: Цілі гри"

class ContentType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Тип контенту"
        verbose_name_plural = "Фільтри: Типи контенту"

class Thematic(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Фільтр: Тематика"
        verbose_name_plural = "Фільтри: Тематика"

class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категорія")
    description = models.TextField(verbose_name="Опис")
    telegram_link = models.URLField(blank=True, null=True, verbose_name="Посилання на Телеграм")
    rules = models.TextField(verbose_name="Правила гри")
    skill_developed = models.CharField(max_length=200, verbose_name="Навичка, яка розвивається", blank=True, null=True)
    
    # Нові фільтри
    players_range = models.ForeignKey(PlayerCountRange, on_delete=models.SET_NULL, null=True, verbose_name="Кількість гравців")
    age_group = models.ForeignKey(AgeGroup, on_delete=models.SET_NULL, null=True, verbose_name="Вік")
    duration = models.ForeignKey(GameDuration, on_delete=models.SET_NULL, null=True, verbose_name="Тривалість")
    prep_level = models.ForeignKey(PrepLevel, on_delete=models.SET_NULL, null=True, verbose_name="Рівень підготовки")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name="Місце проведення")
    activity_level = models.ForeignKey(ActivityLevel, on_delete=models.SET_NULL, null=True, verbose_name="Рівень активності")
    interaction_type = models.ForeignKey(InteractionType, on_delete=models.SET_NULL, null=True, verbose_name="Тип взаємодії")
    goal = models.ForeignKey(GameGoal, on_delete=models.SET_NULL, null=True, verbose_name="Ціль гри")
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, verbose_name="Тип контенту")
    thematic = models.ForeignKey(Thematic, on_delete=models.SET_NULL, null=True, verbose_name="Тематика")

    # Кнопки та посилання
    tg_link = models.URLField(blank=True, null=True, verbose_name="Посилання на Телеграм")
    tg_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Текст кнопки Телеграм", default="Перейти в чат гри")
    
    show_tg = models.BooleanField(default=True, verbose_name="Показувати кнопку Телеграм")
    
    external_link = models.URLField(blank=True, null=True, verbose_name="Посилання на зовнішню гру")
    external_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Текст кнопки зовнішньої гри", default="Грати онлайн")
    show_external = models.BooleanField(default=False, verbose_name="Показувати кнопку зовнішньої гри")

    insta_link = models.URLField(blank=True, null=True, verbose_name="Посилання на Instagram")
    insta_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Текст кнопки Instagram", default="Instagram")
    show_insta = models.BooleanField(default=False, verbose_name="Показувати кнопку Instagram")

    youtube_link = models.URLField(blank=True, null=True, verbose_name="Посилання на YouTube")
    youtube_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Текст кнопки YouTube", default="YouTube")
    show_youtube = models.BooleanField(default=False, verbose_name="Показувати кнопку YouTube")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Гра"
        verbose_name_plural = "Ігри"
