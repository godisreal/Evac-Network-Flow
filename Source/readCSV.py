
# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@126.com

import numpy as np
import csv

def readCSV(fileName):
    
    # Read csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)  # 返回的是迭代类型
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    print(strData)
    dataTemp=np.array(strData)

    #print(strData[1:,1:])
    csvFile.close()	

    [I, J] = np.shape(dataTemp)
    print("The size of tha above matrix:", [I, J])

    matrix = np.zeros((I, J))

    for i in range(1,I):
        for j in range(1,J):
            matrix[i,j]=float(dataTemp[i,j])

    print(matrix[1:, 1:])
    return matrix[1:, 1:]



def readCSV_base(fileName, flag='debug'):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    if flag=='debug':
        print('\n')
        print('#=======================#')
        print(fileName)
        
    dataNP = np.array(strData)
    #print (dataNP)

    if flag=='debug':
        print ('np.shape(dataNP)', np.shape(dataNP))
        print ('\n')

    #print(strData[1:,1:])
    csvFile.close()
    return dataNP


def getData(fileName, strNote):
    dataFeatures = readCSV_base(fileName)

    Num_Data = len(dataFeatures)

    for i in range(Num_Data):
        if dataFeatures[i]:
            if dataFeatures[i][0]==strNote:
                IPedStart=i
                
    for j in range(IPedStart, Num_Data):
        if dataFeatures[j]==[]:
            IPedEnd=j
            break
        if j==Num_Data-1:
            IPedEnd=Num_Data

    dataOK = dataFeatures[IPedStart : IPedEnd]
    return dataOK, IPedStart, IPedEnd

    #data_result = np.array(dataOK)
    #return data_result[1:, 1:]


def arr1D_2D(data, debug=True):
    #data is in type of 1D array, but it is actually a 2D data format.  
    
    NRow = len(data)
    NColomn = len(data[1])
    matrix = np.zeros((NRow, NColomn), dtype='|S20')
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = data[i][j]
    if debug:
        print('Data in 2D array:\n', matrix)
        
    return matrix
    
    
def readFloatArray(tableFeatures, NRow, NColomn):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    print(tableFeatures, '\n')
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(tableFeatures[i+1][j+1])
    print('Data in Table:', '\n', matrix)
    return matrix


if __name__ == '__main__':
    #test1 = readCSV("example2021.csv")
    #print(test1)
    #test = readCSV_base("example2021.csv")
    #print(test)

    print('\n Test of Reading Data. \n')

    filename="example2021.csv"
    
    dataIS, isStart, isEnd = getData(filename, "&inti")
    dataCapa, capaStart, capaEnd = getData(filename, "&capa")
    dataBLD, bldStart, bldEnd = getData(filename, "&bld")
    dataWP, wpStart, wpEnd = getData(filename, "&prob")

    print(dataIS)
    print(dataCapa)
    print(dataBLD)
    print(dataWP)

    np.shape(dataIS)
    dataIS_2D=OneDim2TwoDim(dataIS)
    print(dataIS_2D)
    np.shape(dataIS_2D)

