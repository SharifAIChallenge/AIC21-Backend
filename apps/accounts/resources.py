from import_export import resources, fields

from .models import Profile


class ProfileResource(resources.ModelResource):
    team = fields.Field(attribute='user__team__name',
                        column_name='team')
    username = fields.Field(attribute='user__username', column_name='username')
    email = fields.Field(attribute='user__email',
                         column_name='email')
    team_size = fields.Field()

    class Meta:
        model = Profile
        fields = ('username', 'firstname_fa', 'lastname_fa', 'email',
                  'birth_date', 'phone_number', 'province', 'university',
                  'major', 'university_term', 'university_degree',
                  'linkedin', 'github', 'programming_language', 'position',
                  'image', 'can_sponsors_see', 'sponsor_permission', 'team',
                  'team_size')

    def dehydrate_team_size(self, obj: Profile):
        if hasattr(obj.user, 'participant'):
            return obj.user.team.member_count()
        return ''
