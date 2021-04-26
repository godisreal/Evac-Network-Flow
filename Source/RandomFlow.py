
# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@126.com


import numpy as np
import random


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
	
	print "GoProb:", goProb, "   StayProb:", stayProb

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
	print "The entire probability list with stayProb integrated:"
	print choiceProb
	result = np.random.multinomial(x, choiceProb)

	return result[:-1]


if __name__ == '__main__':
        #test = np.random.multinomial(10, [0.1, 0.2, 0.3])
        test = ProbQi(10, np.array([0.1, 0.2, 0.3]))
        print test
	
