import os
import sys
import django

# Додаємо кореневу директорію проекту до шляху пошуку модулів
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LogosGameSite.settings')
django.setup()

from game.models import (
    PlayerCountRange, AgeGroup, GameDuration, PrepLevel, 
    Location, ActivityLevel, InteractionType, GameGoal, ContentType
)

data = {
    PlayerCountRange: ["2–4", "5–8", "9–12", "13–20", "20+"],
    AgeGroup: ["діти (6–13)", "підлітки (14–18)", "молодь (18+)", "універсально"],
    GameDuration: ["до 5 хв", "5–10 хв", "10–20 хв", "20–40 хв", "40+ хв"],
    PrepLevel: ["без підготовки", "мінімальна (1–5 хв)", "середня (потрібні матеріали)", "складна (заздалегідь готувати)"],
    Location: ["приміщення", "вулиця", "будь-де"],
    ActivityLevel: ["дуже активна (біг, рух)", "середня", "спокійна", "сидяча"],
    InteractionType: ["командна", "індивідуальна", "всі разом"],
    GameGoal: ["знайомство", "розігрів", "розвага", "навчання", "обговорення / рефлексія"],
    ContentType: ["усна гра", "настільна гра", "додаток", "презентація"]
}

for model, values in data.items():
    print(f"Populating {model.__name__}...")
    for val in values:
        model.objects.get_or_create(name=val)

print("Done!")
