from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Quiz, QuizType, QuizCBM, Question, QuizAnswer, MultipleChoice, UploadCSVFormat, Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
   list_display=('title', 'author', 'created_date', 'published_date')
   search_field=['title', 'text']

class UploadCSVAdmin(admin.ModelAdmin):
    model = UploadCSVFormat
    list_display=('title',)

class QuizAnswerInline(admin.TabularInline):
   model = QuizAnswer

class QuizAdminPage(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"), 
        widget=FilteredSelectMultiple(
            verbose_name=("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminPage, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial =\
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz=super(QuizAdminPage, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz

class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminPage
    list_display=('title', 'quiztype',)
    list_type=('quiztype',)
    search_fields = ('descriptor', 'quiztype',)

class QuizTypeAdmin(admin.ModelAdmin):
   search_field = ('quiztype',)

class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display=('entans', 'quiztype',)
    list_filter =('quiztype',)
    fields=('entans', 'quiztype', 'quiz', 'questdescript', 'answer_order', 'figure')
    search_fields=('entans', 'questdescript')
    filter_horizontal = ('quiz',)

    inlines = [QuizAnswerInline]

class QuizCBMAdmin(admin.ModelAdmin):
    search_fields = ('user', 'score',)

#admin.site.register(Post)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizType, QuizTypeAdmin)
admin.site.register(MultipleChoice, MultipleChoiceAdmin)
admin.site.register(QuizCBM, QuizCBMAdmin) 
admin.site.register(UploadCSVFormat, UploadCSVAdmin)
