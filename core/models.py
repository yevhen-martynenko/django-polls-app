from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from polls.utils import create_code


QUESTION_TYPES = [
    ('short_text', 'Short Text'),
    ('long_text', 'Long Text'),
    ('checkbox', 'Checkbox'),
    ('radio', 'Radio'),
]


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    password = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=32, unique=True, editable=False)
    title = models.CharField(max_length=255, default='Untitled Form')
    description = models.TextField()
    date_of_creation = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.public:
            if not self.password:
                raise ValueError('Password is required for private polls.')
        else:
            self.password = None

        if not self.code:
            self.code = create_code(32)
            while Poll.objects.filter(code=self.code).exists():
                self.code = create_code(32)
        
        super().save(*args, **kwargs)


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    question_text = models.CharField(max_length=255, default='')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    total_answers = models.IntegerField(default=0)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255, default='')
    votes = models.IntegerField(default=0)
    text_answer = models.TextField(default='')

    def __str__(self):
        return self.option_text
