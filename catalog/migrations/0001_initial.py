# Generated by Django 2.0.5 on 2018-06-17 13:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('Surname', models.CharField(max_length=150)),
                ('D_O_B', models.DateField(blank=True, null=True)),
                ('D_O_D', models.DateField(blank=True, null=True, verbose_name='Died')),
            ],
            options={
                'ordering': ['first_name', 'Surname'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn>ISBN number</a>", max_length=15, verbose_name='ISBN')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Author')),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text="Enter the book's particurlar UUID", primary_key=True, serialize=False)),
                ('imprint', models.CharField(max_length=200)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('A', 'Avaialable'), ('M', 'Maintanance'), ('R', 'Reserved'), ('O', 'On Loan')], default='A', help_text='Book Avaialability', max_length=1)),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the genre the book belongs to e.g Science, Fiction etc', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dialet_used', models.CharField(choices=[('E', 'English'), ('F', 'French'), ('C', 'Chinese'), ('I', 'Italia')], default='E', max_length=1)),
                ('local_dialet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.BookInstance')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Enter a genre for the book', to='catalog.Genre'),
        ),
    ]
