from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        users = [
            User.objects.create(email='tony@marvel.com', username='IronMan', team=marvel),
            User.objects.create(email='steve@marvel.com', username='CaptainAmerica', team=marvel),
            User.objects.create(email='bruce@marvel.com', username='Hulk', team=marvel),
            User.objects.create(email='clark@dc.com', username='Superman', team=dc),
            User.objects.create(email='bruce@dc.com', username='Batman', team=dc),
            User.objects.create(email='diana@dc.com', username='WonderWoman', team=dc),
        ]

        # Create activities
        for user in users:
            Activity.objects.create(user=user, type='Running', duration=30, date=timezone.now().date())
            Activity.objects.create(user=user, type='Cycling', duration=45, date=timezone.now().date())

        # Create workouts
        w1 = Workout.objects.create(name='Strength', description='Strength training')
        w2 = Workout.objects.create(name='Cardio', description='Cardio workout')
        w1.suggested_for.set(users[:3])
        w2.suggested_for.set(users[3:])

        # Create leaderboard
        for i, user in enumerate(users):
            Leaderboard.objects.create(user=user, score=100-i*10, rank=i+1)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
