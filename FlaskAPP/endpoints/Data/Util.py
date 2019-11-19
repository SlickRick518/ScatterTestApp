import xlsxwriter


def circle_fill(page, testinfo, circles):
    # Hard coded rows implement the header while the for loop inserts the data below the header.

    page.write(0, 0, 'Circle #')
    page.write(0, 1, 'Symbol')
    page.write(0, 2, 'Start Time')
    page.write(0, 3, 'End Time')
    page.write(0, 4, 'Total Time')

    page.set_column(6, 11, 20)

    page.write(0, 6, 'TestID')
    page.write(1, 6, testinfo.TestID)
    page.write(0, 7, 'PatientID')
    page.write(1, 7, testinfo.PatientID)
    page.write(0, 8, 'Date')
    page.write(1, 8, testinfo.DateTaken)
    page.write(0, 9, 'DoctorID')
    page.write(1, 9, testinfo.DoctorID)
    page.write(0, 10, 'Test')
    page.write(1, 10, testinfo.TestName)

    row = 1
    for item in circles:  # loop circles 5 columns
        page.write(row, 0, item.CircleID)  # converts to 1..n format
        page.write(row, 1, item.symbol)
        page.write(row, 2, item.begin_circle)
        page.write(row, 3, item.end_circle)
        page.write(row, 4, item.total_time)
        row += 1


def pressure_fill(page, pressure):
    # Header data
    col = 0
    row = 1
    page.write(0, 0, 'Circle #')
    page.write(0, 1, 'Pressure')
    page.write(1 + pressure[-1].CircleID, 1, "Azimuth Angle")
    page.write(2 * (1 + pressure[-1].CircleID), 1, "Pen Altitude")
    page.set_column(1, 1, 20)
      # merge from first point to last longest row (XX) with merge_range('C1:XX')

    # Prints in first column the total number of points (1..n)
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
            page.write(circleid, col, pressure[i].Pressure)
            
        else: # Keep printing as long as circleID hasn't changed
            page.write(circleid, col, pressure[i].Pressure)
            page.write(0, col, counter)
            counter += 1
            col += 1

    col = 2
    circleid = 1
    counter = 1
    for i in range(0, len(pressure)):
        
        if (circleid != pressure[i].CircleID): # Drop down a row if circleID is now
            circleid += 1
            col = 2
            counter = 1
            page.write(circleid + pressure[-1].CircleID + 1, col, pressure[i].Azimuth)
            
        else: # Keep printing as long as circleID hasn't changed
            page.write(circleid + pressure[-1].CircleID + 1, col, pressure[i].Azimuth)
            col += 1

    col = 2
    circleid = 1
    for i in range(0, len(pressure)):
        
        if (circleid != pressure[i].CircleID): # Drop down a row if circleID is now
            circleid += 1
            col = 2
            page.write(circleid + 2 * (pressure[-1].CircleID + 1), col, pressure[i].PenAltitude)
            
        else: # Keep printing as long as circleID hasn't changed
            page.write(circleid + 2 * (pressure[-1].CircleID + 1), col, pressure[i].PenAltitude)
            col += 1
