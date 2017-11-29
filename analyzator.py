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

def prehladavaj(state,string,original):
		
	# prehladavame firsty pre dany stav
	for stateFirst in first[state]:
		
		# ak string zacina firstom, yay
		if( string.startswith(stateFirst) ):
		
			# substitucia abecedy	
			if( stateFirst == abeceda ):
				string = "a" + string[1:]
				stateFirst = "a"
			
			# substitucia cislic
			if( stateFirst == cislice ):
				string = "0" + string[1:]
				stateFirst = "0"
			
			# z tabulky najdem nasledujuci stav (INT)
			nextStatesNum = getStateFromTab(state,stateFirst)

			for nextStateNum in nextStatesNum:
				newString = string
				ret = False
				
				# zistim nazov nasledujjuceho stavu
				state = getState(nextStateNum)

				# rozdelenie pravej strany pravidla na jednotlive termy
				termy = state.split(" ")

				# ak je prvy term zaroven firstom, vymazeme ho a osekneme retazec
				if( termy[0] == stateFirst ):
					termy = termy[1:]
					newString = string[len(stateFirst):]

				# ak nie su ziadne termy, sme na konci prehladavania
				if not termy: 
					return newString

				# prehladavame hlbsie kazdy term
				for term in termy:
					# ak je term neterminal ideme dalej
					if( term in no_terms ):
						# prehladavame dalsi stav so zvysnym retazcom
						x = prehladavaj(term,newString,original)

						# ak prehladavanie uspesne, vratime vyssie orezany retazec
						if( x ):
							newString = x
							ret = x

						# ak sa zasekneme vratime False
						else:
							ret = False
							break

					# ak je term terminal a retazec nim zacina, vymazeme ho z retazca
					else:
						if( newString.startswith(term) ):
							newString = newString[len(term):]
						else:
							ret = False
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
					return string #[len(stateFollow):]
		
		# ak pravidlo nema epsilon a retazec je iny ako follow -> slovo nepatri do jazyka
		return False


if( len(sys.argv) < 2 ):
	print("No file specified.")
	exit()

filename = sys.argv[1]

with open(filename) as f:
    content = f.readlines()

slova = [x.strip() for x in content]

for slovo in slova:
	if(	prehladavaj(startState,slovo+"$",slovo) == '$' ):
		print("SUCCES: Slovo '{}' patri do jazyka".format(slovo))
	else:
		print("ERROR: Slovo '{}' nepatri do jazyka".format(slovo))
