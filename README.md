# PDS_Project nextbike 
 
Within the same folder as ```setup.py```run ```pip install .``` to install the package. Use flag ```-e``` to install in development mode. In subdirectory ```notebooks``` run ```pip install ..``` to install the package. Import via ```import nextbike```. 

This package implements a command line interface. 
Usage is as follows:
1. When the packages are all sucessfull installed you have to type in PDS_Project_nextbike --transform <source_csv_file> <target_file_path> to tarnsform the csv file to the trip format file. 
The target file option is optional for the command when nothing is tipped in for that parameter the file of the transformed csv will be stored in the output_data folder of the project. The source file option is relativly to the data folder of the project.
2. To train a model type in PDS_Project_nextbike --train <training_data_raw_path> relativly to the data folder of the project. 
3. To predict the test data on the created model type in PDS_Project_nextbike --predict <Test_RAW_format_path> relativly to the data folder in the project. 

