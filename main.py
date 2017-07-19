import argparse
import re
"""
//======================================================================================================
//=  =====  ==    ==  =======  ==    ==  =====  =====  =====  =============       ===        =====  ====
//=   ===   ===  ===   ======  ===  ===   ===   ====    ====  =============  ====  ==  ==========    ===
//=  =   =  ===  ===    =====  ===  ===  =   =  ===  ==  ===  =============  ====  ==  =========  ==  ==
//=  == ==  ===  ===  ==  ===  ===  ===  == ==  ==  ====  ==  =============  ====  ==  ========  ====  =
//=  =====  ===  ===  ===  ==  ===  ===  =====  ==  ====  ==  =============  ====  ==      ====  ====  =
//=  =====  ===  ===  ====  =  ===  ===  =====  ==        ==  =============  ====  ==  ========        =
//=  =====  ===  ===  =====    ===  ===  =====  ==  ====  ==  =============  ====  ==  ========  ====  =
//=  =====  ===  ===  ======   ===  ===  =====  ==  ====  ==  =============  ====  ==  ========  ====  =
//=  =====  ==    ==  =======  ==    ==  =====  ==  ====  ==        =======       ===  ========  ====  =
//======================================================================================================
//  Created by Ian Cleasby on 14/04/2015.
//  Copyright © 2017 Ian Cleasby. All rights reserved.
"""

# Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("file", nargs='?', type=file)
args = parser.parse_args()

def operations(input,prev,final,dfa):
	i=0	
	current = dfa[prev] # current state
	todo = input # remainder of string to do
	done = "" # parts of string completed
	while i < len(input):
		next = current[input[i]]
		current = dfa[next]
		todo = todo[1::] # update to do
		print done,'\t',prev + " -- "+ input[i] + " --> "+ next,'\t',todo # print statement
		done += input[i] # update done
		prev = next
		i+=1
	if prev in final: # is it accepted or not
		print "accepted"
	else:
		print "rejected"

def new_dfa(input, file):
	#Read input
	states = file.readline().split(',')
	alpha = file.readline().split(',')
	start = file.readline().split(',')
	final = file.readline().split(',')
	dfa = {} #DFA structure
	c = 0 # counter
	#Create Generic DFA
	while c < len(states):
		transitions = file.readline().split(',') # read transitions for each state
		i=0 # counter
		state = {}
		while i < len(alpha):
			state[alpha[i].rstrip('\n')] = transitions[i].rstrip('\n') # construct states, add transitions
			i+=1
		dfa[states[c].rstrip('\n')] = state # add states to DFA
		c+=1
	prev = start[0].rstrip('\n') # start state
	final[len(final)-1] = final[len(final)-1].rstrip('\n') # final states
	operations(input,prev,final,dfa) #Perform operations	

def default_dfa(input):
	# Creating default states
	dfa = {
	'q1': {'0': 'q2', '1': 'q3'}, 
	'q2': {'0': 'q1', '1': 'q4'},
	'q3': {'0': 'q5', '1': 'q4'}, 
	'q4': {'0': 'q6', '1': 'q3'},
	'q5': {'0': 'q2', '1': 'q7'}, 
	'q6': {'0': 'q1', '1': 'q8'},
	'q7': {'0': 'q8', '1': 'q8'}, 
	'q8': {'0': 'q7', '1': 'q7'}
	}
	# String OPERATIONS
	prev = 'q1' # start state
	final =['q1','q2','q3','q4','q5','q6','q7'] #final states
	operations(input,prev,final,dfa)
		
# Checking for optional file
if args.file:
	new_dfa(args.input, args.file)
else:
	default_dfa(args.input)
