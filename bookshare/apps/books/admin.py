from django.contrib import admin
from models import Book, Course

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', "isbn", "num_available_stocks")
    filter_horizontal = ('courses',)        

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Book, BookAdmin)
admin.site.register(Course, CourseAdmin)
