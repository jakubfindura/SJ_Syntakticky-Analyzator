import collections
import sys

from grammar import *

# vrati pravu stranu pouziteho prechodu
def getState(stateNumber):
	return pravidla[stateNumber-1]

# vyhodnoti tabulku podla stavu a firstu
def getStateFromTab(state,stateFirst):
	y = table[0].index(stateFirst)
	x = no_terms.index(state)+2

	if( isinstance(table[x][y], list) ):
		return table[x][y]
	else: 
		return [table[x][y]]

def prehladavaj(state,wholeString,index,level):
	string = wholeString[index:]
	
	# prehladavame firsty pre dany stav
	for stateFirst in first[state]:
		
		# ak string zacina firstom, yay
		if( string.startswith(stateFirst) ):
		
			# substitucia abecedy	
			if( stateFirst == abeceda ):
				string = wholeString[:index] + "a" + string[1:]
				stateFirst = "a"
			
			# substitucia cislic
			if( stateFirst == cislice ):
				string = wholeString[:index] + "0" + string[1:]
				stateFirst = "0"
			
			# z tabulky najdem nasledujuci stav (INT)
			nextStatesNum = getStateFromTab(state,stateFirst)

			for nextStateNum in nextStatesNum:
				print(" -- Pouzite pravidlo: [{}]: {}{}".format(nextStateNum,level*" ",pomocne_pravidla[nextStateNum-1]))

				newIndex = index
				ret = [False,index]
				
				# zistim nazov nasledujjuceho stavu
				state = getState(nextStateNum)

				# rozdelenie pravej strany pravidla na jednotlive termy
				termy = state.split(" ")

				# ak je prvy term zaroven firstom, vymazeme ho a osekneme retazec
				if( termy[0] == stateFirst ):
					termy = termy[1:]
					string = string[len(stateFirst):]
					newIndex = index + len(stateFirst)

				# ak nie su ziadne termy, sme na konci prehladavania
				if not termy: 
					return [True,newIndex]

				# prehladavame hlbsie kazdy term
				for term in termy:
					# ak je term neterminal ideme dalej
					if( term in no_terms ):
						# prehladavame dalsi stav so zvysnym retazcom
						x = prehladavaj(term,wholeString,newIndex,level+1)

						# ak prehladavanie uspesne, vratime vyssie orezany retazec
						if( x[0] ):
							string = wholeString[x[1]:]
							newIndex = x[1]
							ret = [True,x[1]]

						# ak sa zasekneme vratime False
						else:
							ret = [False,newIndex]
							break

					# ak je term terminal a retazec nim zacina, vymazeme ho z retazca
					else:
						if( string.startswith(term) ):
							string = string[len(term):]
							newIndex = newIndex + len(term)
						else:
							ret = [False,newIndex]
							break

			return ret
	# ak retazec nezacina ziadnym platnym firstom stavu
	else:
		# ak ma stav epsilonove pravidlo
		if( "EPSILON" in first[state] ):
			# pozrieme ci follom stavu je rovnaky s pokracujucim retazcom
			for stateFollow in follow[state]:
				if( string.startswith(stateFollow) ):
					# vratime zvysny retazec
					return [True,index] # + len(stateFollow) #string #[len(stateFollow):]
		
		# ak pravidlo nema epsilon a retazec je iny ako follow -> slovo nepatri do jazyka
		return [False,index]


if( len(sys.argv) < 2 ):
	print("No file specified.")
	exit()

filename = sys.argv[1]

with open(filename) as f:
    content = f.readlines()

slova = [x.strip() for x in content]

for slovo in slova:
	print("-----------------------------------------------")
	print("Nacitane Slovo ", slovo)
	# print("Length: {}, Ret: {}".format(len(slovo)+1,prehladavaj(startState,slovo+"$",0)))
	ret = prehladavaj(startState,slovo+"$",0,0)
	if(	ret[0] and ret[1] == len(slovo) ):
		print("SUCCESS: Slovo '{}' patri do jazyka".format(slovo))
	else:
		if( ret[1] > -1 ):
			print("ERROR NEAR [{}] > '{}'".format(ret[1],slovo[ret[1]:][:10]))
			print("ERROR: Slovo '{}' nepatri do jazyka".format(slovo))
		else:
			print("ERROR: Slovo '{}' nepatri do jazyka".format(slovo))
