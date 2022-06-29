"""
        		     	EE2703 Applied Programming Lab 
      				      Assignment 1: Solution
         			      Rachuri Keerthana EE20B102
         				    
INPUT: .netlist file
OUTPUT: Identifies errors in SPICE program code, and displays the tokens in reverse order
"""

from sys import argv, exit

"""
It's a good practice to check if the user has given required and only the required inputs
Otherwise, show them the expected usage.
"""
if len(argv) != 2:
    print('\nUsage: %s <inputfile>' % argv[0])
    exit()

if(argv[1][-8::1]!='.netlist'):
    print("Input file is not a netlist file")
    exit()
 
filename = argv[1]
try:
    with open(filename) as f:
        lines = f.readlines()
        """
        It's recommended to use constant variables than hard-coding them everywhere.
        For example, if you decide to change the command from '.circuit' to '.start' later,
            you only need to change the constant
        """
        CIRCUIT = '.circuit'
        END = '.end'
        start = -1
        end = -2


        """
        The location of each line is stored, and the endline character is removed from each 'line'.
        Following that, the 'line' is split into two parts, the comment and the program code. The 
        comment is ignored and only the program code is saved in the variable 'line'. The tab spaces
        are converted to spaces and then the lines are stripped out of their leading and trailing 
        spaces and then compared to find the beginning and the ending of the code.
        """

        for line in lines:

            location = lines.index(line)
            line = line.replace('\n','')
            line = line.split('#')[0]
            line = line.replace('\t',' ');	
            line=line.strip()
            lines[location] = line

            if line[:len(CIRCUIT)] == CIRCUIT:
                start = lines.index(line)
            elif line[:len(END)] == END:
                end = lines.index(line)	

            

            
        
        if start >= end:
            print("Circuit Block Invalid")
            exit(0)


        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Token = []
        
        for line in lines[start+1:end]:
            
            """
            Each line's location is stored.
            A 'linelist' of words/tokens is formed from 'line,' i.e. tokens separated by space are saved in 'linelist.' 
            This iteration is ignored if the linelist is empty.
            """
            location = lines.index(line)
            linelist = line.split(" ")
            linelist = [elem for elem in linelist if elem != ""]

            if linelist == []:
                continue
                
            """
            The 'linelist' is then tested for resistor, capacitor, inductor dependent and independent voltage and currect sources before being appended to the 'Token'.
            The relationships depend on only two nodes - so four tokens - in the case of resistor, inductor, and capacitor independent voltage and current sources.
            There are 6 tokens in the case of voltage dependent sources and 5 tokens in the case of current dependent sources. 
            The element type is indicated by the first letter of the element label. The node labels must be alphanumeric as well.
            """
            if linelist[0][0] == 'R' or 'L' or 'C' or 'V' or 'I' :	
                if len(linelist) != 4:
                    print("Incorrect Number of Parameters: Line ",location)
                    exit(0)
                if linelist[1].isalnum() != True or linelist[2].isalnum() != True :
                    print("Incorrect Node Designation - only alphanumeric variables: Line ",location)
                    exit(0)
                
            elif linelist[0][0] ==  'E' or 'G':
                if len(linelist) != 6:
                    print("Incorrect Number of Parameters: Line ",location)
                    exit(0)
                if linelist[1].isalnum() != True or linelist[2].isalnum() != True or linelist[3].isalnum() != True or linelist[4].isalnum() != True:
                    print("Incorrect Node Designation - only alphanumeric variables: Line ",location)
                    exit(0) 
            

            elif linelist[0][0] ==  'H' or 'F':
                if len(linelist) != 5:
                    print("Incorrect Number of Parameters: Line ",location);
                    exit(0)
                if linelist[1].isalnum() != True or linelist[2].isalnum() != True:
                    print("Incorrect Node Designation - only alphanumeric variables: Line ",location)
                    exit(0)
                if linelist[3][0] != 'V':
                    print("Incorrect Voltage Label: Line ",location)
                    exit(0)
            
            Token.append(linelist);
            
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        """
        Finally the tokens are then printed in the reverse fashion		
        """	
        length = len(Token)
        for i in range(length-1,-1,-1):
            line = " "
            for j in range(len(Token[i])-1,-1,-1):
                print(Token[i][j]," ",end="")
            print()
            
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

except:
	print("File not found")
	exit(0)

