from django.contrib import admin
# Task 2 Requirement: Import seven classes from .models
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade', 'lesson']
    search_fields = ['question_text']


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']
    search_fields = ['title', 'content']


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_learners']


class LearnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation', 'social_link']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'id']


# Register models in Admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
