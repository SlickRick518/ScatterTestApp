import xlsxwriter
from statistics import mean

def formula_fill(page, circleAsArray, pressureList, workbook):
    row = 0
    col = 1
    for i in range(len(circleAsArray)):
        page.write(row, 0, 'Circle #')
        page.write(row, 1, 'Symbol')
        page.write(row, 2, 'Start Time')
        page.write(row, 3, 'End Time')
        page.write(row, 4, 'Total Time')
        page.set_column(2, 8, 20)
        page.write(row, 5, 'Latency')
        page.write(row, 6, 'Average Pressure')
        page.write(row, 7, 'Avg Azimuth Angle')
        page.write(row, 8, 'Average Altitute')

        page.write(row+1, 0, circleAsArray[i].CircleID)
        page.write(row+1, 1, circleAsArray[i].symbol)
        page.write(row+1, 2, circleAsArray[i].begin_circle)
        page.write(row+1, 3, circleAsArray[i].end_circle)
        page.write(row+1, 4, circleAsArray[i].total_time)
        if(i != 0):
            page.write(row+1, 5, circleAsArray[i].begin_circle - circleAsArray[i-1].end_circle)
        else:
            page.write(row+1, 5, "N/A")

        pressureSum = 0.0
        azimuthSum = 0.0
        altitudeSum = 0.0
        
        for j in range(0, len(pressureList[i])):
            pressureSum += pressureList[i][j].Pressure
            azimuthSum += pressureList[i][j].Azimuth
            altitudeSum += pressureList[i][j].PenAltitude
        
        page.write(row+1, 6, (pressureSum / len(pressureList[i])))
        page.write(row+1, 7, (azimuthSum / len(pressureList[i])))
        page.write(row+1, 8, (altitudeSum / len(pressureList[i])))

        pressureChart = workbook.add_chart({'type': 'line'})
        pressureChart.add_series({
            'name':     'Pressure',
            'values':   ['pressure', 1, col, len(pressureList[i])+1, col],
            'line':     {'color': 'red'},
        })

        azimuthChart = workbook.add_chart({'type': 'line'})
        azimuthChart.add_series({
            'name':     'Azimuth Angle',
            'values':   ['pressure', 1, col+1, len(pressureList[i])+1, col+1],
            'line':     {'color': 'red'},
        })

        altitudeChart = workbook.add_chart({'type': 'line'})
        altitudeChart.add_series({
            'name':     'Altitude',
            'values':   ['pressure', 1, col+2, len(pressureList[i])+1, col+2],
            'line':     {'color': 'red'},
        })
        page.insert_chart(row+2, 1, pressureChart)
        page.insert_chart(row+2, 6, azimuthChart)
        page.insert_chart(row+2, 11, altitudeChart)
        row += 18
        col += 4

def circle_fill(page, testinfo, circleAsArray, workbook):

    dateFormat = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    timeFormat = workbook.add_format({'num_format': 'mm:ss'})
    #set up circle info
    page.write(0, 0, 'Circle #')
    page.write(0, 1, 'Symbol')
    page.write(0, 2, 'Start Time')
    page.write(0, 3, 'End Time')
    page.write(0, 4, 'Total Time')
    page.set_column(2, 5, 16)
    page.write(0, 5, 'Latency')

    #set up general test info - why isn't this on another sheet?
    page.write(0, 7, 'TestID')
    page.write(1, 7, testinfo.TestID)
    page.write(0, 8, 'PatientID')
    page.write(1, 8, testinfo.PatientID)
    #date is bad
    page.write(0, 9, 'Date')
    page.write(1, 9, testinfo.DateTaken, dateFormat)
    page.write(0, 10, 'DoctorID')
    page.write(1, 10, testinfo.DoctorID)
    page.write(0, 11, 'Test')
    page.write(1, 11, testinfo.TestName)
    page.write(0, 12, 'Test Length')
    page.write(1, 12, testinfo.TestLength, timeFormat)
    page.set_column(7, 10, 15)
    page.set_column(11, 11, 18)
    page.set_column(12, 12, 15)

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

def col_pressure_fill(page, pressureList, workbook):
    #Circle ID: number of attributes
    col = 0
    row = 1
    pressure_format = workbook.add_format({'bg_color' : '#993333'})
    azimuth_format  = workbook.add_format({'bg_color' : '#0099ff'})
    altitude_format = workbook.add_format({'bg_color' : '#00ffcc'})

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
