from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','sort_id')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','sort_id')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('summary','created_date','user')
    search_fields = ('summary','user')
    list_filter = ('user','created_date')
    ordering = ('-created_date',)
    #filter_horizontal = ('tags')

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('user','question','created_date')
    
class QLikeAdmin(admin.ModelAdmin):
	list_display = ('user','question')	

class ALikeAdmin(admin.ModelAdmin):	
	list_display = ('user','answer')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QLike, QLikeAdmin)
admin.site.register(ALike, ALikeAdmin)