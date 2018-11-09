#Executes reformatting functions in the ReformatRainfallData module

import ReformatWeatherData
#absolute filepath of input files/output files
filepath = "INSERT FULL FILE PATH HERE"

files = [] #empty list to hold the names of .txt files for input

#add input file names to 'files'
files.append("INSERT FILE1 NAME, WITHOUT FILE TYPE EXTENSION, HERE");
files.append("INSERT FILE2 NAME, WITHOUT FILE TYPE EXTENSION, HERE");

#execute function 'addMissingDates' to add null data values for all dates not
#included in the rainfall data record within the start and end date range
ReformatRainfallData.addMissingDates(filepath, files[0])
ReformatRainfallData.addMissingDates(filepath, files[1])

#sequentially combine files to produce one single file with all rainfall data
#compiled such that the maximum rainfall value observed on each date is present in the "CompiledRainfall" file
ReformatRainfallData.combineRainfallFiles(filepath, files[0], files[1]) #combine revised data files
ReformatRainfallData.arrangeByMonth(filepath, "CompiledRainfall")
