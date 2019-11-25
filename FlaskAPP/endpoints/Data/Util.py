import xlsxwriter
def circle_fill(page, testinfo, circles, workbook):

    #set up circle info
    page.write(0, 0, 'Circle #')
    page.write(0, 1, 'Symbol')
    page.write(0, 2, 'Start Time')
    page.write(0, 3, 'End Time')
    page.write(0, 4, 'Total Time')
    page.set_column(4, 4, 20)
    page.write(0, 5, 'Latency')

    #set up general test info - why isn't this on another sheet?
    page.write(0, 7, 'TestID')
    page.write(1, 7, testinfo.TestID)
    page.write(0, 8, 'PatientID')
    page.write(1, 8, testinfo.PatientID)
    #date is bad
    page.write(0, 9, 'Date')
    page.write(1, 9, testinfo.DateTaken)
    page.write(0, 10, 'DoctorID')
    page.write(1, 10, testinfo.DoctorID)
    page.write(0, 11, 'Test')
    page.write(1, 11, testinfo.TestName)
    page.set_column(7, 12, 20)

    #grab all the circle objects and throw them in an array for ez access
    circleAsArray = []
    for row in circles:
        circleAsArray.append(row)

    for i in range(len(circleAsArray)):
        page.write(i+1, 0, circleAsArray[i].CircleID)
        page.write(i+1, 1, circleAsArray[i].symbol)
        page.write(i+1, 2, circleAsArray[i].begin_circle)
        page.write(i+1, 3, circleAsArray[i].end_circle)
        page.write(i+1, 4, circleAsArray[i].total_time)
        if(i != 0):
            page.write(i+1, 5, circleAsArray[i].begin_circle - circleAsArray[i-1].end_circle)
        else:
            page.write(i+1, 5, "N/A")

def col_pressure_fill(page, pressure, workbook):
    #Circle ID: number of attributes
    col = 0
    row = 1
    pressureList = []
    pressure_format = workbook.add_format({'bg_color' : '#993333'})
    azimuth_format  = workbook.add_format({'bg_color' : '#0099ff'})
    altitude_format = workbook.add_format({'bg_color' : '#00ffcc'})

    for i in range(pressure[-1].CircleID):
        #fun python filtering - i+1 because the circle values start at 1
        filtered = list(x for x in pressure if x.CircleID == i+1)
        pressureList.append(filtered)

    for i in range(len(pressureList)):
        page.write(0, col, 'Circle ID: ' + str(i+1))
        page.write(0, col+1, 'Pressure (' + str(len(pressureList[i])) + ' values)')
        page.set_column(0, col+1, 20)
        page.write(0, col+2, 'Azimuth Angle')
        page.set_column(0, col+2, 20)
        page.write(0, col+3, 'Altitude Angle')
        page.set_column(0, col+3, 20)
        for j in range(0, len(pressureList[i])):
            page.write(row, col+1, pressureList[i][j].Pressure, pressure_format)
            page.write(row, col+2, pressureList[i][j].Azimuth, azimuth_format)
            page.write(row, col+3, pressureList[i][j].PenAltitude, altitude_format)
            row = row + 1
        col = col + 4
        row = 1


# use this if you want to have the info displayed in rows
def row_pressure_fill(page, pressure, workbook):
    page.write(0, 0, 'Circle #')
    page.write(0, 1, 'Pressure')
    page.write(1 + pressure[-1].CircleID, 1, "Azimuth Angle")
    page.write(2 * (1 + pressure[-1].CircleID), 1, "Pen Altitude")
    page.set_column(1, 1, 20)
    #setup formatting - example colors
    pressure_format = workbook.add_format({'bg_color' : '#993333'})
    azimuth_format  = workbook.add_format({'bg_color' : '#0099ff'})
    altitude_format = workbook.add_format({'bg_color' : '#00ffcc'})
    # Prints in first column the total number of points (1..n)
    # an index of -1 accesses the last element in the array
    col = 0
    row = 1
    for i in range(pressure[-1].CircleID):
        page.write(row, 0, i + 1)
        page.write(row + pressure[-1].CircleID + 1, 0, i+1)
        page.write(row + 2 * (pressure[-1].CircleID + 1), 0, i+1)
        row += 1

    col = 2
    circleid = 1
    counter = 1
    for i in range(0, len(pressure)):
        
        if (circleid != pressure[i].CircleID): # Drop down a row if circleID is now
            circleid += 1
            col = 2
            counter = 1
            page.write(circleid, col, pressure[i].Pressure, pressure_format)
            
        else: # Keep printing as long as circleID hasn't changed
            page.write(circleid, col, pressure[i].Pressure, pressure_format)
            page.write(0, col, counter)
            counter += 1
            col += 1

    col = 2
    circleid = 1
    for i in range(0, len(pressure)):
        
        if (circleid != pressure[i].CircleID): # Drop down a row if circleID is now
            circleid += 1
            col = 2
            page.write(circleid + pressure[-1].CircleID + 1, col, pressure[i].Azimuth, azimuth_format)
            
        else: # Keep printing as long as circleID hasn't changed
            page.write(circleid + pressure[-1].CircleID + 1, col, pressure[i].Azimuth, azimuth_format)
            col += 1

    col = 2
    circleid = 1
    for i in range(0, len(pressure)):
        
        if (circleid != pressure[i].CircleID): # Drop down a row if circleID is now
            circleid += 1
            col = 2
            page.write(circleid + 2 * (pressure[-1].CircleID + 1), col, pressure[i].PenAltitude, altitude_format)
            
        else: # Keep printing as long as circleID hasn't changed
            page.write(circleid + 2 * (pressure[-1].CircleID + 1), col, pressure[i].PenAltitude, altitude_format)
            col += 1
