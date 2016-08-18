# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations

CATEGORIES = [
    'Django',
    'Django REST framework',
    'Python',
    'SQL',
    'Object-oriented programming',
    'HTML',
    'CSS',
    'JavaScript',
    'REST',
    'General',
    'XML',
    'JSON',
    'Design Patterns',
    'HTTP',
    'Networking',
    'Algorithms + Data Structures'       
]

ANSWER_QUALITIES = [
    'Poor',
    'Good',
    'Excellent'                    
]

def categories(apps, schema_editor):
    Category = apps.get_model("screener", "Category")
    for cat in CATEGORIES:
        Category.objects.create(category=cat)
        
def answer_qualities(apps, schema_editor):
    AnswerQuality = apps.get_model("screener", "AnswerQuality")
    for quality in ANSWER_QUALITIES:
        AnswerQuality.objects.create(quality=quality)


class Migration(migrations.Migration):

    dependencies = [
        ('screener', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(categories),
        migrations.RunPython(answer_qualities)
    ]
