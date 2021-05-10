from import_export import resources, fields

from .models import Profile


class ProfileResource(resources.ModelResource):
    team = fields.Field(attribute='user__team__name',
                        column_name='team')
    username = fields.Field(attribute='user__username', column_name='username')
    email = fields.Field(attribute='user__email',
                         column_name='email')
    team_size = fields.Field()
    last_bot_won = fields.Field()
    total_submissions = fields.Field()
    is_finalist = fields.Field()
    skills = fields.Field()
    job_experiences = fields.Field()

    class Meta:
        model = Profile
        fields = ('username', 'firstname_fa', 'lastname_fa', 'email',
                  'birth_date', 'phone_number', 'province', 'university',
                  'major', 'university_term', 'university_degree',
                  'linkedin', 'github', 'programming_language', 'position',
                  'image', 'can_sponsors_see', 'sponsor_permission', 'team',
                  'team_size', 'last_bot_won', 'total_submissions',
                  'is_finalist', 'skills', 'job_experiences')

    def dehydrate_team_size(self, obj: Profile):
        if obj.user.team:
            return obj.user.team.member_count()
        return ''

    def dehydrate_last_bot_won(self, obj: Profile):
        from apps.team.models import Team

        if not obj.user.team:
            return None

        bots = Team.bots.all().order_by('bot_number')
        last_bot = None
        for bot in bots:
            if bot.has_won_me(obj.user.team):
                last_bot = bot

        return last_bot.bot_number if last_bot else None

    def dehydrate_total_submissions(self, obj: Profile):
        if not obj.user.team:
            return 0
        return obj.user.team.submissions.all().count()

    def dehydrate_is_finalist(self, obj: Profile):
        if not obj.user.team:
            return 0
        return obj.user.team.is_finalist

    def dehydrate_skills(self, obj: Profile):
        result = ', '.join(obj.skills.values_list('skill', flat=True))

        return result

    def dehydrate_job_experiences(self, obj: Profile):
        results = []

        for job in obj.jobs.all():
            current = f'company: {job.company}, position: {job.position}, ' \
                      f'description: {job.description}'
            results.append(current)

        return '\n------------------\n'.join(results)
