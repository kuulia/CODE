import numpy as np

def mynorm(a, b):
    return np.linalg.norm(a-b)

################# input file ############################################
max_na = 48

name_of_file = input('What is the name of the file? ie. 100Mol \n')
filename= name_of_file + ".xyz"
atoms=[]
xyz=open(filename, errors='ignore')
na_array = []
cm_arr = []
flat_list = []

count = 0
while True:
    line=xyz.readline()                    #first line = number of atoms (na)
    if not line: break
    l = line.split()
    number_of_atoms = l[0]
    na_array.append(number_of_atoms)
    na = int(line)
    if len(l) == 1:
        sl = xyz.readline()                   #second line = numeration of molecules and atomization energy --> energyline
        nc = []
        R=[]
        for i in range(na):
            al = xyz.readline()                          #atom lines with element type and coordinates
            #print(al)
            atom, x, y, z = al.split()
            atoms.append(atom)
            #print('atom:', atom)
            R.append([float(x),float(y),float(z)])    #nuclear charge of atoms: H->1, C->6, N->7, O->8, S->16, F->9
            if atom == "H":
                nc.append(1)
            elif atom == "C":
                nc.append(6)
            elif atom == "N":
                nc.append(7)
            elif atom == "O":
                nc.append(8)
            elif atom == 'F':
                nc.append(9)
            elif atom == 'S':
                nc.append(16)
            elif atom == 'Cl':
                nc.append(17)
            elif atom == 'Br':
                nc.append(35)
               
        cm = [[0]*na for i in range(na)]           # Calculate Coulomb matrix 
        #print "The first matrix i ", cm
        i=0
        while i<na:
            j=0
            while j<na:
                if i == j:
                    cm[i][j]=0.5*nc[i]**2.4
                    #print "Diagonal elememt is", cm[i][j]
                else:
                    a=np.array(R[i])
                    b=np.array(R[j])
                    #print "this is array R_i", a
                    #print "this is array R_j", b
                    cm[i][j]=nc[i]*nc[j]/np.linalg.norm(a-b)
            #print "Nondiagonal element is", cm[i][j]
                j=j+1
            i=i+1

        s0 = np.round(cm, decimals=3)       # round numbers to 3 digits after comma

        #file = open(fn, "w")                                    

        #print(cm)

        a = np.zeros(shape=(max_na, max_na))  #OE
        ##a = np.zeros(shape=(15,15))
        #print(a)
        b = a.copy()
        b[:s0.shape[0],:s0.shape[1]] += s0    # pad matrix with zero elements to size 23x23

	## order by row norm
        indexlist_row = np.argsort(np.linalg.norm(b, axis=1), axis=-1)[::-1]
        ## apply to Coulomb matrix
        cm_ordered_by_row_norm = b[indexlist_row]


        ## order by column norm --> transpose of ordered by row norm
        cm_ordered_by_column_norm = cm_ordered_by_row_norm.transpose()
        ## order this matrix by row norm
        indexlist_row2 = np.argsort(np.linalg.norm(cm_ordered_by_column_norm, axis=1))[::-1]
        ## apply to cm ordered by row norm
        final_matrix = cm_ordered_by_column_norm[indexlist_row2]

        flat_matrix = [item for sublist in final_matrix for item in sublist]
        
        flat_list.append(flat_matrix)
	
        count=count+1

        #cm = np.array(b, dtype=float)
        #cm_arr.append(cm)
	#count = count + 1


xyz.close()
#cm_arr=np.array(cm_arr, dtype=float)
print("count is", count)


fileoutname = name_of_file + '_cm.txt'


#flat_list = [item for sublist in coulomblist_array for item in sublist]
np.savetxt(fileoutname, flat_list, fmt="%s")  ############################## output file #########################
