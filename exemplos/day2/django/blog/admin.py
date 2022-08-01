from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "published", "date"]
    list_filter = ["published", "date"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["-date"]
    actions = ["publish"]

    @admin.action(description="Publish/Unpublish posts")
    def publish(self, request, queryset):
        for post in queryset:
            post.published = not post.published
            post.save()


admin.site.register(Post, PostAdmin)
