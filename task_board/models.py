from django.db import models, transaction


class Executor(models.Model):
    asana_id = models.CharField(verbose_name='Asana ID', unique=True, max_length=64)
    name = models.CharField(verbose_name='Имя', max_length=255)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'


class Project(models.Model):
    asana_id = models.CharField(verbose_name='Asana ID', unique=True, max_length=64)
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        from task_board.tasks import update_or_create_project

        with transaction.atomic():
            super().save(*args, **kwargs)
            transaction.on_commit(lambda: update_or_create_project.delay(self.id))

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Task(models.Model):
    asana_id = models.CharField(verbose_name='Asana ID', unique=True, max_length=64)
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    project = models.ForeignKey(
        to=Project, verbose_name='Проект',
        on_delete=models.CASCADE
    )
    executor = models.ForeignKey(
        to=Executor, verbose_name='Исполнитель',
        on_delete=models.SET_NULL, blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        from task_board.tasks import update_or_create_task

        with transaction.atomic():
            super().save(*args, **kwargs)
            transaction.on_commit(lambda: update_or_create_task.delay(self.id))

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
