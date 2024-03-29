

########################################################################
#-----------------------------------------------------------------------
# Copyright (C) 2020, All rights reserved
#
# Peng Wang
# Email: wp2204@gmail.com
#-----------------------------------------------------------------------
########################################################################
# -*-coding:utf-8-*-


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%% Simulation
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%


import numpy as np
import random
import matplotlib.pyplot as plt
import csv
from readCSV import *
#from RandomFlow import *
import logging
import os, sys


#def ProbQi(x, goProb, wayProb, capa):
        # x: number of people in room x
        # goProb: affected by fire status and alarm info, etc.  
        # wayProb: affected by guidance info and familiar ways, etc.
        # 					  [way1Prob, way2Prob, ... waynProb]
        # capa: passageway capacity [way1Capa, way2Capa, ... waynCapa]


def ProbQi(x, wayProb):

        # x: number of people in room x
        # wayProb: affected by guidance info and familiar ways, etc.
        # 					  [way1Prob, way2Prob, ... waynProb]

        goProb = np.sum(wayProb)
        stayProb = 1-goProb

        print("GoProb:", goProb, "   StayProb:", stayProb)

        #### Input parameter check
        #if len(capa)!=len(wayProb):
        #	print('\nError on input parameter in function ProbQi\n')
        #end

        #if goProb<0 or x<0:
        #	print('\nError on input parameter in function ProbQi\n')
        #end

        if np.sum(wayProb)>1 or x<0:
                print('\nError on input parameter in function ProbQi\n')

        choiceProb = np.append(wayProb, stayProb)
        #choiceProb = wayProb + [stayProb]
        #choicProb = wayProb.append(stayProb)

        #print wayProb
        print("The entire probability list with stayProb integrated:")
        print(choiceProb)
        result = np.random.multinomial(x, choiceProb)

        return result[:-1]


#if __name__ == '__main__':
        #test = np.random.multinomial(10, [0.1, 0.2, 0.3])
#        test = ProbQi(10, np.array([0.1, 0.2, 0.3]))
#        print test


logging.basicConfig(filename='log_examp.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


def simulation(filename, T, DEBUG=True):

        # Time Horizon: T

        # Read in csv file
        #fileName


        #Building Structure
        # 11 Rooms: E1 E2 H1 H2 H3 O1 O2 O3 L1 L2 L3
        # 14 Paths: H1->E1; H3->E2; 
        #           O1->H1; O2->H2; O3->H3;
        #           L1->H1; L2->H2; L3->H3;
        #           H2->H1; H2->H3;
        #           O2->O1; O2->O3;
        #           L2->L1; L2->L3

        #       H1  H3  O1  O2  O3  L1  L2` L3  H2  H2  O2  O2  L2  L2
        #       ->  ->  ->  ->  ->  ->  ->  ->  ->  ->  ->  ->  ->  ->
        #       E1  E2  H1  H2  H3  H1  H2  H3  H1  H3  O1  O3  L1  L3


        print('\nBuilding Models\n')

        dataIS, isStart, isEnd = getData(filename, "&inti")
        dataCapa, capaStart, capaEnd = getData(filename, "&capa")
        dataBLD, bldStart, bldEnd = getData(filename, "&bld")
        dataWP, wpStart, wpEnd = getData(filename, "&prob")

        print(dataIS)
        print(dataCapa)
        print(dataBLD)
        print(dataWP)

        Num_X=np.size(dataIS)
        Num_Y=np.size(dataCapa[0])

        Num_R=Num_X-1
        Num_P=Num_Y-1

        matrixIS=readFloatArray(dataIS, Num_R, 1)
        matrixCapa=readFloatArray(dataCapa, 1, Num_P)
        matrixBLD=readFloatArray(dataBLD, Num_R, Num_P)
        matrixWP=readFloatArray(dataWP, Num_R, Num_P)


        # %%%% Input parameter check
        if np.shape(matrixWP)!= np.shape(matrixBLD):
            print('\nError on input parameter\n')

        if matrixCapa.shape[1]!=Num_P:
            print('\nError with matrixCapa\n')
            
        if matrixIS.shape[0]!=Num_R:
            print('\nError with matrixIS\n')

        #print matrixBLD
        #print matrixWP
        #print matrixCapa
        #print matrixIS

        f = open("out.txt", "w+") 
        f.write("matrixBLD\n"+str(matrixBLD)+"\n") #??????
        f.write("matrixCapa\n"+str(matrixCapa)+"\n")
        f.write("matrixWP\n"+str(matrixWP)+"\n")
        f.write("matrixIS\n"+str(matrixIS)+"\n")
        f.write("Number of Locations and Passages:"+str(Num_R)+","+str(Num_P))
        #f.wrtie("dimension of matrixCapa"+str(np.shape(matrixCapa)))
        #f.wrtie("maximal element in matrixCapa"+str(np.max(matrixCapa)))

        if DEBUG and sys.version_info[0] == 2:
            print >> f, "matrixIS\n", matrixIS, "\n" 
            print >> f, "Number of Locations and Passages:", Num_R, Num_P
            print >> f, "dimension of matrixCapa", np.shape(matrixCapa)
            print >> f, "maximal element in matrixCapa", np.max(matrixCapa)
        #f.close()

        temp=arr1D_2D(dataIS)
        NameLocation =np.transpose(temp)[0,1:]
        #NameLocation=['E1', 'E2', 'H1', 'H2', 'H3', 'O1', 'O2', 'O3', 'L1', 'L2', 'L3']
        #BLD_Index_Room=cellstr(NameLocation);   %Colomn Vector

        temp=arr1D_2D(dataCapa)
        NamePassage =temp[0,1:]
        #NamePassage=['H1->E1', 'H3->E2', 'O1->H1', 'O2->H2', 'O3->H3', 'L1->H1', 'L2->H2', 'L3->H3', 'H2->H1', 'H2->H3', 'O2->O1', 'O2->O3', 'L2->L1']
        #BLD_Index_Path=cellstr(NamePassage);   %Colomn Vector

        print(NameLocation)
        print(NamePassage)

        print("Some Testing Cases:")
        print(matrixBLD[:,0])
        print(matrixBLD[:,1])
        print(matrixBLD[1,:])

        if DEBUG and sys.version_info[0] == 2: 
            raw_input('Please check input data here!')
        if DEBUG and sys.version_info[0] == 3:
            input('Please check input data here!')

        X = np.zeros((Num_R, T))
        Mov = np.zeros((Num_P, T))
        MovSource = np.zeros((Num_P, T))

        print(X[:,1])
        print(X[1,:])
        #matrixIS.shape = 1,-1

        X[:,0] = matrixIS.reshape((1,-1))

        numOfPeople = np.sum(X[:,0])
        print("Number of Evacuees:", numOfPeople)

        print("Initial State of the Model")
        print(X[:,0])
        print(matrixIS)

        MovComp = np.zeros((Num_R, Num_P))
        MovCompDir = np.zeros((Num_R, Num_P))
        MovCompInter = np.zeros((Num_R, Num_P))


        if DEBUG and sys.version_info[0] == 2: 
            print >> f, "Initial State: X[:,0]\n", X[:,0], "\n"
            print >> f, "Initial MovComp: \n", MovComp, "\n"
            print >> f, "Initial MovCompDir: \n", MovCompDir, "\n"
            print >> f, "Initial MovCompInter: \n", MovCompInter, "\n"

        if DEBUG and sys.version_info[0] == 2: 
            raw_input('Please check data in initialization phase here!')
        if DEBUG and sys.version_info[0] == 3: 
            input('Please check data in initialization phase here!')

        print("Computing in iteration starts here!\n")
        f.write("Computing in iteration starts here!\n")

        for t in range(0, T-1):
            
            print("\n&&&&&&&&&&&&&&&&&&&")
            print("Time Step:", t)
            print("&&&&&&&&&&&&&&&&&&&\n")
            
            f.write("\n&&&&&&&&&&&&&&&&&&&&")
            f.write("Time Step:"+str(t))
            f.write("&&&&&&&&&&&&&&&&&&&&&&\n")
            
            MovCompInter = np.zeros((Num_R, Num_P))

            for i in range(0, Num_R):
                print("Location in calculation:", NameLocation[i])
                print(matrixWP[i,:])
                #matWayProb = matrixWP[i,:]
                MovComp[i,:] = ProbQi(X[i,t], matrixWP[i,:])
                print("Movement array genertated:", MovComp[i,:])

            MovCompDir = -MovComp*matrixBLD
            
            #print "Movement array: MovComp"   
            #print MovComp
            #print "Movement in direction: MovCompDir"
            #print MovCompDir
            
            for j in range(0, Num_P):
                temp = 0
                tempIndex = 0
                maxIndex = 0
                for i in range(0, Num_R):
                    if MovComp[i,j]>temp:
                        temp = MovComp[i,j]
                        tempIndex = i
                maxIndex = np.argmax(MovComp[:,j])
            
                if maxIndex == tempIndex:
                    print("OK. Well Done!")
                    f.write("OK. Well Done!")
                else:
                    print("Something wrong here!")
                    f.write("Something wrong here!")
            
                Mov[j,t] = min(temp, matrixCapa[0,j])
                if MovCompDir[tempIndex, j]<0:
                    Mov[j,t] = -Mov[j,t]
                MovSource[j,t] = int(tempIndex)
                MovCompInter[int(maxIndex),j] = np.fabs(Mov[j,t])


            for i in range(0, Num_R):
                for j in range(0, Num_P):
                    #if not np.allclose(X[i,t], 0): 
                    if np.fabs(X[i,t])>1E-2:
                    #    continue
                    #else:
                        matrixWP[i,j] = (matrixWP[i,j]*X[i,t]+MovCompInter[i,j])/X[i,t]/2.0

            # Check the math model: 
            # Is the flow generated correct?  We need to check it
            for i in range(0, Num_R):
                if np.sum(MovComp[i,:])>X[i,t]:
                    print("!!!!!!!!!!!!!!!")
                    print("error found here! About MovComp")
                    print("Flow generated exceeds the source!")
                if np.sum(MovCompInter[i,:])>X[i,t]:
                    print("!!!!!!!!!!!!!!!")
                    print("error found here! About MovCompInter")
                    print("Flow generated exceeds the source!")
                if np.sum(matrixWP[i,:])>1:
                    print("!!!!!!!!!!!!!!!")
                    print("error found here! About matrixWP")
                    print("Flow generated exceeds the source!")
                    print("error location:", i)


            print("Movement Information:")
            print("MovComp: \n", MovComp)
            print("MovCompDir: \n", MovCompDir)
            print("MovCompInter: \n", MovCompInter)
            print("Mov[:,t]: \n", Mov[:,t])
            
            f.write("MovComp: \n"+str(MovComp)+"\n")
            f.write("MovCompDir: \n"+str(MovCompDir)+"\n")
            f.write("MovCompInter: \n"+str(MovCompInter)+"\n")
            f.write("Mov[:,t]: \n"+str(Mov[:,t])+"\n")
            f.write("MovSource[:,t]: \n"+str(MovSource[:,t])+"\n")


            #for j in range(0, Num_P-1):
            #    if Mov[j,t] > matrixCapa[0,j]:
            #	Mov[j,t] = matrixCapa[0,j]
            #	print "print here to show that this line is being run"
            #	print "********************"
            #	print "********************"


            #X = X + BLD*Mov
            X[:,t+1] = X[:,t] + np.dot(matrixBLD, Mov[:,t])

            #print "Movement integrated from the above matrix", Mov[:,t]
            print("Number of evacuees X[t]:", X[:,t])
            print("Number of evacuees X[t+1]:", X[:,t+1])
            print("number of evacuees", np.sum(X[:,t]))

            f.write("Number of evacuees X[t]:"+str(X[:,t])+"\n")
            f.write("Number of evacuees X[t+1]:"+str(X[:,t+1])+"\n")
            f.write("number of evacuees"+str(np.sum(X[:,t]))+"\n")

        f.close()

        print('E1:', X[0,:])
        print('E2:', X[1,:])
        np.save("E1.npy",X[0,:])
        np.save("E2.npy",X[1,:])
        #plt.figure('data')
        plt.plot(X[0,:])
        plt.plot(X[1,:])
        plt.show()


if __name__ == '__main__':
    #test = np.random.multinomial(10, [0.1, 0.2, 0.7])
    T=16  # Simulation Timo Horizon [0, T]
    simulation('example2021.csv', T)

