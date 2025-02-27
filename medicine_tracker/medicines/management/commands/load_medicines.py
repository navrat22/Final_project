from django.core.management.base import BaseCommand
from medicines.models import Medicine

from django.core.management.base import BaseCommand
from medicines.models import Medicine


class Command(BaseCommand):
    help = 'Načte (nebo doplní) hromadně vybrané léky do tabulky Medicine.'

    def handle(self, *args, **options):
        medicines_data = [
            {
                "name": "Apixaban",
                "storage_temp": "2–25 °C",
                "side_effects": "Možné krvácení, bolesti hlavy, únava",
                "manufacturer": "Pfizer"
            },
            {
                "name": "Paracetamol",
                "storage_temp": "15–25 °C",
                "side_effects": "Ojediněle alergické reakce, nevolnost",
                "manufacturer": "Sanofi"
            },
            {
                "name": "Ibalgin",
                "storage_temp": "Do 25 °C",
                "side_effects": "Podráždění žaludku, alergie",
                "manufacturer": "Zentiva"
            },
            {
                "name": "Warfarin",
                "storage_temp": "15–30 °C",
                "side_effects": "Krvácení, bolesti svalů",
                "manufacturer": "Orion"
            },
            {
                "name": "Xarelto",
                "storage_temp": "15–30 °C",
                "side_effects": "Nadměrné krvácení, kožní vyrážka",
                "manufacturer": "Bayer"
            },
            {
                "name": "Nimesil",
                "storage_temp": "Do 25 °C",
                "side_effects": "Bolesti břicha, průjem",
                "manufacturer": "Berlin-Chemie"
            },
            {
                "name": "Anopyrin",
                "storage_temp": "15–25 °C",
                "side_effects": "Bolesti žaludku, krvácení z nosu",
                "manufacturer": "Zentiva"
            },
            {
                "name": "Metformin",
                "storage_temp": "Do 30 °C",
                "side_effects": "Nechutenství, průjem",
                "manufacturer": "Teva"
            },
            {
                "name": "Penicilin",
                "storage_temp": "2–8 °C",
                "side_effects": "Alergické reakce, vyrážka",
                "manufacturer": "Biotika"
            },
            {
                "name": "Viagra",
                "storage_temp": "25–30 °C",
                "side_effects": "Bolesti hlavy, návaly horka",
                "manufacturer": "Pfizer"
            },
            {
                "name": "Kodein",
                "storage_temp": "15–25 °C",
                "side_effects": "Zácpa, ospalost, závislost",
                "manufacturer": "Zentiva"
            },
            {
                "name": "Diazepam",
                "storage_temp": "2–25 °C",
                "side_effects": "Ospalost, závratě, slabost",
                "manufacturer": "Galena"
            },
            {
                "name": "Omeprazol",
                "storage_temp": "Do 25 °C",
                "side_effects": "Nevolnost, průjem, bolesti hlavy",
                "manufacturer": "Krka"
            },
            {
                "name": "Atorvastatin",
                "storage_temp": "15–30 °C",
                "side_effects": "Bolesti svalů, zažívací potíže",
                "manufacturer": "Pfizer"
            },
            {
                "name": "Amlodipin",
                "storage_temp": "Do 30 °C",
                "side_effects": "Otoky kotníků, návaly horka",
                "manufacturer": "Zentiva"
            },
            {
                "name": "Clexane",
                "storage_temp": "Do 25 °C",
                "side_effects": "Krvácení, hematomy v místě vpichu",
                "manufacturer": "Sanofi"
            },
            {
                "name": "Clarithromycin",
                "storage_temp": "15–25 °C",
                "side_effects": "Zažívací potíže, hořkost v ústech",
                "manufacturer": "Teva"
            },
            {
                "name": "Zyrtec",
                "storage_temp": "Do 25 °C",
                "side_effects": "Ospalost, sucho v ústech",
                "manufacturer": "UCB"
            },
            {
                "name": "Diclofenac",
                "storage_temp": "15–25 °C",
                "side_effects": "Bolesti břicha, žaludeční vředy",
                "manufacturer": "Sandoz"
            },
            {
                "name": "Lipitor",
                "storage_temp": "Do 25 °C",
                "side_effects": "Bolesti svalů, zažívací problémy",
                "manufacturer": "Pfizer"
            },
        ]

        for med_data in medicines_data:
            obj, created = Medicine.objects.get_or_create(
                name=med_data["name"],
                defaults={
                    "storage_temp": med_data["storage_temp"],
                    "side_effects": med_data["side_effects"],
                    "manufacturer": med_data["manufacturer"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Přidán lék: {obj.name}'))
            else:
                 self.stdout.write(f'Lék {obj.name} už v DB existoval, ponechán beze změn.')

        self.stdout.write(self.style.SUCCESS('Hotovo!'))

