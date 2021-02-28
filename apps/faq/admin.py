from django.contrib import admin

from .models import QuestionWithAnswer, QuestionTitle


@admin.register(QuestionTitle)
class QuestionTitleAnswer(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(QuestionWithAnswer)
class QuestionWithAnswer(admin.ModelAdmin):
    list_display = ['id', 'question_en', 'question_fa', 'answer_en',
                    'answer_fa']
    list_editable = ['question_en', 'question_fa', 'answer_en', 'answer_fa']
    list_display_links = ['id']
    sortable_by = ['id', 'question_en', 'question_fa', 'answer_en',
                   'answer_fa']
    search_fields = ['question_en', 'question_fa', 'answer_en', 'answer_fa']
