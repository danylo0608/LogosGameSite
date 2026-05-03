from django.contrib import admin
from .models import (
    Game, Category, PlayerCountRange, AgeGroup, GameDuration,
    PrepLevel, Location, ActivityLevel, InteractionType, GameGoal, ContentType, Thematic,
    SiteSettings
)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'footer_contact_text', 'footer_contact_link')

    def has_add_permission(self, request):
        # Дозволити додавати лише якщо об'єктів ще немає
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PlayerCountRange)
class PlayerCountRangeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(GameDuration)
class GameDurationAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PrepLevel)
class PrepLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ActivityLevel)
class ActivityLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(InteractionType)
class InteractionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(GameGoal)
class GameGoalAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Thematic)
class ThematicAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'goal', 'thematic', 'age_group', 'players_range')
    list_filter = (
        'category', 'goal', 'thematic', 'age_group', 'players_range', 
        'duration', 'prep_level', 'location', 'activity_level', 
        'interaction_type', 'content_type'
    )
    search_fields = ('title', 'description', 'skill_developed')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'rules')
        }),
        ('Кнопки та посилання', {
            'fields': (
                ('show_tg', 'tg_link', 'tg_text'),
                ('show_external', 'external_link', 'external_text'),
                ('show_insta', 'insta_link', 'insta_text'),
                ('show_youtube', 'youtube_link', 'youtube_text'),
            ),
            'description': 'Налаштування кнопок для гри'
        }),
        ('Фільтри та параметри', {
            'fields': (
                ('players_range', 'age_group'),
                ('duration', 'prep_level'),
                ('location', 'activity_level'),
                ('interaction_type', 'goal'),
                ('content_type', 'thematic'),
                'skill_developed'
            ),
            'classes': ('collapse',),
            'description': 'Налаштування фільтрів для пошуку гри'
        }),
    )
