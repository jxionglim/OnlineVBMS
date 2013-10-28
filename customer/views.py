from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from customer.models import JobForm, companySearchForm, TripForm
import datetime
import dbaccess
import userprofile.dbaccess as userProfileDBAccess


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def addJob(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            jobId = dbaccess.getMaxJobId()+1
            cusId = 1 #userProfileDBAccess.getCustIdByUserId(request.user.id)
            coyId = request.POST['coyId']
            params = [
                jobId,
                datetime.datetime.now().strftime("%Y-%m-%d"),
                cusId,
                coyId,
                request.POST['amount'],
                request.POST['paidStatus']
            ]
            dbaccess.insertJob(params)
            request.session['jobId'] = jobId
            request.session['coyId'] = coyId
            return HttpResponseRedirect('/customer/addTrip')
    else:
        form = JobForm()

    return render_to_response('customer/addJob.html', {
        'form': form
    }, context_instance=RequestContext(request))


def addTrip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            jobId = request.session.get('jobId')
            cusId = 1 #userProfileDBAccess.getCustIdByUserId(request.user.id)
            coyId = request.session.get('coyId')
            tripId = dbaccess.getMaxTripId()+1
            startDate = request.POST['startDate']
            startTime = request.POST['startTime']
            endDate = request.POST['endDate']
            endTime = request.POST['endTime']
            startDateTime = startDate+" "+startTime+":00"
            endDateTime = endDate+" "+endTime+":00"
            roundTrip = request.POST['roundTrip'] #gets YES or NO
            if roundTrip == "YES":
                roundTrip = "y"
            elif roundTrip == "NO":
                roundTrip = "n"
            noOfCars = request.POST['noOfCars']
            noOfBuses = request.POST['noOfBuses']
            noOfLorries = request.POST['noOfLorries']
            finalRResource = []
            driverParams = [
                coyId,
                endDateTime,
                startDateTime,
                coyId
            ]
            listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
            addingSuccess = True
            if int(noOfCars) > 0:
                sedanAmt = request.POST['sedanAmt']
                mpvAmt = request.POST['mpvAmt']
                luxuryAmt = request.POST['luxuryAmt']
                if int(sedanAmt)+int(mpvAmt)+int(luxuryAmt) == int(noOfCars):
                    print "hello"
                    if int(sedanAmt) > 0:
                        sedanParams = [
                            'c',
                            'sedan',
                            coyId,
                            endDateTime,
                            startDateTime,
                            'c',
                            'sedan',
                            coyId
                        ]
                        listOfSedanCars = dbaccess.getAvailableCars(sedanParams)
                        print len(listOfSedanCars)
                        if len(listOfSedanCars) < int(sedanAmt):
                            addingSuccess = False
                        else:
                            print "LIST OF CAR"
                            print listOfSedanCars
                            listOfSedanCars = listOfSedanCars[:int(sedanAmt)]
                            print "LIST OF NEW CAR"
                            print listOfSedanCars
                            print listOfAvailableDrivers
                            if len(listOfAvailableDrivers) < len(listOfSedanCars):
                                addingSuccess = False
                            else:
                                result, listOfAvailableDrivers = matchVehicleDriver(listOfSedanCars, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                print result
                                if result == False:
                                    addingSuccess = False
                                else:
                                    for x in result:
                                        finalRResource.append(x)
                                    print "yahoo"
                                    print finalRResource

                    if addingSuccess:
                        if int(mpvAmt) > 0:
                            mpvParams = [
                                'c',
                                'mpv',
                                coyId,
                                endDateTime,
                                startDateTime,
                                'c',
                                'mpv',
                                coyId
                            ]
                            listOfMpvCars = dbaccess.getAvailableCars(mpvParams)
                            print listOfMpvCars
                            if len(listOfMpvCars) < int(mpvAmt):
                                addingSuccess = False
                            else:
                                print "LIST OF CAR"
                                print listOfMpvCars
                                listOfMpvCars = listOfMpvCars[:int(mpvAmt)]
                                print "LIST OF NEW CAR"
                                print listOfMpvCars
                                print listOfAvailableDrivers
                                if len(listOfAvailableDrivers) < len(listOfMpvCars):
                                    addingSuccess = False
                                else:
                                    result, listOfAvailableDrivers = matchVehicleDriver(listOfMpvCars, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                    print result
                                    if result == False:
                                        addingSuccess = False
                                    else:
                                        for x in result:
                                            finalRResource.append(x)
                                        print "yahoo"
                                        print finalRResource
                    if addingSuccess:
                        if int(luxuryAmt) > 0:
                            luxuryParams = [
                                'c',
                                'luxury',
                                coyId,
                                endDateTime,
                                startDateTime,
                                'c',
                                'luxury',
                                coyId
                            ]
                            listOfLuxuryCars = dbaccess.getAvailableCars(luxuryParams)

                            if len(listOfLuxuryCars) < int(luxuryAmt):
                                addingSuccess = False
                            else:
                                print "LIST OF CAR"
                                print listOfLuxuryCars
                                listOfLuxuryCars = listOfLuxuryCars[:int(luxuryAmt)]
                                print "LIST OF NEW CAR"
                                print listOfLuxuryCars
                                print listOfAvailableDrivers
                                if len(listOfAvailableDrivers) < len(listOfLuxuryCars):
                                    addingSuccess = False
                                else:
                                    result, listOfAvailableDrivers = matchVehicleDriver(listOfLuxuryCars, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                    print result
                                    if result == False:
                                        addingSuccess = False
                                    else:
                                        for x in result:
                                            finalRResource.append(x)
                                        print "yahoo"
                                        print finalRResource

                    print "FINALLY"
                    print addingSuccess
                else:
                    addingSuccess = False
                    #search for cars that are needed.
                    #if have enough cars, need to create a reqResource record for each car. but have to check if need bus and lorry anot

            if int(noOfBuses) > 0 and addingSuccess:
                print "omg" + noOfBuses
                busAmt = request.POST['busAmt']
                miniAmt = request.POST['miniAmt']
                coachAmt = request.POST['coachAmt']
                if int(busAmt)+int(miniAmt)+int(coachAmt) == int(noOfBuses):
                    print "hello"
                    if int(busAmt) > 0:
                        busParams = [
                            'b',
                            'bus',
                            coyId,
                            endDateTime,
                            startDateTime,
                            'b',
                            'bus',
                            coyId
                        ]
                        listOfBusBus = dbaccess.getAvailableBuses(busParams)
                        print len(listOfBusBus)
                        if len(listOfBusBus) < int(busAmt):
                            addingSuccess = False
                        else:
                            print "LIST OF BUS"
                            print listOfBusBus
                            listOfBusBus = listOfBusBus[:int(busAmt)]
                            print "LIST OF NEW BUS"
                            print listOfBusBus
                            print listOfAvailableDrivers
                            if len(listOfAvailableDrivers) < len(listOfBusBus):
                                addingSuccess = False
                            else:
                                result, listOfAvailableDrivers = matchVehicleDriver(listOfBusBus, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                print result
                                if result == False:
                                    addingSuccess = False
                                else:
                                    for x in result:
                                        finalRResource.append(x)
                                    print "yahoo"
                                    print finalRResource

                    if addingSuccess:
                        if int(miniAmt) > 0:
                            miniParams = [
                                'b',
                                'mini',
                                coyId,
                                endDateTime,
                                startDateTime,
                                'b',
                                'mini',
                                coyId
                            ]
                            listOfMiniBus = dbaccess.getAvailableBuses(miniParams)
                            print listOfMiniBus
                            if len(listOfMiniBus) < int(miniAmt):
                                addingSuccess = False
                            else:
                                print "LIST OF BUS"
                                print listOfMiniBus
                                listOfMiniBus = listOfMiniBus[:int(miniAmt)]
                                print "LIST OF NEW BUS"
                                print listOfMiniBus
                                print listOfAvailableDrivers
                                if len(listOfAvailableDrivers) < len(listOfMiniBus):
                                    addingSuccess = False
                                else:
                                    result, listOfAvailableDrivers = matchVehicleDriver(listOfMiniBus, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                    print result
                                    if result == False:
                                        addingSuccess = False
                                    else:
                                        for x in result:
                                            finalRResource.append(x)
                                        print "yahoo"
                                        print finalRResource
                    if addingSuccess:
                        if int(coachAmt) > 0:
                            coachParams = [
                                'b',
                                'coach',
                                coyId,
                                endDateTime,
                                startDateTime,
                                'b',
                                'coach',
                                coyId
                            ]
                            listOfCoachBus = dbaccess.getAvailableBuses(coachParams)

                            if len(listOfCoachBus) < int(coachAmt):
                                addingSuccess = False
                            else:
                                print "LIST OF BUS"
                                print listOfCoachBus
                                listOfCoachBus = listOfCoachBus[:int(coachAmt)]
                                print "LIST OF NEW BUS"
                                print listOfCoachBus
                                print listOfAvailableDrivers
                                if len(listOfAvailableDrivers) < len(listOfCoachBus):
                                    addingSuccess = False
                                else:
                                    result, listOfAvailableDrivers = matchVehicleDriver(listOfCoachBus, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                    print result
                                    if result == False:
                                        addingSuccess = False
                                    else:
                                        for x in result:
                                            finalRResource.append(x)
                                        print "yahoo"
                                        print finalRResource

                    print "FINALLY"
                    print addingSuccess
                else:
                    addingSuccess = False
            if int(noOfLorries) > 0 and addingSuccess:
                print "omglorrymax" + noOfLorries
                oneTonAmt = request.POST['oneTonAmt']
                threeTonAmt = request.POST['threeTonAmt']
                fiveTonAmt = request.POST['fiveTonAmt']
                if int(oneTonAmt)+int(threeTonAmt)+int(fiveTonAmt) == int(noOfLorries):
                    print "hello"
                    if int(oneTonAmt) > 0:
                        oneTonParams = [
                            'l',
                            1,
                            coyId,
                            endDateTime,
                            startDateTime,
                            'l',
                            1,
                            coyId
                        ]
                        listOfOneTonLorry = dbaccess.getAvailableLorries(oneTonParams)
                        print len(listOfOneTonLorry)
                        if len(listOfOneTonLorry) < int(oneTonAmt):
                            addingSuccess = False
                        else:
                            print "LIST OF LORRY"
                            print listOfOneTonLorry
                            listOfOneTonLorry = listOfOneTonLorry[:int(oneTonAmt)]
                            print "LIST OF NEW LORRY"
                            print listOfOneTonLorry
                            print listOfAvailableDrivers
                            if len(listOfAvailableDrivers) < len(listOfOneTonLorry):
                                addingSuccess = False
                            else:
                                result, listOfAvailableDrivers = matchVehicleDriver(listOfOneTonLorry, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                print result
                                if result == False:
                                    addingSuccess = False
                                else:
                                    for x in result:
                                        finalRResource.append(x)
                                    print "yahoo"
                                    print finalRResource

                    if addingSuccess:
                        if int(threeTonAmt) > 0:
                            threeTonParams = [
                                'l',
                                3,
                                coyId,
                                endDateTime,
                                startDateTime,
                                'l',
                                3,
                                coyId
                            ]
                            listOfThreeTonLorry = dbaccess.getAvailableLorries(threeTonParams)
                            print listOfThreeTonLorry
                            if len(listOfThreeTonLorry) < int(threeTonAmt):
                                addingSuccess = False
                            else:
                                print "LIST OF LORRY"
                                print listOfThreeTonLorry
                                listOfThreeTonLorry = listOfThreeTonLorry[:int(threeTonAmt)]
                                print "LIST OF NEW LORRY"
                                print listOfThreeTonLorry
                                print listOfAvailableDrivers
                                if len(listOfAvailableDrivers) < len(listOfThreeTonLorry):
                                    addingSuccess = False
                                else:
                                    result, listOfAvailableDrivers = matchVehicleDriver(listOfThreeTonLorry, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                    print result
                                    if result == False:
                                        addingSuccess = False
                                    else:
                                        for x in result:
                                            finalRResource.append(x)
                                        print "yahoo"
                                        print finalRResource
                    if addingSuccess:
                        if int(fiveTonAmt) > 0:
                            fiveTonParams = [
                                'l',
                                5,
                                coyId,
                                endDateTime,
                                startDateTime,
                                'l',
                                5,
                                coyId
                            ]
                            listOfFiveTonLorry = dbaccess.getAvailableLorries(fiveTonParams)

                            if len(listOfFiveTonLorry) < int(fiveTonAmt):
                                addingSuccess = False
                            else:
                                print "LIST OF LORRY"
                                print listOfFiveTonLorry
                                listOfFiveTonLorry = listOfFiveTonLorry[:int(fiveTonAmt)]
                                print "LIST OF NEW LORRY"
                                print listOfFiveTonLorry
                                print listOfAvailableDrivers
                                if len(listOfAvailableDrivers) < len(listOfFiveTonLorry):
                                    addingSuccess = False
                                else:
                                    result, listOfAvailableDrivers = matchVehicleDriver(listOfFiveTonLorry, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                                    print result
                                    if result == False:
                                        addingSuccess = False
                                    else:
                                        for x in result:
                                            finalRResource.append(x)
                                        print "yahoo"
                                        print finalRResource

                    print "FINALLY"
                    print addingSuccess
                else:
                    addingSuccess = False

            if addingSuccess:
                params = [
                    tripId,
                    startDateTime,
                    endDateTime,
                    request.POST['startLocation'],
                    request.POST['endLocation'],
                    request.POST['comments'],
                    jobId,
                    cusId
                ]

                dbaccess.insertTrip(params)
                print "OVERALL A SUCCESS"
                for x in finalRResource:
                    resourceParams = [
                        x[0],
                        x[1],
                        x[2],
                        x[3],
                        x[4],
                        x[5],
                        x[6]
                    ]
                    dbaccess.insertReqResource(resourceParams)

            return HttpResponseRedirect('/customer/addTrip')
    else:
        form = TripForm()

    return render_to_response('customer/addTrip.html', {
        'form': form
    }, context_instance=RequestContext(request))


def matchVehicleDriver(listOfAvailableVehicles, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId):
    listOfAvailableVehicles = list(list(x) for x in listOfAvailableVehicles)
    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
    listOfRResource = []
    for vehicle in listOfAvailableVehicles:
        rResource = range(7)
        print vehicle[0]
        if vehicle[2] == "3a":
            found = False
            bestNumber = -1
            index = -1
            for i, driver in enumerate(listOfAvailableDrivers):
                if driver[1] == "5" or driver[1] == "4" or driver[1] == "4a" or driver[1] == "3" or driver[1] == "3a":
                    #FOUND A DRIVER!!!
                    found = True
                    if bestNumber == -1:
                        bestNumber = driver[1]
                        index = i
                    if bestNumber == "3":
                        if driver[1] == "3a":
                            bestNumber = driver[1]
                            index = i
                    if bestNumber == "4a":
                        if driver[1] == "3" or driver[1] == "3a":
                            bestNumber = driver[1]
                            index = i
                    if bestNumber == 4:
                        if driver[1] == "4a" or driver[1] == "3" or driver[1] == "3a":
                            bestNumber = driver[1]
                            index = i
                    if bestNumber == 5:
                        if driver[1] == "4" or driver[1] == "4a" or driver[1] == "3" or driver[1] == "3a":
                            bestNumber = driver[1]
                            index = i
            if found:
                rResource[0] = vehicle[0]
                rResource[1] = roundTrip
                rResource[2] = listOfAvailableDrivers[index][0]
                rResource[3] = coyId
                rResource[4] = tripId
                rResource[5] = jobId
                rResource[6] = cusId
                listOfRResource.append(rResource)
                listOfAvailableDrivers.pop(index)
            if not found:
                return False, False

        if vehicle[2] == "3":
            found = False
            bestNumber = -1
            index = -1
            for i, driver in enumerate(listOfAvailableDrivers):
                if driver[1] == "5" or driver[1] == "4" or driver[1] == "4a" or driver[1] == "3":
                    #FOUND A DRIVER!!!
                    found = True
                    if bestNumber == -1:
                        bestNumber = driver[1]
                        index = i
                    if bestNumber == "4a":
                        if driver[1] == "3":
                            bestNumber = driver[1]
                            index = i
                    if bestNumber == 4:
                        if driver[1] == "4a" or driver[1] == "3":
                            bestNumber = driver[1]
                            index = i
                    if bestNumber == 5:
                        if driver[1] == "4" or driver[1] == "4a" or driver[1] == "3":
                            bestNumber = driver[1]
                            index = i
            if found:
                rResource[0] = vehicle[0]
                rResource[1] = roundTrip
                rResource[2] = listOfAvailableDrivers[index][0]
                rResource[3] = coyId
                rResource[4] = tripId
                rResource[5] = jobId
                rResource[6] = cusId
                listOfRResource.append(rResource)
                listOfAvailableDrivers.pop(index)
            if not found:
                return False, False

        if vehicle[2] == "4a":
            found = False
            bestNumber = -1
            index = -1
            for i, driver in enumerate(listOfAvailableDrivers):
                if driver[1] == "5" or driver[1] == "4" or driver[1] == "4a":
                    #FOUND A DRIVER!!!
                    found = True
                    if bestNumber == -1:
                        bestNumber = driver[1]
                        index = i
                    if bestNumber == 4:
                        if driver[1] == "4a":
                            bestNumber== driver[1]
                            index = i
                    if bestNumber == 5:
                        if driver[1] == "4" or driver[1] == "4a":
                            bestNumber = driver[1]
                            index = i
            if found:
                rResource[0] = vehicle[0]
                rResource[1] = roundTrip
                rResource[2] = listOfAvailableDrivers[index][0]
                rResource[3] = coyId
                rResource[4] = tripId
                rResource[5] = jobId
                rResource[6] = cusId
                listOfRResource.append(rResource)
                listOfAvailableDrivers.pop(index)
            if not found:
                return False, False

        if vehicle[2] == "4":
            found = False
            bestNumber = -1
            index = -1
            for i, driver in enumerate(listOfAvailableDrivers):
                if driver[1] == "5" or driver[1] == "4":
                    #FOUND A DRIVER!!!
                    found = True
                    if bestNumber == -1:
                        bestNumber = driver[1]
                        index = i
                    if bestNumber == 5:
                        if driver[1] == "4":
                            bestNumber = driver[1]
                            index = i
            if found:
                rResource[0] = vehicle[0]
                rResource[1] = roundTrip
                rResource[2] = listOfAvailableDrivers[index][0]
                rResource[3] = coyId
                rResource[4] = tripId
                rResource[5] = jobId
                rResource[6] = cusId
                listOfRResource.append(rResource)
                listOfAvailableDrivers.pop(index)
            if not found:
                return False, False

        if vehicle[2] == "5":
            found = False
            for driver in listOfAvailableDrivers:
                if driver[1] == "5":
                    #FOUND A DRIVER!!!
                    found = True
                    rResource[0] = vehicle[0]
                    rResource[1] = roundTrip
                    rResource[2] = driver[0]
                    rResource[3] = coyId
                    rResource[4] = tripId
                    rResource[5] = jobId
                    rResource[6] = cusId
                    listOfRResource.append(rResource)
                    listOfAvailableDrivers.pop(index)
            if not found:
                return False, False

    return listOfRResource, tuple(tuple(x) for x in listOfAvailableDrivers)


def viewJobs(request):
    cusId = 1 #userProfileDBAccess.getCustIdByUserId(request.user.id)
    listOfJobs = list(list(x) for x in dbaccess.getAllJobsByCusId(cusId))
    for x in listOfJobs:
        x[1] = x[1].date().strftime("%d-%m-%Y")
    print listOfJobs
    return render_to_response('customer/viewJobs.html', {
        'listOfJobs': listOfJobs
    }, context_instance=RequestContext(request))


def viewTripsOfJob(request):
    jobId = request.get_full_path().split('=')[1]
    print jobId
    listOfTrips = list(list(x) for x in dbaccess.getAllTripsByJobId(jobId))
    for x in listOfTrips:
        x[1] = x[1].strftime("%d-%m-%Y %H:%M:%S")
        x[2] = x[2].strftime("%d-%m-%Y %H:%M:%S")
    print listOfTrips

    return render_to_response('customer/viewTripsOfJob.html', {
        'listOfTrips': listOfTrips,
        'jobId': jobId
    }, context_instance=RequestContext(request))


def deleteTripOfJob(request):
    tripId = request.get_full_path().split('=')[1]
    print "OMG"
    print tripId
    jobId = dbaccess.getJobOfTrip(tripId)
    dbaccess.deleteTrip(tripId)
    listOfTrips = dbaccess.getAllTripsByJobId(jobId)
    if len(listOfTrips) == 0:
        dbaccess.deleteJob(jobId)
        return HttpResponseRedirect('/customer/viewJobs')

    return HttpResponseRedirect('/customer/viewJobs/j_id=' + str(jobId))


def editTripOfJob(request):
    tripId = request.get_full_path().split('=')[1]
    tripRow = dbaccess.getTripDetails(tripId)
    tripReqResources = dbaccess.getReqResourceByTripId(tripId)
    jobId = dbaccess.getJobOfTrip(tripId)
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            #addTrip
            '''params = [
                request.POST['coyName'],
                request.POST['email'],
                request.POST['faxNo'],
                request.POST['coyContactNo'],
                request.POST['zipcode'],
                request.POST['streetName'],
                coyRow[0]
            ]
            dbaccess.updateCompany(params)'''
            return HttpResponseRedirect('/customer/viewJobs/j_id=' + str(jobId))
    else:
        startDate = str(tripRow[0][1]).split(" ")[0]
        year, month, day = startDate.split("-")
        startDate = day+"-"+month+"-"+year
        startTime = str(tripRow[0][1]).split(" ")[1][:5]
        EndDate = str(tripRow[0][2]).split(" ")[0]
        year, month, day = EndDate.split("-")
        EndDate = day+"-"+month+"-"+year
        EndTime = str(tripRow[0][2]).split(" ")[1][:5]
        startLocation = tripRow[0][3]
        endLocation = tripRow[0][4]
        comments = tripRow[0][5]
        roundTrip = tripReqResources[0][1]
        if roundTrip == 'y':
            roundTrip = 'YES'
        elif roundTrip == 'n':
            roundTrip = 'NO'
        params = ['sedan', tripId]
        noOfSedanCars = dbaccess.getNoOfCarsByCarplateNos(params)
        params = ['mpv', tripId]
        noOfMpvCars = dbaccess.getNoOfCarsByCarplateNos(params)
        params = ['luxury', tripId]
        noOfLuxuryCars = dbaccess.getNoOfCarsByCarplateNos(params)
        params = ['bus', tripId]
        noOfBusBus = dbaccess.getNoOfBusesByCarplateNos(params)
        params = ['mini', tripId]
        noOfMiniBus = dbaccess.getNoOfBusesByCarplateNos(params)
        params = ['coach', tripId]
        noOfCoachBus = dbaccess.getNoOfBusesByCarplateNos(params)
        params = [ 1, tripId]
        noOfOneTonLorry = dbaccess.getNoOfLorriesByCarplateNos(params)
        params = [3, tripId]
        noOfThreeTonLorry = dbaccess.getNoOfLorriesByCarplateNos(params)
        params = [5, tripId]
        noOfFiveTonLorry = dbaccess.getNoOfLorriesByCarplateNos(params)
        noOfCars = noOfSedanCars+noOfMpvCars+noOfLuxuryCars
        noOfBuses = noOfBusBus+noOfMiniBus+noOfCoachBus
        noOfLorries = noOfOneTonLorry+noOfThreeTonLorry+noOfFiveTonLorry

        form = TripForm(initial={
            'startDate': startDate,
            'startTime': startTime,
            'endDate': EndDate,
            'endTime': EndTime,
            'startLocation': startLocation,
            'endLocation': endLocation,
            'comments': comments,
            'roundTrip': roundTrip,
            'noOfCars': noOfCars,
            'noOfBuses': noOfBuses,
            'noOfLorries': noOfLorries,
        })

    return render_to_response('customer/editTrip.html', {
        'form': form,
        'noOfCarsInitial': noOfCars,
        'noOfBusesInitial': noOfBuses,
        'noOfLorriesInitial': noOfLorries,
        'sedanAmt': noOfSedanCars,
        'mpvAmt': noOfMpvCars,
        'luxuryAmt': noOfLuxuryCars,
        'busAmt': noOfBusBus,
        'miniAmt': noOfMiniBus,
        'coachAmt': noOfCoachBus,
        'oneTonAmt': noOfOneTonLorry,
        'threeTonAmt': noOfThreeTonLorry,
        'fiveTonAmt': noOfFiveTonLorry,
        'asd': [i for i in range(11)]
    }, context_instance=RequestContext(request))


def searchCompany(request):
    if request.method == 'POST':
        form = companySearchForm(request.POST)
        if form.is_valid():
            coyNameArray = request.POST['coyName'].split(",")
            streetNameArray = request.POST['streetName'].split(",")
            companyResult = dbaccess.searchCompanies(coyNameArray, streetNameArray)
            companyResultArray = dictfetchall(companyResult)

            request.session['companyResultArray'] = companyResultArray
            return HttpResponseRedirect('/customer/searchCompanyResults')
    else:
        form = companySearchForm()

    return render_to_response('customer/searchCompany.html', {
        'form': form
    }, context_instance=RequestContext(request))


def searchCompanyResults(request):
    return render_to_response('customer/searchCompanyResults.html', {
    }, context_instance=RequestContext(request))


def searchVehicle(request):
    if request.method == 'POST':
        form = companySearchForm(request.POST)
        if form.is_valid():

            coyNames = request.POST['coyName']
            streetNames = request.POST['streetName']
            coyNameArray = coyNames.split(",")
            streetNameArray = streetNames.split(",")
            cursor = connection.cursor()
            query = "SELECT * FROM company WHERE "

            if coyNameArray:
                query = query + "(coyName LIKE "
                for x in coyNameArray:
                    query = query + "'%s' OR coyName LIKE " % (x)

                query = query[:-18] + "') AND "

            if streetNameArray:
                query = query + "(streetName LIKE "
                for x in streetNameArray:
                    query = query + "'%s' OR streetName LIKE " % (x)

                query = query[:-21] + "') AND "
            query = query[:-5]
            print query
            companyResult = cursor.execute(query)
            companyResultArray = dictfetchall(companyResult)
            #print companyResultArray

            request.session['companyResultArray'] = companyResultArray
            return HttpResponseRedirect('/customer/searchVehicleResults')
    else:
        form = companySearchForm()

    return render_to_response('customer/searchVehicle.html', {
        'form': form
    }, context_instance=RequestContext(request))


def searchVehicleResults(request):
    return render_to_response('customer/searchVehicleResults.html', {
    }, context_instance=RequestContext(request))