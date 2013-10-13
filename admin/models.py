from django.db import models

class Company(models.Model):
	coyId = models.IntegerField()
	coyName = models.CharField(max_length=256)
	email = models.EmailField(max_length=256)
	faxNo = models.BigIntegerField()
	contactNo = models.BigIntegerField()
	zipcode = models.BigIntegerField()
	streetName = models.CharField(max_length=256)
	rating = models.DecimalField(max_digits=3, decimal_places=2)
	
class Driver(models.Model):
	coyId = models.IntegerField()
	driverId = models.IntegerField()
	firstName = models.CharField(max_length=256)
	lastName = models.CharField(max_length=256)
	driverClass = models.CharField(max_length=2)
	contactNo = models.BigIntegerField()
	
class Customer(models.Model):
	cusId = models.IntegerField()
	firstName = models.CharField(max_length=256)
	lastName = models.CharField(max_length=256)
	contactNo = models.BigIntegerField()
	email = models.EmailField(max_length=256)
	zipcode = models.BigIntegerField()
	streetName = models.CharField(max_length=256)
	credit_expDate = models.DateField()
	credit_serialNo = models.BigIntegerField()
	
class Job(models.Model):
	cusId = models.IntegerField()
	coyId = models.IntegerField()
	jobId = models.IntegerField()
	dateCreated = models.DateField()
	amount = models.DecimalField(max_digits=9, decimal_places=3)
	paidStatus = models.CharField(max_length=8)

class Trip(models.Model):
	cusId = models.IntegerField()
	jobId = models.IntegerField()
	tripId = models.IntegerField()
	dateReq = models.DateField()
	startTime = models.TimeField()
	endTime = models.TimeField()
	startLocation = models.CharField(max_length=256)
	endLocation = models.CharField(max_length=256)
	comments = models.TextField()
	
class Vehicle(models.Model):
	coyId = models.IntegerField()
	carplateNo = models.CharField(max_length=8)
	iuNo = models.IntegerField()
	manufacturer = models.CharField(max_length=256)
	model = models.CharField(max_length=256)
	transType = models.CharField(max_length=6)
	driverClass = models.CharField(max_length=2)
	capacity = models.IntegerField()

class Lorry(models.Model):
	carplateNo = models.CharField(max_length=8)
	tons = models.IntegerField()

class Car(models.Model):
	carplateNo = models.CharField(max_length=8)
	category = models.CharField(max_length=9)
	
class Bus(models.Model):
	carplateNo = models.CharField(max_length=8)
	category = models.CharField(max_length=9)

class reqResources(models.Model):
	coyId = models.IntegerField()
	driverId = models.IntegerField()
	cusId = models.IntegerField()
	jobId = models.IntegerField()
	tripId = models.IntegerField()
	roundTrip = models.CharField(max_length=1)