import random
from faker import Faker
from django.core.management.base import BaseCommand
from ...models import CustomUser, Gofer
from main.models import Address, Location, SubCategory, Category

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Populate Categories
        categories = []
        for category_name, _ in Category.CATEGORY_CHOICES:
            category = Category.objects.create(
                category_name=category_name,
                description=fake.text(max_nb_chars=200)
            )
            categories.append(category)
        
        # Populate SubCategories
        subcategories = []
        subcategory_names = set()
        for _ in range(30):  # Adjust the number of subcategories
            category = random.choice(categories)
            name = fake.unique.word().capitalize()
            while name in subcategory_names:
                name = fake.unique.word().capitalize()
            subcategory_names.add(name)
            subcategory = SubCategory.objects.create(
                category=category,
                name=name,
                description=fake.text(max_nb_chars=200)
            )
            subcategories.append(subcategory)
        
        # Populate Locations
        locations = []
        for _ in range(20):  # Adjust the number of locations
            location = Location.objects.create(
                latitude=fake.latitude(),
                longitude=fake.longitude(),
            )
            locations.append(location)
            
        addresses = []
        for _ in range(20): # Adjust the number of addresses
            address = Address.objects.create(
                house_number=fake.building_number(),
                street=fake.street_name(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country()
            )
            addresses.append(address)
            
        
        # Creating CustomUsers and Gofers
        for _ in range(50):  # Change 50 to the number of users you want to create
            gender = random.choice(['M', 'F', 'O'])
            location = random.choice(locations)
            address = random.choice(addresses)
            user = CustomUser.objects.create_user(
                email=fake.email(),
                phone_number=fake.phone_number(),
                gender=gender,
                location=location,
                address=address,
                phone_verified=fake.boolean(),
                email_verified=fake.boolean()
            )
            user.set_password('password')  # Set a default password
            user.save()

            # Creating Gofer for each CustomUser
            gofer = Gofer.objects.create(
                custom_user=user,
                expertise=fake.job(),
                mobility_means=random.choice(['Motorcycle', 'Car', 'Bicycle']),
                bio=fake.text(max_nb_chars=200),
                sub_category=random.choice(subcategories),
                charges=random.randint(10, 900),
            )
            gofer.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
