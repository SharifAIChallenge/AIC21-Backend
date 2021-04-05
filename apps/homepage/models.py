from django.db import models


class SponsorGradeTypes:
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'
    TYPES = (
        (FIRST, 'First Grade'),
        (SECOND, 'Second Grade'),
        (THIRD, 'Third Grade')
    )


class Intro(models.Model):
    header_en = models.CharField(max_length=100)
    header_fa = models.CharField(max_length=100)
    text_en = models.TextField()
    text_fa = models.TextField()

    term_of_use = models.TextField(null=True)

    def __str__(self):
        return self.header_en


class TimelineEvent(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    text_en = models.TextField()
    text_fa = models.TextField()

    day = models.CharField(max_length=32, null=True, blank=True)
    month = models.CharField(max_length=32, null=True, blank=True)

    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title_en


class Prize(models.Model):
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    prize_en = models.CharField(max_length=100)
    prize_fa = models.CharField(max_length=100)
    team_name = models.CharField(max_length=128)

    def __str__(self):
        return self.title_en


class Stats(models.Model):
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    stat_en = models.CharField(max_length=100)
    stat_fa = models.CharField(max_length=100)
    icon = models.CharField(max_length=128)

    def __str__(self):
        return self.title_en


class Sponsor(models.Model):
    title_en = models.CharField(max_length=512, unique=True)
    title_fa = models.CharField(max_length=512, unique=True)
    url = models.CharField(max_length=500)
    grade = models.CharField(max_length=20, choices=SponsorGradeTypes.TYPES)
    description = models.TextField()

    def upload_path(self, filename):
        return f'sponsor/{self.grade}/{self.title}/'

    image = models.FileField(upload_to=upload_path, null=True, blank=True)
    video = models.FileField(upload_to=upload_path, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class WhyThisEvent(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=300)
    body = models.TextField()


class Quote(models.Model):
    name_en = models.CharField(max_length=200)
    name_fa = models.CharField(max_length=200)
    comment_en = models.TextField()
    comment_fa = models.TextField()


class Motto(models.Model):
    motto = models.CharField(max_length=2048)
    pre_text = models.CharField(max_length=2048)


class Media(models.Model):
    title = models.CharField(max_length=128)
    file = models.FileField()


class SocialMedia(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField(max_length=256)
    icon = models.CharField(max_length=128)


class SponsorSocialMedia(SocialMedia):
    sponsor = models.ForeignKey(Sponsor,
                                related_name='socials',
                                on_delete=models.CASCADE)


class SponsorJobOpportunity(models.Model):
    job_url = models.URLField(
        max_length=512,
        help_text='Job opp url at sponsor website'
    )
    sponsor = models.ForeignKey(
        Sponsor,
        related_name='jobs',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=512)


class Rule(models.Model):
    title_en = models.CharField(max_length=50, blank=True)
    title_fa = models.CharField(max_length=50)
    text_en = models.TextField(max_length=10000, blank=True)
    text_fa = models.TextField(max_length=10000)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title_fa}'


class Subscribe(models.Model):
    email = models.EmailField(unique=True)


class GoogleAddEventToCalender(models.Model):
    url = models.CharField(max_length=512)
