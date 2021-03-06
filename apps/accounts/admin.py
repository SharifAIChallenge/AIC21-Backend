from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .resources import ProfileResource
from .models import User, Profile, Skill, JobExperience, GoogleLogin, \
    UniversityAPIConfig, MajorAPIConfig, University, Major


# Register your models here.

class SkillInline(admin.StackedInline):
    model = Skill


class JobExperienceInline(admin.StackedInline):
    model = JobExperience


@admin.register(UniversityAPIConfig)
class UniversityAPIConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(MajorAPIConfig)
class MajorAPIConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'team')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    inlines = (SkillInline, JobExperienceInline)
    list_display = ('id', 'firstname_fa', 'lastname_fa', 'birth_date',
                    'phone_number', 'university', 'major', 'university_degree')
    list_filter = ('university', 'major', 'university_degree')

    search_fields = ('firstname_fa', 'lastname_fa', 'major',
                     'phone_number', 'university')

    resource_class = ProfileResource


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    pass


@admin.register(GoogleLogin)
class GoogleLoginAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_signup')
    list_display_links = ('id', 'email')
    search_fields = ('email',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    pass
