from django.contrib import admin
from models import Book, Course

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', "isbn")

"""
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'changed_at', 'owner', )
    list_filter = ('status',)
"""

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'semester', 'department', )
    list_filter = ('department', 'year', )

admin.site.register(Book, BookAdmin)
#admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Course, CourseAdmin)
