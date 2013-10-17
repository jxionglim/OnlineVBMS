class Job(models.Model):
	cusId = models.IntegerField()
	coyId = models.IntegerField()
	jobId = models.IntegerField()
	dateCreated = models.DateField()
	amount = models.DecimalField(max_digits=9, decimal_places=3)
	paidStatus = models.CharField(max_length=8)
	
	class Meta:
		managed = False
		
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
		
	class Meta:
		managed = False
		
class reqResources(models.Model):
	coyId = models.IntegerField()
	driverId = models.IntegerField()
	cusId = models.IntegerField()
	jobId = models.IntegerField()
	tripId = models.IntegerField()
	roundTrip = models.CharField(max_length=1)
		
	class Meta:
		managed = False