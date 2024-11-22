from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=120)
    ssn = models.CharField(max_length=9)

    def __str__(self):
        return self.name
    
class Bank_account(models.Model):

    account_num = models.IntegerField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account_num} ({self.person})"
    
    
class Course(models.Model):

    name = models.CharField(max_length=120)
    number = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    


class Student(models.Model):
    name = models.CharField(max_length=120)
    # courses = models.ManyToManyField('Course')

    def __str__(self):
        return self.name
    

class Registration(models.Model):
    """ implement many to many relationships between student and Course """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.course}"

    def get_students(self, course):
        return Registration.objects.filter(course=course)
    
class FamilyPerson(models.Model):
    """ person within a family tree """

    name = models.CharField(max_length=120)
    dob = models.DateField()

    mother = models.ForeignKey('FamilyPerson', on_delete=models.CASCADE, 
                               related_name='mother_person', 
                               null=True, blank=True)
    father = models.ForeignKey('FamilyPerson', on_delete=models.CASCADE, 
                               related_name='father_person',
                               null=True, blank=True)

    def __str__(self):
        return self.name



