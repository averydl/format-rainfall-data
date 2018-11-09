
#This script is used to combine whitespace-delimited rainfall data from two text files on multiple dates
#with only date and rainfall depth information in space-delimited format (e.g. "30900   25.4" could represent
#a single line of data, indicating that 25.4 units of rain fell on the absolute date 30900 (August 6, 1984)

#This module contains functions which can be used to process rainfall data files (binary text files, whitespace-delimited)
#which contain entries for date (integer form) and rainfall on each line. The functions in this module include:

#addMissingDates() - This function will add 'null' data tags for all missing dates, such that every date in the range is included in the file1
#combineRainfallFiles() - This function will combine two rainfall files in the specified format, taking the larger of two values on duplicate addMissingDates

#adds missing dates to all files included in a list 'filenames' under directory 'filepath',
#in new files included in the list 'outputnames' under the same directory 'filepath'
def addMissingDates(filepath, filenames):

    list3 = [] #declare empty list to hold start date of each file in 'filenames'

    for i in range(len(filenames)):

        f = open(filenames[i]+".txt") #open each file
        list3.append(int(f.readline().split()[0])) #add entries to list; each entry is the first date in each of the files in 'filenames'
        f.close() #close each file

    for num in range(len(filenames)):
        #set current date to applicable date for current files
        curdate = list3[num]

        #clear values in the date/rainfall lists prior to processing next file
        list1 = []
        list2 = []

        #open current file w/ alias 'f'
        f = open(filepath+filenames[num]+".txt") #open both rainfall files

        #add missing dates and add a 'null' precipitation value
        for line in f:
            date = int(line.split()[0])
            rain = line.split()[1]

            #convert all non-null rainfall values from strings --> floats
            if rain != "null":
                rain = float(rain)

            #add all missing dates to list1, and corresponding 'null' data tags to list2
            while curdate < date:
                list1.append(curdate) #add missing date 'prevdate' to list1
                list2.append("null")    #add 'null' data tag to list2
                curdate = curdate + 1 #increment prevdate

            #add current date and corresponding rainfall value to lists 'list1' and 'list2' respectively
            list1.append(int(date))
            list2.append(rain)
            curdate = date + 1

        #close file
        f.close()

        #write all dates and precipitation values to files
        with open(filepath+filenames[num]+"Output.txt", "w") as op:
            for j in range(len(list1)):
                op.write(str(list1[j]) + "\t" + str(list2[j]) + "\n")

#This function is used to combine whitespace-delimited rainfall data from two text files on multiple dates;
#these two files, file1 and file2, (located under the directory at ultimate filepath 'filepath') must contain
#only date and rainfall depth information in space-delimited format (e.g. "30900 /t 25.4" could represent
#a single line of data, indicating that 25.4 units of rain fell on the absolute date 30900 (August 6, 1984)
def combineRainfallFiles(filepath, file1, file2):

    list1, list2 = [], [] #declare list variables to store tuples with the (date, precipitation) pairs from each file
    cur = 0 #marker for current index in list2

    #add each date/precipitation pair for each station, to two separate lists
    with open(filepath+"\\"+file1+".txt") as f1, open(filepath+"\\"+file2+".txt") as f2: #open both rainfall files

        #add each (date, precip) tuple from 'file1' to 'list1'
        for line in f1:
            curline = line.split()
            date = curline[0]
            rain = curline[1]

            if rain != "null":
                list1.append((date,float(rain)))
            else:
                list1.append((date,rain))

        #add each (date, precip) tuple from 'file2' to 'list2'
        for line in f2:
            curline = line.split()
            date = curline[0]
            rain = curline[1]

            if rain != "null":
                list2.append((date,float(rain)))
            else:
                list2.append((date,rain))

    range1 = range(len(list1)) #range of list1 to be iterated through
    date, precip = [], [] #declare empty list to store the dates and precip. depths

    #iterate through all tuples in list1
    for i in range1:
        date1 = int(list1[i][0]) #store the date at the current tuple in list1
        rain1 = list1[i][1] #store the precipitation at the current tuple in list1

        #write data from all dates in list2 to the file that are missing from list1
        if  cur < len(list2):
            while int(list2[cur][0]) < int(date1):
                date.append(list2[cur][0])
                precip.append(list2[cur][1])
                cur += 1
        if cur < len(list2):
            date2 = int(list2[cur][0]) #store the date at the current tuple in list2
            rain2 = list2[cur][1] #store the precipitation at the current tuple in list2
            cur += 1

        #if duplicate dates are found, add the larger of the two; if one of the data points is 'null' add the other
        if (date2 == date1 and rain1 != rain2):

            #if rain2 is null, add rain1 value to 'precip'
            if (rain2 == "null"):
                date.append(date1)
                precip.append(rain1)

            #if rain1 is null, add rain2 value to 'precip'
            elif (rain1 == "null"):
                date.append(date2)
                precip.append(rain2)

            #neither rain value is null --> append the larger of the two rain values
            else:
                date.append(date1)
                precip.append(max([float(rain1),float(rain2)]))

        else:
            date.append(date1)
            precip.append(rain1)

    #create range object with all remaining indices of list2
    range2 = range(cur, len(list2))

    #add remaining entries from list2 to lists 'date' and 'precip'
    for i in range2:
        date2 = int(list2[i][0])
        rain2 = list2[i][1]
        date.append(date2)
        precip.append(rain2)

    #create new text file for the compiled data to be written to
    with open(filepath+"\\"+"CompiledRainfall.txt", "w") as f:
        for i in range(len(date)):
            f.write(str(date[i]) + "\t" + str(precip[i]) + "\n")

#this function takes arguments an absolute filepath 'filepath' and file name 'file';
#the file must contain space-delimeted text, in which each line contains one 'date'
#value in m/dd/yyyy format, and one rainfall value, separated by a space or tab. This
#function will read the file, and produce a new file in which each 'column' of tab-delimited
#text represents a given month (1-12) and each row represents a day/year of record
#pre: all 'leap-year' dates (i.e. february 29, xxxx) MUST be removed, or the code will break
def arrangeByMonth(filepath, file):

    f = open(filepath + file + ".txt") #open the file

    #store first and last line in file
    first = f.readline().split()[0]
    for line in f:
        pass;
    last = line.split()[0]

    #find starting values for month, day, and year
    startyear = int(first[first.find("/",3)+1:])
    startmonth = int(first[:first.find("/")])
    startday = int(first[first.find("/")+1:first.find("/",3)])

    #find ending values for month, day, and year
    endyear = int(last[last.find("/",3)+1:])
    endmonth = int(last[:last.find("/")])
    endday = int(last[last.find("/")+1:last.find("/",3)])

    numlines = 31*(endyear-startyear+1) #compute number of lines needed to store data in new format
    zerolist = ["x"]*numlines
    datalist = [] #final list of lists; used to store all data in new format specified @ function header

    f.close()

    #preallocate memory for datalist; default to 'null'
    for i in range(12):
        datalist.append(zerolist)

    with open(filepath + file + ".txt") as f:
        for line in f:
            #hold values from each line in 'date' and 'rain' variables
            date = line.split()[0]
            rain = line.split()[1]

            #extract substrings from the 'date' token for current day, month, and year;
            #convert these substrings to integers
            day = int(date[date.find("/")+1:date.find("/",3)]) #extract day on current line
            month = int(date[:date.find("/")]) #extract month on current line
            year = int(date[date.find("/",3)+1:]) #extract year on current line

            row = 31*(year-startyear) #calculate first 'row' (i.e. list index) of the current years
            datalist[month-1][row+day-1] = str(rain) #store the current rainfall value at the correct list & list index

    # with open(filepath + "new.txt", "w") as f:
    #     for i in range(12):
    #         for j in datalist[i]:
    #             f.write(str(j) + "\t")
    #     f.write("\n")
