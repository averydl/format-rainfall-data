## Overview

The ___ReformatRainfallData_.py__ module is intended to be used to, reformat basic weather data for use in data analysis. All files
used with the functions in this module must be in a very specific format, the specifics of which are detailed in 
the section "Step 4 - Modifying Data File Format" below. 

## Functions

Before using the functions in the _ReformatRainfallData_ module, it helps to be aware of what functions are included
in the module, what purpose they serve, and what their constraints are. The module contains three functions, each of 
which has multiple arguments (i.e. function inputs, all of which are strings) which allow the user to generate new files. Each of 
these three functions, _addMissingDates()_, _combineRainfallFiles()_, and _arrangeByMonth()_, and their arguments/constraints, 
are detailed below. It is also important to note that generally, these functions should be executed in the order in which they
are listed, using the output from each prior function call as the input to the next function call. An example workflow is illustrated schematically below, where parentheses "()" represent files, braces "[]" represent functions, and arrows "-->" represent input/output of the functions)

### Example 
Take two files, (File1.txt) and (File2.txt), adding missing dates to each to create new files (File1DatesAdded.txt) and (File2DatesAdded.txt), 
combine these resulting files to create a more comprehensive record file (File3.txt), and finally, process (File3.txt) to output a file
(FileResult.txt) which has the correct row/column format for simple processing and visualization using Excel. This workflow is illustrated
below:



(File1.txt) --> [_addMissingDates()_] --> (File1DatesAdded.txt) --
						                |
							        |
						                 \
						                  -----> [combineRainfallFiles] ------> (File3.txt) ------> [_arrangeByMonth()_] -----> (FileResult.txt)
						       	         /	 
							        |
(File2.txt) --> [_addMissingDates()_] --> (File2DatesAdded.txt) --|



_addMissingDates(filepath, filename, outputname)_ - 

The _addMissingDates()_ function is intended to add dates to a non-comprehensive set of weather data (i.e. data which has periods of time 
without any record) such that all dates without data will be included, but will have a value "null" instead of data. This is basically
a helper function that formats the data such that it can be used with the other functions in the __ReformatRainfallData.py__ module without error.
As an example, if the data file had data points on the dates 01/01/1990 and 01/03/1990, this function would add the date 01/02/1990 with a "null" 
placeholder, indicating that this date does not contain any data.

This function takes as arguments a String "filepath" where the target file is located, a String "filename" which is the name of the 
file to be processed, and the String "outputname" which is the name of the new file being created by the function. 


combineRainfallFiles(filepath, file1, file2, outputname) - 

The _combineRainfallFiles()_ function does what the name implies; it combines two separate rainfall data files into one rainfall 
data file. This function will fill in gaps in the record. In the case that only one of the two data files has data point for a given date, 
the resulting file "outputname" will include the value from the file which does contain data on that date. In the event that both files have a 
non "null" value for a specific date, this function will include the greater of the two values in the new "outputname" file. It is important to 
note that the _addMissingDates()_ function must be used prior to using the _combineRainfallFiles()_ if the original file has gaps in date. That is 
to say, any file that is used with the _combineRainfallFiles()_ function must either:

	Case 1- Be comprehensive, without any gaps in date; additionally, the dates without data must have a filler value "null" instead of numerical data
	Case 2- Be the output of a call to the _addMissingDates()_ function, which will ensure that the output file is in the format specified in case 1

_arrangeByMonth(filepath, file, outputname)_

The _arrangeByMonth()_ function will take a text file "file" located under the absolute directory "filepath", and output a re-formatted 
file "outputname" in the same directory. In the reformatted file, each row will represent the day of the month in a given calendar year, 
and each column represents month. This is easier to demonstrate visually. For example, the first few lines of the file may look like:

"
Months:	Jan	Feb	Mar	Apr	May	Jun	Jul	Aug	Sep	Oct	Nov	Dec	

1-1957	null	null	null	null	null	null	0.0	0.12	0.0	0.04	0.0	0.0	
2-1957	null	null	null	null	null	null	0.0	0.0	0.0	0.0	0.12	0.43	
3-1957	null	null	null	null	null	null	0.0	0.0	0.02	0.0	0.0	0.08	
4-1957	null	null	null	null	null	null	0.0	0.08	0.0	0.0	0.0	0.0	
"

These data tokens represent all precipitation values on the first four days of each month, in the year 1957. This format makes it easy to find
average or max/min weather events on a given month or year in Excel, which is the ultimate intent of this module. Again, the input file 
for the _arrangeByMonth()_ function must be in the format specified


### Installation

Any system with python installed will be able to utilize these scripts. Simply clone the directory from the command line as:
__git clone https://github.com/averydl/format-rainfall-data.git__

### Usage

Currently this software does not have a GUI, and is purely operated via the command line. Refer to the example above for a typical workflow.

### General Information

#### Setting the Working Directory

Once the shell interface is open, the next step is to set the working directory to the location of the
executable file. For example, the python '.py' file might be located on the "I:" drive, with the absolute 
file path "I:\ExampleDirectory\WeatherData"

In the example file path above, begin by entering "I:" in the command window and hitting enter. This will set the
current root directory to the I: drive. Then, enter the command "cd" (short for "current directory") 
followed by the file path of the folder which contains the executable python script. Note that the character "U"
followed by a slash "\" will result in an error, so all "\" marks preceding "U" should be duplicated. In the example above, 
this would result in a command that looks like "cd \\ExampleDirectory\WeatherData" which will set the current working directory
to the I:\ExampleDirectory\WeatherData directory in the I drive. Remember, you must first enter "I:" prior to executing this command

#### Required binary file format

Prior to executing the python scripts, the data files MUST be in the correct format. For these files, this format will consist
of whitespace-delimited text (i.e. text separated by tabs or spaces) which has two values per row; date (in mm/dd/yyyy or mm-dd-yyyy format) followed
by the rainfall (or other daily weather reading). For example, one line in a rain data file may contain the values "01/25/2017	0.21"
This would represent a data point on January 25, 2017, indicating a rainfall depth of 0.21 units. Each line must contain ONLY these two 
types of data, and the MUST be separated by a tab. It is fairly easy to format data like this in Excel and copy it over to a .txt file. Also, make
sure that there aren't any blank lines in the .txt file, either at the beginning or end. This will result in an error, as the script is not designed
to check for this scenario during execution. An example of test contained in such a file with two data points, one of which is "null", is indicated below.

#### Generalizing/Modifying Workflow

This next step is critical for applying the script to the specific data of interest, making it generic rather than specific to a single project. 
For most intents and purposes, the _ReformatRainfallData_ module may be left alone; the only
reason to modify this file would be to either add functionality (i.e. add functions to perform other tasks) or to modify the functionality
of the existing functions (for example, a user might desire to change the combineRainfallFiles() function to use the LESSER of two values
on dates which have values for both input files, rather than the GREATER of the two values. However, in all other cases, this file should
not be modified. 

Rather, the "ExecuteReformat.py" script can either be modified, or new scripts written which utilize the functions located in the _ReformatRainfallData_
module. Generally speaking, the most common changes that will need to be made to the pre-written ExecuteReformat.py script would be:

	-Changing "filepath" variable: If the directory in which text files, this script, and the _ReformatRainfallData_ module changes (very likely), then
	this variable will need to be changed to reflect the current working directory, or the script will not work.

	-Changing file names: It is almost certain that the data files used by this script will have a wide variety of names, although they should all be ".txt"
	files. Therefore, the file names (e.g. the current script contains a line of code:

	 "addDates(filepath, "WeatherData.txt", "OutputForExample.txt)" 

	This simply adds missing dates with the "null" placeholder value, to the file "WeatherData.txt", and puts the results in a new file "OutputForExample.txt"). 
	If the user wanted to do this for, say, a file named "Example.txt" and wanted the new file to be called "ExampleOutput.txt", this line of code would
	need to be changed to be:

	"addDates(filepath, "Example.txt", "ExampleOutput.txt")"

	-Repeating commands for multiple files, or combining multiple files. Some users may want to combine multiple files in serial, for example. These users
	could use the same general format in the existing script, but they would need to apply the combineRainfallFiles() function to the resulting output. For 
	the visual example shown in the "Functions" section of this README file, in which two files are processed and combined, the commands required to be in 
	the script would look something like this:

	"
	filepath = "I:\\ExampleDirectory\WeatherDataFile\"
	addDates(filepath, "File1.txt", "File1DatesAdded.txt")
	addDates(filepath, "File2.txt", "File2DatesAdded.txt")
	combineRainfallFiles(filepath, "File1DatesAdded.txt", "File2DatesAdded.txt", "File3.txt")
	arrangeByMonth(filepath, "File3.txt", "FileResult.txt")
	"

### Executing the Script
Once your command window open and you have navigated to the correct working directory, transferred all binary data files to the working directory, 
and modified your scripts as necessary, you are ready to execute the program.

"py ExecuteReformat.py"

If everything has been done correctly, this script should generate one or more new files in the current working directory.

_Written by_ __Derek Avery__
