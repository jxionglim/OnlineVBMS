from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from customer.models import JobForm, searchCompanyByLocationForm, TripForm, searchCompanyByVehicleForm, searchCompanyByVehicleAmtForm
import datetime
import dbaccess
from copy import copy, deepcopy
import userprofile.dbaccess as userProfileDBAccess
from django.views.decorators.csrf import csrf_exempt


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@csrf_exempt
def addJob(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            jobId = dbaccess.getMaxJobId()+1
            cusId = userProfileDBAccess.getCustIdByUserId(request.user.id)
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

@csrf_exempt
def addTrip(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = TripForm(request, request.POST)
        if form.is_valid():
            jobId = request.session.get('jobId')
            cusId = userProfileDBAccess.getCustIdByUserId(request.user.id)
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
            finalRResource = []
            driverParams = [
                coyId,
                endDateTime,
                startDateTime,
                coyId
            ]
            listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
            addingSuccess = True
            sedanAmt = request.POST['sedanAmt']
            mpvAmt = request.POST['mpvAmt']
            luxuryAmt = request.POST['luxuryAmt']
            busAmt = request.POST['busAmt']
            miniAmt = request.POST['miniAmt']
            coachAmt = request.POST['coachAmt']
            oneTonAmt = request.POST['oneTonAmt']
            threeTonAmt = request.POST['threeTonAmt']
            fiveTonAmt = request.POST['fiveTonAmt']

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
                    listOfSedanCars = listOfSedanCars[:int(sedanAmt)]
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
                    if len(listOfMpvCars) < int(mpvAmt):
                        addingSuccess = False
                    else:
                        listOfMpvCars = listOfMpvCars[:int(mpvAmt)]
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
                        listOfLuxuryCars = listOfLuxuryCars[:int(luxuryAmt)]
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

            if addingSuccess:
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
                        listOfBusBus = listOfBusBus[:int(busAmt)]
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
                    if len(listOfMiniBus) < int(miniAmt):
                        addingSuccess = False
                    else:
                        listOfMiniBus = listOfMiniBus[:int(miniAmt)]
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
                        listOfCoachBus = listOfCoachBus[:int(coachAmt)]
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

            if addingSuccess:
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
                    if len(listOfOneTonLorry) < int(oneTonAmt):
                        addingSuccess = False
                    else:
                        listOfOneTonLorry = listOfOneTonLorry[:int(oneTonAmt)]
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
                    if len(listOfThreeTonLorry) < int(threeTonAmt):
                        addingSuccess = False
                    else:
                        listOfThreeTonLorry = listOfThreeTonLorry[:int(threeTonAmt)]
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
                        listOfFiveTonLorry = listOfFiveTonLorry[:int(fiveTonAmt)]
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

            if addingSuccess:
                overallSuccess = True
                print tripId
                print jobId
                print cusId

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
            else:
                overallSuccess = False
                print "OVERALL A FAIL"

            return render_to_response('customer/addTrip.html', {
                'form': TripForm(request),
                'overallSuccess': overallSuccess
            }, context_instance=RequestContext(request))
    else:
        form = TripForm(request)

    return render_to_response('customer/addTrip.html', {
        'form': form,
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
            for i, driver in enumerate(listOfAvailableDrivers):
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
                    listOfAvailableDrivers.pop(i)
                    break
            if not found:
                return False, False

    return listOfRResource, tuple(tuple(x) for x in listOfAvailableDrivers)

@csrf_exempt
def viewJobs(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    cusId = userProfileDBAccess.getCustIdByUserId(request.user.id)
    listOfJobs = list(list(x) for x in dbaccess.getAllJobsByCusId(cusId))
    for x in listOfJobs:
        x[1] = x[1].date().strftime("%d-%m-%Y")
    print listOfJobs
    return render_to_response('customer/viewJobs.html', {
        'listOfJobs': listOfJobs
    }, context_instance=RequestContext(request))

@csrf_exempt
def viewTripsOfJob(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
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

@csrf_exempt
def deleteTripOfJob(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
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

@csrf_exempt
def editTripOfJob(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    tripId = request.get_full_path().split('=')[1]
    tripRow = dbaccess.getTripDetails(tripId)
    coyId = dbaccess.getCoyOfTrip(tripId)
    cusId = userProfileDBAccess.getCustIdByUserId(request.user.id)
    startDateTime = datetime.datetime.strptime(str(tripRow[0][1]), "%Y-%m-%d %H:%M:%S")
    endDateTime = datetime.datetime.strptime(str(tripRow[0][2]), "%Y-%m-%d %H:%M:%S")

    tripReqResources = list(list(x) for x in dbaccess.getReqResourceByTripId(tripId))
    print "ORIGINAL"
    print tripReqResources
    tempTripReqResources = deepcopy(tripReqResources)
    confirmTakeOutResources = []
    tempTakeOutTripReqResources = []
    jobId = dbaccess.getJobOfTrip(tripId)
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
    params = [1, tripId]
    noOfOneTonLorry = dbaccess.getNoOfLorriesByCarplateNos(params)
    params = [3, tripId]
    noOfThreeTonLorry = dbaccess.getNoOfLorriesByCarplateNos(params)
    params = [5, tripId]
    noOfFiveTonLorry = dbaccess.getNoOfLorriesByCarplateNos(params)
    if request.method == 'POST':
        form = TripForm(request, request.POST)
        if form.is_valid():
            roundTrip = request.POST['roundTrip']
            if roundTrip == "YES":
                roundTrip = "y"
            elif roundTrip == "NO":
                roundTrip = "n"
            startDate = request.POST['startDate']
            startTime = request.POST['startTime']
            endDate = request.POST['endDate']
            endTime = request.POST['endTime']
            changedStartDateTimeString = startDate+" "+startTime+":00"
            changedEndDateTimeString = endDate+" "+endTime+":00"
            changedStartDateTime = datetime.datetime.strptime(changedStartDateTimeString, "%d-%m-%Y %H:%M:%S")
            changedEndDateTime = datetime.datetime.strptime(changedEndDateTimeString, "%d-%m-%Y %H:%M:%S")
            print changedStartDateTime
            print changedEndDateTime
            if changedEndDateTime > changedStartDateTime:
                dateChanged = True
                if startDateTime == changedStartDateTime and endDateTime == changedEndDateTime:
                    dateChanged = False

                #-------------------- START FOR CAR ---------------------
                #-----------START-------------
                params = ['sedan', tripId]
                originalTripSedan = list(list(x) for x in dbaccess.getListOfCarsByCategoryAndTripIdByDrivingClass(params))

                tempOriginalTripSedan = deepcopy(originalTripSedan)
                print originalTripSedan

                sedanAmtChanged = request.POST['sedanAmt']
                mpvAmtChanged = request.POST['mpvAmt']
                luxuryAmtChanged = request.POST['luxuryAmt']
                busAmtChanged = request.POST['busAmt']
                miniAmtChanged = request.POST['miniAmt']
                coachAmtChanged = request.POST['coachAmt']
                oneTonAmtChanged = request.POST['oneTonAmt']
                threeTonAmtChanged = request.POST['threeTonAmt']
                fiveTonAmtChanged = request.POST['fiveTonAmt']

                addingSuccess = True
                if len(originalTripSedan) > 0:
                    if dateChanged:
                        for entry in originalTripSedan:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u, no clash la"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripSedan.remove(entry)
                originalTripSedan = tempOriginalTripSedan
                print originalTripSedan
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------

                #-----------START-------------
                params = ['mpv', tripId]
                originalTripMPV = list(list(x) for x in dbaccess.getListOfCarsByCategoryAndTripIdByDrivingClass(params))
                tempOriginalTripMPV = deepcopy(originalTripMPV)

                if len(originalTripMPV) > 0:
                    if dateChanged:
                        for entry in originalTripMPV:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        confirmTakeOutResources.append(rr)
                                        tempTripReqResources.remove(rr)
                                tempOriginalTripMPV.remove(entry)
                originalTripMPV = tempOriginalTripMPV
                print "----------------MPVMPVMMPV----------------------"
                print tempOriginalTripMPV
                #final array
                print tempTripReqResources
                #array that can be used for later
                print tempTakeOutTripReqResources
                print "----------------MPVMPVMMPV----------------------"

                #-----------END-------------

                #-----------START-------------
                params = ['luxury', tripId]
                originalTripLUXURY = list(list(x) for x in dbaccess.getListOfCarsByCategoryAndTripIdByDrivingClass(params))
                tempOriginalTripLUXURY = deepcopy(originalTripLUXURY)

                if len(originalTripLUXURY) > 0:
                    if dateChanged:
                        for entry in originalTripLUXURY:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripLUXURY.remove(entry)
                originalTripLUXURY = tempOriginalTripLUXURY
                print originalTripLUXURY
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------
                #-------------------- END FOR CAR ---------------------


                #-------------------- START FOR BUS ---------------------
                #-----------START-------------
                params = ['bus', tripId]
                originalTripBUS = list(list(x) for x in dbaccess.getListOfBusesByCategoryAndTripIdByDrivingClass(params))
                tempOriginalTripBUS = deepcopy(originalTripBUS)

                if len(originalTripBUS) > 0:
                    if dateChanged:
                        for entry in originalTripBUS:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripBUS.remove(entry)
                originalTripBUS = tempOriginalTripBUS
                print originalTripBUS
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------

                #-----------START-------------
                params = ['mini', tripId]
                originalTripMINI = list(list(x) for x in dbaccess.getListOfBusesByCategoryAndTripIdByDrivingClass(params))
                tempOriginalTripMINI = deepcopy(originalTripMINI)

                if len(originalTripMINI) > 0:
                    if dateChanged:
                        for entry in originalTripMINI:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripMINI.remove(entry)
                originalTripMINI = tempOriginalTripMINI
                print originalTripMINI
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------

                #-----------START-------------
                params = ['coach', tripId]
                originalTripCOACH = list(list(x) for x in dbaccess.getListOfBusesByCategoryAndTripIdByDrivingClass(params))
                tempOriginalTripCOACH = deepcopy(originalTripCOACH)

                if len(originalTripCOACH) > 0:
                    if dateChanged:
                        for entry in originalTripCOACH:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripCOACH.remove(entry)
                originalTripCOACH = tempOriginalTripCOACH
                print originalTripCOACH
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------
                #-------------------- END FOR BUS ---------------------



                #-------------------- START FOR LORRY ---------------------
                #-----------START-------------
                params = [1, tripId]
                originalTripOneTon = list(list(x) for x in dbaccess.getListOfLorriesByTonsAndTripIdByDrivingClass(params))
                tempOriginalTripOneTon = deepcopy(originalTripOneTon)

                if len(originalTripOneTon) > 0:
                    if dateChanged:
                        for entry in originalTripOneTon:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripOneTon.remove(entry)
                originalTripOneTon = tempOriginalTripOneTon
                print originalTripOneTon
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------

                #-----------START-------------
                params = [3, tripId]
                originalTripThreeTon = list(list(x) for x in dbaccess.getListOfLorriesByTonsAndTripIdByDrivingClass(params))
                tempOriginalTripThreeTon = deepcopy(originalTripThreeTon)

                if len(originalTripThreeTon) > 0:
                    if dateChanged:
                        for entry in originalTripThreeTon:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripThreeTon.remove(entry)
                originalTripThreeTon = tempOriginalTripThreeTon
                print originalTripThreeTon
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------

                #-----------START-------------
                params = [5, tripId]
                originalTripFiveTon = list(list(x) for x in dbaccess.getListOfLorriesByTonsAndTripIdByDrivingClass(params))
                tempOriginalTripFiveTon = deepcopy(originalTripFiveTon)

                if len(originalTripFiveTon) > 0:
                    if dateChanged:
                        for entry in originalTripFiveTon:
                            params = [
                                tripId,
                                entry[1],
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                                changedStartDateTimeString,
                                changedEndDateTimeString,
                            ]
                            ifDriverId = dbaccess.checkTimingClash(params)
                            if ifDriverId == 0:
                                print "good for u"
                            else:
                                for rr in tempTripReqResources:
                                    if int(entry[0]) == int(rr[0]):
                                        tempTripReqResources.remove(rr)
                                        confirmTakeOutResources.append(rr)
                                tempOriginalTripFiveTon.remove(entry)
                originalTripFiveTon = tempOriginalTripFiveTon
                print originalTripFiveTon
                print tempTripReqResources
                print confirmTakeOutResources

                #-----------END-------------
                #-------------------- END FOR LORRY ---------------------

                print "===============================V5B==========================="
                #original array
                print tripReqResources
                #final array
                print tempTripReqResources
                #array that can be used for later
                print tempTakeOutTripReqResources
                #array that cannot be used anymore
                print confirmTakeOutResources
                print "===================================V5B========================="

                #get inputvalues
                sedanIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if int(sedanAmtChanged) < len(originalTripSedan):
                    difference = len(originalTripSedan) - int(sedanAmtChanged)
                    for rr in originalTripSedan:
                        carplateNoToRemove = int(rr[0])
                        if difference > 0:
                            for ttrr in tempTripReqResources:
                                if int(ttrr[0]) == carplateNoToRemove:
                                    difference -= 1
                                    temporaryTempTripReqResources.remove(ttrr)
                                    tempTakeOutTripReqResources.append(ttrr)
                                    break
                        else:
                            break
                elif int(sedanAmtChanged) > len(originalTripSedan):
                    sedanIncrease = True

                tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                print "VB"
                #final array
                print tempTripReqResources
                #array that can be used for later
                print tempTakeOutTripReqResources
                print "VB"

                mpvIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(mpvAmtChanged) < len(originalTripMPV):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripMPV) - int(mpvAmtChanged)
                        for rr in originalTripMPV:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(mpvAmtChanged) > len(originalTripMPV):
                        mpvIncrease = True

                print "========================qq============================="
                tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                #final array
                print tempTripReqResources
                #array that can be used for later
                print tempTakeOutTripReqResources
                #array that cannot be used anymore
                print confirmTakeOutResources
                print addingSuccess
                print "======================qq============================"


                luxuryIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(luxuryAmtChanged) < len(originalTripLUXURY):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripLUXURY) - int(luxuryAmtChanged)
                        for rr in originalTripLUXURY:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(luxuryAmtChanged) > len(originalTripLUXURY):
                        luxuryIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                    print "VB"
                    #final array
                    print tempTripReqResources
                    #array that can be used for later
                    print tempTakeOutTripReqResources
                    print "VB"


                if sedanIncrease:
                    print "hehe"
                    difference = int(sedanAmtChanged) - len(originalTripSedan)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER==========="
                    print listOfAvailableDrivers
                    sedanParams = [
                        'c',
                        'sedan',
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'c',
                        'sedan',
                        coyId
                    ]
                    listOfSedanCars = dbaccess.getAvailableCars(sedanParams)
                    listOfSedanCars = list(list(x) for x in listOfSedanCars)
                    tempList = deepcopy(listOfSedanCars)
                    for x in listOfSedanCars:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfSedanCars = deepcopy(tempList)
                    if len(listOfSedanCars) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfSedanCars
                        listOfSedanCars = listOfSedanCars[:difference]
                        print "LIST OF NEW CAR"

                        copyListOfSedanCars = deepcopy(listOfSedanCars)
                        for car in listOfSedanCars:
                            if car[2] == "3a":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3" or dClass == "3a":
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
                                    copyListOfSedanCars.remove(car)
                                    tempTakeOutTripReqResources[index][0] = car[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))

                            if car[2] == "3":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3":
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
                                    copyListOfSedanCars.remove(car)
                                    tempTakeOutTripReqResources[index][0] = car[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfSedanCars = copyListOfSedanCars

                        if len(listOfAvailableDrivers) < len(listOfSedanCars):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfSedanCars, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources

                if mpvIncrease:
                    print "hehe"
                    difference = int(mpvAmtChanged) - len(originalTripMPV)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    print "LIST OF DRIVER================="
                    print listOfAvailableDrivers
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER================="
                    print listOfAvailableDrivers
                    mpvParams = [
                        'c',
                        'mpv',
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'c',
                        'mpv',
                        coyId
                    ]
                    listOfMpvCars = dbaccess.getAvailableCars(mpvParams)
                    listOfMpvCars = list(list(x) for x in listOfMpvCars)
                    tempList = deepcopy(listOfMpvCars)
                    print "LIST OF mpvvvvvv================"
                    print listOfMpvCars
                    for x in listOfMpvCars:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfMpvCars = deepcopy(tempList)
                    print "LIST OF mpvvvvvv================"
                    print listOfMpvCars


                    if len(listOfMpvCars) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"

                        listOfMpvCars = listOfMpvCars[:difference]
                        print "=========fgdgf==========dd======"
                        #final array
                        print tempTripReqResources
                        #array that can be used for later
                        print tempTakeOutTripReqResources
                        print listOfMpvCars



                        print "=======dfgf============yy==========dd======"


                        listOfMpvCars = list(list(x) for x in listOfMpvCars)
                        copyListOfMpvCars = deepcopy(listOfMpvCars)
                        for car in listOfMpvCars:
                            if car[2] == "3a":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3" or dClass == "3a":
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
                                    copyListOfMpvCars.remove(car)
                                    tempTakeOutTripReqResources[index][0] = car[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))

                            if car[2] == "3":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3":
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
                                    copyListOfMpvCars.remove(car)
                                    tempTakeOutTripReqResources[index][0] = car[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfMpvCars = copyListOfMpvCars
                        print "==============================yy==========dd======"
                        #final array
                        print tempTripReqResources
                        #array that can be used for later
                        print tempTakeOutTripReqResources
                        print listOfMpvCars
                        print "==============================yy==========dd======"


                        print "LIST OF NEW CAR"
                        print listOfMpvCars
                        print listOfAvailableDrivers
                        print len(listOfMpvCars)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfMpvCars):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfMpvCars, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources
                            #top up from database or tempTakeOutTripReqResources

                if luxuryIncrease:
                    print "hehe1"
                    difference = int(luxuryAmtChanged) - len(originalTripLUXURY)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    luxuryParams = [
                        'c',
                        'luxury',
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'c',
                        'luxury',
                        coyId
                    ]

                    listOfLuxuryCars = dbaccess.getAvailableCars(luxuryParams)
                    listOfLuxuryCars = list(list(x) for x in listOfLuxuryCars)
                    tempList = deepcopy(listOfLuxuryCars)
                    for x in listOfLuxuryCars:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfLuxuryCars = deepcopy(tempList)

                    if len(listOfLuxuryCars) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfLuxuryCars
                        listOfLuxuryCars = listOfLuxuryCars[:difference]
                        print "LIST OF NEW CAR"
                        print listOfLuxuryCars
                        print listOfAvailableDrivers
                        print len(listOfLuxuryCars)
                        print len(listOfAvailableDrivers)

                        listOfLuxuryCars = list(list(x) for x in listOfLuxuryCars)
                        copyListOfLuxuryCars = deepcopy(listOfLuxuryCars)
                        for car in listOfLuxuryCars:
                            if car[2] == "3a":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3" or dClass == "3a":
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
                                    copyListOfLuxuryCars.remove(car)
                                    tempTakeOutTripReqResources[index][0] = car[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))

                            if car[2] == "3":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3":
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
                                    copyListOfLuxuryCars.remove(car)
                                    tempTakeOutTripReqResources[index][0] = car[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfLuxuryCars = copyListOfLuxuryCars
                        print "========dfgd========dfg====="
                        #final array
                        print tempTripReqResources
                        #array that can be used for later
                        print tempTakeOutTripReqResources
                        print listOfLuxuryCars



                        print "======dfg============yy==========dd======"
                        if len(listOfAvailableDrivers) < len(listOfLuxuryCars):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfLuxuryCars, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources
                    #top up from database or tempTakeOutTripReqResources





                #get inputvalues

                busIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(busAmtChanged) < len(originalTripBUS):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripBUS) - int(busAmtChanged)
                        for rr in originalTripBUS:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(busAmtChanged) > len(originalTripBUS):
                        busIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                    print "VB"
                    #final array
                    print tempTripReqResources
                    #array that can be used for later
                    print tempTakeOutTripReqResources
                    print "VB"

                #get inputvalues
                miniIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(miniAmtChanged) < len(originalTripMINI):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripMINI) - int(miniAmtChanged)
                        for rr in originalTripMINI:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(miniAmtChanged) > len(originalTripMINI):
                        miniIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                    print "VB"
                    #final array
                    print tempTripReqResources
                    #array that can be used for later
                    print tempTakeOutTripReqResources
                    print "VB"

                #get inputvalues
                coachIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(coachAmtChanged) < len(originalTripCOACH):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripCOACH) - int(coachAmtChanged)
                        for rr in originalTripCOACH:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(coachAmtChanged) > len(originalTripCOACH):
                        coachIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                    print "V4B"
                    #final array
                    print tempTripReqResources
                    #array that can be used for later
                    print tempTakeOutTripReqResources
                    print "V4B"



                if busIncrease:
                    print "hehe"
                    difference = int(busAmtChanged) - len(originalTripBUS)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    busParams = [
                        'b',
                        'bus',
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'b',
                        'bus',
                        coyId
                    ]

                    listOfBusBus = dbaccess.getAvailableBuses(busParams)
                    listOfBusBus = list(list(x) for x in listOfBusBus)
                    tempList = deepcopy(listOfBusBus)
                    for x in listOfBusBus:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfBusBus = deepcopy(tempList)
                    if len(listOfBusBus) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfBusBus
                        listOfBusBus = listOfBusBus[:difference]

                        listOfBusBus = list(list(x) for x in listOfBusBus)
                        copyListOfBusBus = deepcopy(listOfBusBus)
                        for bus in listOfBusBus:
                            if bus[2] == "4a":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a":
                                        #FOUND A DRIVER!!!
                                        found = True
                                        if bestNumber == -1:
                                            bestNumber = driver[1]
                                            index = i
                                        if bestNumber == 4:
                                            if driver[1] == "4a" or driver[1]:
                                                bestNumber = driver[1]
                                                index = i
                                        if bestNumber == 5:
                                            if driver[1] == "4" or driver[1] == "4a":
                                                bestNumber = driver[1]
                                                index = i
                                if found:
                                    copyListOfBusBus.remove(bus)
                                    tempTakeOutTripReqResources[index][0] = bus[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))

                            if bus[2] == "4":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4":
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
                                    copyListOfBusBus.remove(bus)
                                    tempTakeOutTripReqResources[index][0] = bus[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfBusBus = copyListOfBusBus


                        print "LIST OF NEW CAR"
                        print listOfBusBus
                        print listOfAvailableDrivers
                        print len(listOfBusBus)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfBusBus):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfBusBus, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources

                if miniIncrease:
                    print "hehe"
                    difference = int(miniAmtChanged) - len(originalTripMINI)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    miniParams = [
                        'b',
                        'mini',
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'b',
                        'mini',
                        coyId
                    ]

                    listOfMiniBus = dbaccess.getAvailableBuses(miniParams)
                    listOfMiniBus = list(list(x) for x in listOfMiniBus)
                    tempList = deepcopy(listOfMiniBus)
                    for x in listOfMiniBus:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfMiniBus = deepcopy(tempList)
                    if len(listOfMiniBus) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfMiniBus
                        listOfMiniBus = listOfMiniBus[:difference]



                        listOfMiniBus = list(list(x) for x in listOfMiniBus)
                        copyListOfMiniBus = deepcopy(listOfMiniBus)
                        for bus in listOfMiniBus:
                            if bus[2] == "4a":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a":
                                        #FOUND A DRIVER!!!
                                        found = True
                                        if bestNumber == -1:
                                            bestNumber = driver[1]
                                            index = i
                                        if bestNumber == 4:
                                            if driver[1] == "4a" or driver[1]:
                                                bestNumber = driver[1]
                                                index = i
                                        if bestNumber == 5:
                                            if driver[1] == "4" or driver[1] == "4a":
                                                bestNumber = driver[1]
                                                index = i
                                if found:
                                    copyListOfMiniBus.remove(bus)
                                    tempTakeOutTripReqResources[index][0] = bus[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))

                            if bus[2] == "4":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4":
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
                                    copyListOfMiniBus.remove(bus)
                                    tempTakeOutTripReqResources[index][0] = bus[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfMiniBus = copyListOfMiniBus


                        print "LIST OF NEW CAR"
                        print listOfMiniBus
                        print listOfAvailableDrivers
                        print len(listOfMiniBus)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfMiniBus):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfMiniBus, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources
                    #top up from database or tempTakeOutTripReqResources

                if coachIncrease:
                    print "hehe"
                    difference = int(coachAmtChanged) - len(originalTripCOACH)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    coachParams = [
                        'b',
                        'coach',
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'b',
                        'coach',
                        coyId
                    ]

                    listOfCoachBuses = dbaccess.getAvailableBuses(coachParams)
                    listOfCoachBuses = list(list(x) for x in listOfCoachBuses)
                    tempList = deepcopy(listOfCoachBuses)
                    for x in listOfCoachBuses:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfCoachBuses = deepcopy(tempList)
                    if len(listOfCoachBuses) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfCoachBuses
                        listOfCoachBuses = listOfCoachBuses[:difference]


                        listOfCoachBuses = list(list(x) for x in listOfCoachBuses)
                        copyListOfCoachBuses = deepcopy(listOfCoachBuses)
                        for bus in listOfCoachBuses:
                            if bus[2] == "4a":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a":
                                        #FOUND A DRIVER!!!
                                        found = True
                                        if bestNumber == -1:
                                            bestNumber = driver[1]
                                            index = i
                                        if bestNumber == 4:
                                            if driver[1] == "4a" or driver[1]:
                                                bestNumber = driver[1]
                                                index = i
                                        if bestNumber == 5:
                                            if driver[1] == "4" or driver[1] == "4a":
                                                bestNumber = driver[1]
                                                index = i
                                if found:
                                    copyListOfCoachBuses.remove(bus)
                                    tempTakeOutTripReqResources[index][0] = bus[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))

                            if bus[2] == "4":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4":
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
                                    copyListOfCoachBuses.remove(bus)
                                    tempTakeOutTripReqResources[index][0] = bus[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfCoachBuses = copyListOfCoachBuses

                        print "LIST OF NEW CAR"
                        print listOfCoachBuses
                        print listOfAvailableDrivers
                        print len(listOfCoachBuses)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfCoachBuses):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfCoachBuses, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources
                    #top up from database or tempTakeOutTripReqResources






                #get inputvalues
                oneTonIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(oneTonAmtChanged) < len(originalTripOneTon):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripOneTon) - int(oneTonAmtChanged)
                        for rr in originalTripOneTon:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(oneTonAmtChanged) > len(originalTripOneTon):
                        oneTonIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                    print "VB"
                    #final array
                    print tempTripReqResources
                    #array that can be used for later
                    print tempTakeOutTripReqResources
                    print "VB"

                #get inputvalues
                threeTonIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(threeTonAmtChanged) < len(originalTripThreeTon):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripThreeTon) - int(threeTonAmtChanged)
                        for rr in originalTripThreeTon:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(threeTonAmtChanged) > len(originalTripThreeTon):
                        threeTonIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)
                    print "VB"
                    #final array
                    print tempTripReqResources
                    #array that can be used for later
                    print tempTakeOutTripReqResources
                    print "VB"

                #get inputvalues
                fiveTonIncrease = False
                temporaryTempTripReqResources = deepcopy(tempTripReqResources)
                if addingSuccess:
                    if int(fiveTonAmtChanged) < len(originalTripFiveTon):
                        #remove lowest drivingClass from A2 by the difference
                        difference = len(originalTripFiveTon) - int(fiveTonAmtChanged)
                        for rr in originalTripFiveTon:
                            carplateNoToRemove = int(rr[0])
                            if difference > 0:
                                for ttrr in tempTripReqResources:
                                    if int(ttrr[0]) == carplateNoToRemove:
                                        difference -= 1
                                        temporaryTempTripReqResources.remove(ttrr)
                                        tempTakeOutTripReqResources.append(ttrr)
                                        break
                            else:
                                break
                    elif int(fiveTonAmtChanged) > len(originalTripFiveTon):
                        fiveTonIncrease = True

                    tempTripReqResources = deepcopy(temporaryTempTripReqResources)


                if oneTonIncrease:
                    print "hehe2"
                    difference = int(oneTonAmtChanged) - len(originalTripOneTon)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    oneTonParams = [
                        'l',
                        1,
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'l',
                        1,
                        coyId
                    ]

                    listOfOneTonLorry = dbaccess.getAvailableLorries(oneTonParams)
                    listOfOneTonLorry = list(list(x) for x in listOfOneTonLorry)
                    tempList = deepcopy(listOfOneTonLorry)
                    for x in listOfOneTonLorry:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfOneTonLorry = deepcopy(tempList)
                    if len(listOfOneTonLorry) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfOneTonLorry
                        listOfOneTonLorry = listOfOneTonLorry[:difference]
                        listOfOneTonLorry = list(list(x) for x in listOfOneTonLorry)
                        copyListOfOneTonLorry = deepcopy(listOfOneTonLorry)
                        for lorry in listOfOneTonLorry:
                            if lorry[2] == "3":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4" or dClass == "4a" or dClass == "3":
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
                                    copyListOfOneTonLorry.remove(lorry)
                                    tempTakeOutTripReqResources[index][0] = lorry[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfOneTonLorry = copyListOfOneTonLorry










                        print "LIST OF NEW CAR"
                        print listOfOneTonLorry
                        print listOfAvailableDrivers
                        print len(listOfOneTonLorry)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfOneTonLorry):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfOneTonLorry, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources



                if threeTonIncrease:
                    print "hehe"
                    difference = int(threeTonAmtChanged) - len(originalTripThreeTon)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    threeTonParams = [
                        'l',
                        3,
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'l',
                        3,
                        coyId
                    ]

                    listOfThreeTonLorry = dbaccess.getAvailableLorries(threeTonParams)
                    listOfThreeTonLorry = list(list(x) for x in listOfThreeTonLorry)
                    tempList = deepcopy(listOfThreeTonLorry)
                    for x in listOfThreeTonLorry:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[0]):
                                tempList.remove(x)
                    listOfThreeTonLorry = deepcopy(tempList)
                    if len(listOfThreeTonLorry) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfThreeTonLorry
                        listOfThreeTonLorry = listOfThreeTonLorry[:difference]


                        listOfThreeTonLorry = list(list(x) for x in listOfThreeTonLorry)
                        copyListOfThreeTonLorry = deepcopy(listOfThreeTonLorry)
                        for lorry in listOfThreeTonLorry:
                            if lorry[2] == "4":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5" or dClass == "4":
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
                                    copyListOfThreeTonLorry.remove(lorry)
                                    tempTakeOutTripReqResources[index][0] = lorry[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfThreeTonLorry = copyListOfThreeTonLorry







                        print "LIST OF NEW CAR"
                        print listOfThreeTonLorry
                        print listOfAvailableDrivers
                        print len(listOfThreeTonLorry)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfThreeTonLorry):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfThreeTonLorry, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources
                    #top up from database or tempTakeOutTripReqResources



                if fiveTonIncrease:
                    print "hehe"
                    difference = int(fiveTonAmtChanged) - len(originalTripFiveTon)
                    driverParams = [
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        coyId
                    ]
                    listOfAvailableDrivers = dbaccess.getAvailableDrivers(driverParams)
                    listOfAvailableDrivers = list(list(x) for x in listOfAvailableDrivers)
                    tempList = deepcopy(listOfAvailableDrivers)
                    for x in listOfAvailableDrivers:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfAvailableDrivers = deepcopy(tempList)
                    print "LIST OF DRIVER"
                    print listOfAvailableDrivers
                    fiveTonParams = [
                        'l',
                        5,
                        coyId,
                        changedEndDateTimeString,
                        changedStartDateTimeString,
                        'l',
                        5,
                        coyId
                    ]
                    listOfFiveTonLorry = dbaccess.getAvailableLorries(fiveTonParams)
                    listOfFiveTonLorry = list(list(x) for x in listOfFiveTonLorry)
                    tempList = deepcopy(listOfFiveTonLorry)
                    for x in listOfFiveTonLorry:
                        for y in tempTripReqResources:
                            if int(x[0]) == int(y[2]):
                                tempList.remove(x)
                    listOfFiveTonLorry = deepcopy(tempList)
                    if len(listOfFiveTonLorry) < difference:
                        addingSuccess = False
                    else:
                        print "LIST OF CAR"
                        print listOfFiveTonLorry
                        listOfFiveTonLorry = listOfFiveTonLorry[:difference]


                        listOfFiveTonLorry = list(list(x) for x in listOfFiveTonLorry)
                        copyListOfFiveTonLorry = deepcopy(listOfFiveTonLorry)
                        for lorry in listOfFiveTonLorry:
                            if lorry[2] == "5":
                                #found match!
                                found = False
                                bestNumber = -1
                                index = -1
                                for i, driver in enumerate(tempTakeOutTripReqResources):
                                    print driver[2]
                                    dClass = dbaccess.getDrivingClassOfDriver(driver[2])
                                    print dClass
                                    if dClass == "5":
                                        #FOUND A DRIVER!!!
                                        if bestNumber == -1:
                                            found = True
                                            bestNumber = driver[1]
                                            index = i
                                if found:
                                    copyListOfFiveTonLorry.remove(lorry)
                                    tempTakeOutTripReqResources[index][0] = lorry[0]
                                    tempTripReqResources.append(tempTakeOutTripReqResources.pop(index))
                        listOfFiveTonLorry = copyListOfFiveTonLorry


                        print "LIST OF NEW CAR"
                        print listOfFiveTonLorry
                        print listOfAvailableDrivers
                        print len(listOfFiveTonLorry)
                        print len(listOfAvailableDrivers)
                        if len(listOfAvailableDrivers) < len(listOfFiveTonLorry):
                            addingSuccess = False
                        else:
                            result, listOfAvailableDrivers = matchVehicleDriver(listOfFiveTonLorry, listOfAvailableDrivers, roundTrip, coyId, tripId, jobId, cusId)
                            print result
                            if result == False:
                                print "DFF"
                                addingSuccess = False
                            else:
                                for x in result:
                                    tempTripReqResources.append(x)
                                print "yahoo"
                                print tempTripReqResources
                    #top up from database or tempTakeOutTripReqResources



                print "========================qq============================="
                #final array
                print tempTripReqResources
                #array that can be used for later
                print tempTakeOutTripReqResources
                #array that cannot be used anymore
                print confirmTakeOutResources
                print addingSuccess
                print "======================qq============================"


                for y in tempTripReqResources:
                    if y[1] != roundTrip:
                        y[1] = roundTrip

                print "VB"
                #original array
                print tripReqResources
                #final array
                print tempTripReqResources
                #array that can be used for later
                print tempTakeOutTripReqResources
                #array that cannot be used anymore
                print confirmTakeOutResources
                print "VB"
                print addingSuccess

                toDelete = [x for x in tripReqResources if x not in tempTripReqResources]
                toAdd = [x for x in tempTripReqResources if x not in tripReqResources]
                print toDelete
                print toAdd


                if addingSuccess:
                    print tripId
                    print jobId
                    print cusId

                    updatedTripParams = [
                        changedStartDateTimeString,
                        changedEndDateTimeString,
                        request.POST['startLocation'],
                        request.POST['endLocation'],
                        request.POST['comments'],
                        tripId
                    ]
                    dbaccess.updateTrip(updatedTripParams)

                    print "OVERALL A SUCCESS"
                    for x in toDelete:
                        resourceParams = [
                            x[0],
                            x[1],
                            x[2],
                            x[3],
                            x[4],
                            x[5],
                            x[6]
                        ]
                        dbaccess.deleteReqResource(resourceParams)

                    for x in toAdd:
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
                else:
                    print "OVERALL A FAIL"
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

        form = TripForm(request, initial={
            'startDate': startDate,
            'startTime': startTime,
            'endDate': EndDate,
            'endTime': EndTime,
            'startLocation': startLocation,
            'endLocation': endLocation,
            'comments': comments,
            'roundTrip': roundTrip,
            'sedanAmt': noOfSedanCars,
            'mpvAmt': noOfMpvCars,
            'luxuryAmt': noOfLuxuryCars,
            'busAmt': noOfBusBus,
            'miniAmt': noOfMiniBus,
            'coachAmt': noOfCoachBus,
            'oneTonAmt': noOfOneTonLorry,
            'threeTonAmt': noOfThreeTonLorry,
            'fiveTonAmt': noOfFiveTonLorry,
        })

    return render_to_response('customer/editTrip.html', {
        'form': form,
        'tripId': tripId,
        'sedanAmt': noOfSedanCars,
        'mpvAmt': noOfMpvCars,
        'luxuryAmt': noOfLuxuryCars,
        'busAmt': noOfBusBus,
        'miniAmt': noOfMiniBus,
        'coachAmt': noOfCoachBus,
        'oneTonAmt': noOfOneTonLorry,
        'threeTonAmt': noOfThreeTonLorry,
        'fiveTonAmt': noOfFiveTonLorry,
    }, context_instance=RequestContext(request))

@csrf_exempt
def searchCompanyByLocation(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = searchCompanyByLocationForm(request.POST)
        if form.is_valid():
            coyNameArray = request.POST['coyName'].split(",")
            streetNameArray = request.POST['streetName'].split(",")
            for index, item in enumerate(coyNameArray):
                coyNameArray[index] = "%%"+item.lower()+"%%"
            for index, item in enumerate(streetNameArray):
                streetNameArray[index] = "%%"+item.lower()+"%%"
            print coyNameArray
            print streetNameArray
            companyResult = dbaccess.searchCompanies(coyNameArray, streetNameArray)
            companyResultArray = dictfetchall(companyResult)

            request.session['companyResultArray'] = companyResultArray
            return HttpResponseRedirect('/customer/searchCompanyByLocationResults')
    else:
        form = searchCompanyByLocationForm()

    return render_to_response('customer/searchCompanyByLocation.html', {
        'form': form
    }, context_instance=RequestContext(request))

@csrf_exempt
def searchCompanyByLocationResults(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    return render_to_response('customer/searchCompanyByLocationResults.html', {
    }, context_instance=RequestContext(request))

@csrf_exempt
def searchCompanyByVehicle(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = searchCompanyByVehicleForm(request.POST)
        if form.is_valid():
            vehicleChoice = request.POST['vehicleChoice']
            vehicleAmount = request.POST['vehicleAmount']
            companyByVehicleResultArray = []
            if vehicleChoice == "sedan" or vehicleChoice == "mpv" or vehicleChoice == "luxury":
                params = [vehicleChoice, int(vehicleAmount)]
                companyByVehicleResult = dbaccess.getCompanyByCarCount(params)
                companyByVehicleResultArray = dictfetchall(companyByVehicleResult)
            elif vehicleChoice == "bus" or vehicleChoice == "mini" or vehicleChoice == "coach":
                params = [vehicleChoice, int(vehicleAmount)]
                companyByVehicleResult = dbaccess.getCompanyByBusCount(params)
                companyByVehicleResultArray = dictfetchall(companyByVehicleResult)
            elif int(vehicleChoice) == 1 or int(vehicleChoice) == 3 or int(vehicleChoice) == 5:
                params = [int(vehicleChoice), int(vehicleAmount)]
                companyByVehicleResult = dbaccess.getCompanyByLorryCount(params)
                companyByVehicleResultArray = dictfetchall(companyByVehicleResult)

            request.session['companyByVehicleResultArray'] = companyByVehicleResultArray
            return HttpResponseRedirect('/customer/searchCompanyByVehicleResults')
    else:
        form = searchCompanyByVehicleForm()

    return render_to_response('customer/searchCompanyByVehicle.html', {
        'form': form
    }, context_instance=RequestContext(request))

@csrf_exempt
def searchCompanyByVehicleResults(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    return render_to_response('customer/searchCompanyByVehicleResults.html', {
    }, context_instance=RequestContext(request))

@csrf_exempt
def searchCompanyByVehicleAmt(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = searchCompanyByVehicleAmtForm(request.POST)
        if form.is_valid():
            carChoice = request.POST['carChoice']
            busChoice = request.POST['busChoice']
            lorryChoice = request.POST['lorryChoice']

            if carChoice == "None" and busChoice == "None" and int(lorryChoice) == 10:
                form = searchCompanyByVehicleAmtForm()
            else:
                companyByVehicleAmtResult = dbaccess.getCompanyByVehicleTypes(carChoice, busChoice, lorryChoice)
                companyByVehicleAmtResultArray = dictfetchall(companyByVehicleAmtResult)

                request.session['companyByVehicleAmtResultArray'] = companyByVehicleAmtResultArray
                return HttpResponseRedirect('/customer/searchCompanyByVehicleAmtResults')
    else:
        form = searchCompanyByVehicleAmtForm()

    return render_to_response('customer/searchCompanyByVehicleAmt.html', {
        'form': form
    }, context_instance=RequestContext(request))

@csrf_exempt
def searchCompanyByVehicleAmtResults(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    return render_to_response('customer/searchCompanyByVehicleAmtResults.html', {
    }, context_instance=RequestContext(request))