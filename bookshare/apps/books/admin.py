from django.contrib import admin
from models import Book, Course

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', "isbn")

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', )
    list_filter = ('year', )

admin.site.register(Book, BookAdmin)
admin.site.register(Course, CourseAdmin)
