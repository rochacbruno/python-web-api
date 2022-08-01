from blog.models import Post
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify


class Command(BaseCommand):
    """Adds a new post to the database
    django-admin add-post --title 'Title' --content 'Content'
    """

    help = "Creates a new Post in the blog"

    def add_arguments(self, parser):
        parser.add_argument("--title", type=str)
        parser.add_argument("--content", type=str)

    def handle(self, *args, **options):
        """handles the arguments and creates the new post"""
        try:
            post = Post.objects.create(
                title=options["title"],
                slug=slugify(options["title"]),
                content=options["content"],
            )
        except Exception as e:
            raise CommandError(e)
        else:
            self.stdout.write(self.style.SUCCESS(f'Post "{post.title}" created'))
