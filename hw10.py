from hw8.models import *
import datetime

task = Task.objects.create(
 title="Prepare presentation",
 description="Prepare materials and slides for the presentation",
 status="New",
 deadline=datetime.datetime.today()+datetime.timedelta(days=3)
)

sub_task_1 = SubTask.objects.create(
 title="Gather information",
 description="Find necessary information for the presentation",
 status="New",
 deadline=datetime.datetime.today()+datetime.timedelta(days=2),
 task=task
)

sub_task_2 = SubTask.objects.create(
 title="Create slides",
 description="Create presentation slides",
 status="New",
 deadline=datetime.datetime.today()+datetime.timedelta(days=1),
 task=task
)

new_tasks = Task.objects.filter(status__iexact="New")
print(new_tasks)

expired_sub_tasks = SubTask.objects.filter(status__iexact="Done", deadline__lt=datetime.datetime.today())
print(expired_sub_tasks)

task.status = "In progress"
task.save()
print(task)

sub_task_1.deadline=datetime.datetime.today()+datetime.timedelta(days=-2)
sub_task_1.save()
print(sub_task_1)

sub_task_2.description = "Create and format presentation slides"
sub_task_2.save()
print(sub_task_2)

task.delete()

