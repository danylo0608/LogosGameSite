from django.shortcuts import render, get_object_or_404
from .models import (
    Game, Category, PlayerCountRange, AgeGroup, GameDuration,
    PrepLevel, Location, ActivityLevel, InteractionType, GameGoal, ContentType, Thematic
)

def home(request):
    situations = GameGoal.objects.all()
    return render(request, 'game/index.html', {'situations': situations})

def game_list(request, category=None):
    games = Game.objects.all()
    
    category_obj = None
    if category:
        category_obj = get_object_or_404(Category, slug=category)
        games = games.filter(category=category_obj)
    
    # Фільтрація
    players_id = request.GET.get('players')
    age_id = request.GET.get('age')
    duration_id = request.GET.get('duration')
    prep_id = request.GET.get('prep')
    location_id = request.GET.get('location')
    activity_id = request.GET.get('activity')
    interaction_id = request.GET.get('interaction')
    goal_id = request.GET.get('situation')
    content_id = request.GET.get('content')
    thematic_id = request.GET.get('thematic')

    if players_id: games = games.filter(players_range_id=players_id)
    if age_id: games = games.filter(age_group_id=age_id)
    if duration_id: games = games.filter(duration_id=duration_id)
    if prep_id: games = games.filter(prep_level_id=prep_id)
    if location_id: games = games.filter(location_id=location_id)
    if activity_id: games = games.filter(activity_level_id=activity_id)
    if interaction_id: games = games.filter(interaction_type_id=interaction_id)
    if goal_id: games = games.filter(goal_id=goal_id)
    if content_id: games = games.filter(content_type_id=content_id)
    if thematic_id: games = games.filter(thematic_id=thematic_id)

    # Дані для фільтрів (спрощуємо передачу в шаблон)
    filter_data = [
        ('situation', 'Ситуація', GameGoal.objects.all(), goal_id),
        ('players', 'Гравців', PlayerCountRange.objects.all(), players_id),
        ('age', 'Вік', AgeGroup.objects.all(), age_id),
        ('duration', 'Тривалість', GameDuration.objects.all(), duration_id),
        ('prep', 'Підготовка', PrepLevel.objects.all(), prep_id),
        ('activity', 'Активність', ActivityLevel.objects.all(), activity_id),
        ('location', 'Місце', Location.objects.all(), location_id),
        ('interaction', 'Взаємодія', InteractionType.objects.all(), interaction_id),
        ('content', 'Контент', ContentType.objects.all(), content_id),
        ('thematic', 'Тематика', Thematic.objects.all(), thematic_id),
    ]

    context = {
        'games': games,
        'category': category,
        'category_label': category_obj.name if category_obj else None,
        'filter_data': filter_data,
    }
    return render(request, 'game/game_list.html', context)

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game/game_detail.html', {'game': game})

def about(request):
    return render(request, 'game/about.html')
