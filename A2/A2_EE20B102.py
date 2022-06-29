"""                 	EE2703 Applied Programming Lab 
      				      Assignment 2: Solution
         			      Rachuri Keerthana EE20B102                           """
        		     
                                                                    

from sys import argv, exit
import cmath
import numpy as np

# To improve readability
CIRCUIT = ".circuit"
END = ".end"
Components = { 'R': [], 'C': [], 'L': [], 'V': [], "I": []}
NodesN = {}
ac_present = False

# Classes for circuit components
class RLC:
    def __init__(self, name, n1, n2, val):
        self.name = name
        self.value = np.double(val)
        self.node1 = n1
        self.node2 = n2

class V:
    def __init__(self, name, n1, n2, val, phase=0):
        self.name = name
        self.value = np.double(val)
        self.node1 = n1
        self.node2 = n2
        self.phase = float(phase)

class I:
    def __init__(self, name, n1, n2, val, phase=0):
        self.name = name
        self.value = np.double(val)
        self.node1 = n1
        self.node2 = n2
        self.phase = float(phase)


# We need to make sure that command line arguments are only 2
if len(argv)!=2 :
    exit("Invalid number of arguments!")
else:
    try:
        filename = argv[1]
        # checking if given file is a netlist file
        if (filename[-1*len('.netlist')::1]!='.netlist'):
            print("Wrong file type!")
        else:
            lines = []
            with open (filename, 'r') as f:
                for line in f.readlines():
                    lines.append(line.split('#')[0].split('\n')[0])
                    # Getting frequency, if any
                    if(line[:3] == '.ac'):
                        ac_present = True
                        frequency = float(line.split()[2])
                        # Setting Angular Frequency w
                        w = 2*np.pi*frequency
            try:
                # Finding the location of the identifiers
                index_start = lines.index(CIRCUIT)
                index_end = lines.index(END)
                circuit_block = lines[index_start+1:index_end]
                for line in circuit_block:
                    # Extracting the data from the line
                    linelist = line.split()
                    # Appending new nodes to a list
                    try:
                        if linelist[1] not in NodesN:
                            NodesN[linelist[1]]=len(NodesN)
                        if linelist[2] not in NodesN:
                            NodesN[linelist[2]]=len(NodesN)
                        
                    except IndexError:
                        continue
                    # Resistor
                    if line[0] == 'R':
                        Components['R'].append(RLC(linelist[0], linelist[1], linelist[2], linelist[3]))
                    # 'C'
                    elif line[0] == 'C':
                        Components['C'].append(RLC(linelist[0], linelist[1], linelist[2], linelist[3]))
                    # 'L'
                    elif line[0] == 'L':
                        Components['L'].append(RLC(linelist[0], linelist[1], linelist[2], linelist[3]))
                    # Voltage Source
                    elif line[0] == 'V':
                        if linelist[3] == 'dc': # DC Source
                            Components['V'].append(V(linelist[0], linelist[1], linelist[2], float(linelist[4])))
                        elif linelist[3] == 'ac': # AC Source
                            Components['V'].append(V(linelist[0], linelist[1], linelist[2], float(linelist[4])/2, linelist[5]))
                    # Current source
                    elif line[0] == "I":
                        if linelist[3] == 'dc': # DC Source
                            Components["I"].append(I(linelist[0], linelist[1], linelist[2], float(linelist[4])))
                        elif linelist[3] == 'ac': # AC Source
                            Components["I"].append(I(linelist[0], linelist[1], linelist[2], float(linelist[4])/2, linelist[5]))
                    # Erroneous Component Name
                    else:
                        exit("Wrong Component Given. ABORT!")
                # Make a dictionary of node names and numbers (to reduce the time taken by later parts of the program)
                print(NodesN)
                numNodes = len(NodesN)
                numVS = len(Components['V'])
                # Matrices M and b
                if(ac_present):
                    M = np.zeros((numNodes+numVS, numNodes+numVS), dtype=complex)
                    b = np.zeros((numNodes+numVS,1), dtype=complex)
                else:
                    M = np.zeros((numNodes+numVS, numNodes+numVS))
                    b = np.zeros((numNodes+numVS,1))

                
                # GND Equation
                M[0][0] = 1.0
                # Resistor Equations
                for x in Components['R']:
                    if x.node1 != 'GND':
                        M[NodesN[x.node1]][NodesN[x.node1]] += 1/x.value
                        M[NodesN[x.node1]][NodesN[x.node2]] -= 1/x.value
                    if x.node2 != 'GND':
                        M[NodesN[x.node2]][NodesN[x.node1]] -= 1/x.value
                        M[NodesN[x.node2]][NodesN[x.node2]] += 1/x.value
                # 'C' Equations
                for x in Components['C']:
                    Geff = complex(0, w*x.value)
                    if x.node1 != 'GND':
                        M[NodesN[x.node1]][NodesN[x.node1]] += Geff
                        M[NodesN[x.node1]][NodesN[x.node2]] -= Geff
                    if x.node2 != 'GND':
                        M[NodesN[x.node2]][NodesN[x.node1]] -= Geff
                        M[NodesN[x.node2]][NodesN[x.node2]] += Geff
                # 'L' Equations
                for x in Components['L']:
                    Geff = complex(0, -1.0/(w*x.value))
                    if x.node1 != 'GND':
                        M[NodesN[x.node1]][NodesN[x.node1]] += Geff
                        M[NodesN[x.node1]][NodesN[x.node2]] -= Geff
                    if x.node2 != 'GND':
                        M[NodesN[x.node2]][NodesN[x.node1]] -= Geff
                        M[NodesN[x.node2]][NodesN[x.node2]] += Geff
                # Voltage Source Equations
                for x in range(len(Components['V'])):
                    # Equation accounting for current through the source
                    if Components['V'][x].node1 != 'GND':
                        M[NodesN[Components['V'][x].node1]][numNodes+x] = 1.0
                    if Components['V'][x].node2 != 'GND':
                        M[NodesN[Components['V'][x].node2]][numNodes+x] = -1.0
                    # Auxiliary Equations
                    M[numNodes+x][NodesN[Components['V'][x].node1]] = -1.0
                    M[numNodes+x][NodesN[Components['V'][x].node2]] = +1.0
                    if(ac_present):
                        b[numNodes+x] = complex(Components['V'][x].value, Components['V'][x].phase*np.pi/180)
                    else:
                        b[numNodes+x] = Components['V'][x].value
                    
                # Current Source Equations
                for x in Components["I"]:
                    if x.node1 != 'GND':
                        b[NodesN[x.node1]] = -1*x.value
                    if x.node2 != 'GND':
                        b[NodesN[x.node2]] = x.value

                x = np.linalg.solve(M, b)
   
                circuitCurrents = ["Current (in A) in "+ x.name + ' A' for x in Components['V']]
                
                NodesResult =['Voltage (in V) at node ' + x  for x in NodesN ]
                for j,p in zip(NodesResult+circuitCurrents,x):
                   
                    print(j,p[0])
                
            except ValueError:
                exit("Parameters of the netlist file are incorrect")
    except FileNotFoundError:
        exit("Input file not found")
