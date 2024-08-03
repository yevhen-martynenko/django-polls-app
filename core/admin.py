from django.contrib import admin

from .models import Poll, Question, Option


class OptionInline(admin.StackedInline):
    model = Option
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ['question_text', 'question_type', 'required', 'pk']


class QuestionInline(admin.TabularInline):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Description', {'fields': ['question_type']}),
        ('Required', {'fields': ['required']}),
    ]
    model = Question
    extra = 0


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'public', 'active', 'password']}),
        ('Description', {'fields': ['description']}),
    ]
    inlines = [QuestionInline]
    list_display = ['title', 'date_of_creation', 'owner', 'public', 'active']
    list_filter = ['date_of_creation', 'owner']


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
