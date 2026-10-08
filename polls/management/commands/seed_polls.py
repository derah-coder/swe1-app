from django.core.management import BaseCommand, call_command

from polls.models import Question


class Command(BaseCommand):
    help = "Add the example polls to an empty database without changing existing votes."

    def handle(self, *args, **options):
        if Question.objects.exists():
            self.stdout.write("Polls already exist; keeping the current data.")
            return
        call_command("loaddata", "demo_polls", verbosity=0)
        self.stdout.write(self.style.SUCCESS("Example polls added."))
