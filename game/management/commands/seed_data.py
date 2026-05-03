from django.core.management.base import BaseCommand
from game.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        PlayerCountRange.objects.all().delete()
        AgeGroup.objects.all().delete()
        GameDuration.objects.all().delete()
        PrepLevel.objects.all().delete()
        Location.objects.all().delete()
        ActivityLevel.objects.all().delete()
        InteractionType.objects.all().delete()
        GameGoal.objects.all().delete()
        ContentType.objects.all().delete()

        PlayerCountRange.objects.bulk_create([
            PlayerCountRange(name=x) for x in ["2–4", "5–8", "9–12", "13–20", "20+"]
        ])

        AgeGroup.objects.bulk_create([
            AgeGroup(name=x) for x in ["діти (6–13)", "підлітки (14–18)", "молодь (18+)", "універсально"]
        ])

        GameDuration.objects.bulk_create([
            GameDuration(name=x) for x in ["до 5 хв", "5–10 хв", "10–20 хв", "20–40 хв", "40+ хв"]
        ])

        PrepLevel.objects.bulk_create([
            PrepLevel(name=x) for x in [
                "без підготовки",
                "мінімальна (1–5 хв)",
                "середня (потрібні матеріали)",
                "складна (заздалегідь готувати)"
            ]
        ])

        Location.objects.bulk_create([
            Location(name=x) for x in ["приміщення", "вулиця", "будь-де"]
        ])

        ActivityLevel.objects.bulk_create([
            ActivityLevel(name=x) for x in [
                "дуже активна (біг, рух)",
                "середня",
                "спокійна",
                "сидяча"
            ]
        ])

        InteractionType.objects.bulk_create([
            InteractionType(name=x) for x in ["командна", "індивідуальна", "всі разом"]
        ])

        GameGoal.objects.bulk_create([
            GameGoal(name=x) for x in [
                "знайомство",
                "розігрів",
                "розвага",
                "навчання",
                "обговорення / рефлексія"
            ]
        ])

        ContentType.objects.bulk_create([
            ContentType(name=x) for x in [
                "усна гра",
                "настільна гра",
                "додаток",
                "презентація"
            ]
        ])

        self.stdout.write("Дані успішно додані")
