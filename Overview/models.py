from django.db import models

class Member(models.Model):
	mid = models.CharField(max_length=5, primary_key=True)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=50)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)

	def __str__(self):
		return self.mid

class Group(models.Model):
	gid = models.IntegerField(primary_key=True)
	gname = models.CharField(max_length=100)

	def __str__(self):
		return self.gid

class Project(models.Model):
	pid = models.IntegerField(primary_key=True)
	pname = models.CharField(max_length=100)

	def __str__(self):
		return self.pid

class GroupMember(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	members = models.CharField(max_length=1000)

	def __str__(self):
		return self.group

class GroupProject(models.Model):
	pgroup = models.ForeignKey(Group, on_delete=models.CASCADE)
	projects = models.CharField(max_length=1000)

	def __str__(self):
		return self.pgroup


# Create your models here.
