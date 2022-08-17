import tkinter as tk
import time
import pycosat
from tkinter import filedialog
from itertools import product
from copy import deepcopy

m = 0
n = 0
h = 0
B = []
cnf = []
SL = []
filename = ""

##### Verifier #####

def exist(v, h):
    for i in range(len(v)):
        if (h == v[i][0]):
            return i
    return -1

def findHint(B, m, n):
    l = []
    for i in range(m):
        for j in range (n):
            if (len(l) == 0):
                temp = []
                temp.append(B[i][j])
                temp.append([i,j])
                temp.append([i,j])
                l.append(temp)
            else:
                e = exist(l,B[i][j])
                if (e == -1):
                    temp = []
                    temp.append(B[i][j])
                    temp.append([i,j])
                    temp.append([i,j])
                    l.append(temp)
                else:
                    l[e][2][0] = i
                    l[e][2][1] = j
    return l

def verify(check, B, m, n, r1, c1, r2, c2):
    if ((check[0] == '-' and (r2-r1 >= c2-c1)) or
        (check[0] == '|' and (r2-r1 <= c2-c1)) or
        (check[0] == '+' and (r2-r1 != c2-c1))):
        return False
    
    for i in range(m):
        for j in range(n):
            if (((i < r1 or i > r2 or j < c1 or j > c2) and check == B[i][j]) or
                ((i >= r1 and i <= r2 and j >= c1 and j <= c2) and check != B[i][j])):
                return False
    return True

def verification(B, m, n):
    HL = findHint(B,m,n)

    valid = True
    i = 0
    while (i < len(HL) and valid):
        check = HL[i][0]
        r1 = HL[i][1][0]
        c1 = HL[i][1][1]
        r2 = HL[i][2][0]
        c2 = HL[i][2][1]

        valid = verify(check,B,m,n,r1,c1,r2,c2)

        i = i + 1
    
    if (valid):
        return True
    else:
        return False

def corner(B, m, n):
    for i in range(m-1):
        for j in range(n-1):
            if (B[i][j] != B[i+1][j] and
                B[i][j] != B[i][j+1] and
                B[i][j] != B[i+1][j+1] and
                B[i+1][j] != B[i][j+1] and
                B[i+1][j] != B[i+1][j+1] and
                B[i][j+1] != B[i+1][j+1]):
                return False

    return True

##### SAT Solver #####

def baseMN(r, c, h):
    return 1000 * r + 100 * c + h

def SAThint(B, m, n):
    L2 = []
    h = 0
    for i in range(m):
        for j in range(n):
            if (B[i][j] != '*'):
                h = h + 1
                L2.append(B[i][j])
                temp = []
                temp.append(baseMN(i,j,h))
                cnf.append(temp)
    return L2, h

def rule1 (m, n, h):
    for i in range(m):
        for j in range(n):
            c = []
            for k in range(h):
                c.append(baseMN(i,j,k+1))
            cnf.append(c)
    
    for i in range(m):
        for j in range(n):
            for k in range(h-1):
                for l in range(k+1, h):
                    c = []
                    c.append(-baseMN(i,j,k+1))
                    c.append(-baseMN(i,j,l+1))
                    cnf.append(c)

def rule2 (m, n, h):
    c1 = []
    for i in range(m-1):
        for j in range(n-1):
            for k in range(h):
                c = []
                c.append(baseMN(i,j,k+1))
                c.append(-baseMN(i+1,j,k+1))
                c.append(-baseMN(i,j+1,k+1))
                c.append(-baseMN(i+1,j+1,k+1))
                c1.append(c)

    c2 = []
    for i in range(m-1):
        for j in range(n-1):
            for k in range(h):
                c = []
                c.append(-baseMN(i,j,k+1))
                c.append(baseMN(i+1,j,k+1))
                c.append(-baseMN(i,j+1,k+1))
                c.append(-baseMN(i+1,j+1,k+1))
                c2.append(c)

    c3 = []
    for i in range(m-1):
        for j in range(n-1):
            for k in range(h):
                c = []
                c.append(-baseMN(i,j,k+1))
                c.append(-baseMN(i+1,j,k+1))
                c.append(baseMN(i,j+1,k+1))
                c.append(-baseMN(i+1,j+1,k+1))
                c3.append(c)

    c4 = []
    for i in range(m-1):
        for j in range(n-1):
            for k in range(h):
                c = []
                c.append(-baseMN(i,j,k+1))
                c.append(-baseMN(i+1,j,k+1))
                c.append(-baseMN(i,j+1,k+1))
                c.append(baseMN(i+1,j+1,k+1))
                c4.append(c)
            
    for i in range(len(c1)):
        cnf.append(c1[i])
        cnf.append(c2[i])
        cnf.append(c3[i])
        cnf.append(c4[i])

def rule3 (m,n,h):
    for i in range(m-1):
        for j in range(n-1):
            dnf = []
            for k in range(h):
                c = []
                c1 = []
                c1.append(baseMN(i,j,k+1))
                c1.append(baseMN(i+1,j+1,k+1))
                c2 = []
                c2.append(baseMN(i+1,j,k+1))
                c2.append(baseMN(i,j+1,k+1))
                c.append(c1)
                c.append(c2)
                dnf.append(c)
    
    prod = list(product(*dnf))

    for i in range(len(prod)):
        c = []
        for j in range(len(prod[i])):
            c.append(prod[i][j][0])
            c.append(prod[i][j][1])
        cnf.append(c)

def convertCell(m,n):
    id = []
    for i in range(m):
        for j in range(n):
            for k in range(h):
                id.append([i,j,baseMN(i,j,k+1)])
    return id

def toArray(id,sat,L2):
    sol = []
    for i in range(len(id)):
        for j in range (len(sat)):
            if id[i][2] == sat[j] and sat[j]>0:
                if (sat[j]-(baseMN(id[i][0],id[i][1],0))<h+1):
                    sol.append(sat[j])

    res = []
    for i in range(len(id)):
        for j in range(len(sol)):
            if (id[i][2] == sol[j]):
                res.append([id[i][0],id[i][1],id[i][2]-baseMN(id[i][0],id[i][1],0)])

    C = []
    k = 0
    for i in range(m):
        t = []
        for j in range(n):
            t.append(L2[res[k][2]-1] + str(res[k][2]))
            k = k + 1
        C.append(t)

    return C

def onehint(L2,h,SL,m,n):
    if ((L2[0] == '-' and m>n) or
        (L2[0] == '|' and m<n) or
        (L2[0] == '+' and m==n)):
        C = []
        for i in range(m):
            t = []
            for j in range(n):
                t.append(L2[0] + '1')
            C.append(t)
        SL.append(C)
    

def satsolver():
    global B,m,n,h,cnf,SL

    L2, h = SAThint(B,m,n)
    id = convertCell(m,n)

    if (h==1):
        onehint(L2,h,SL,m,n)
    else:
        rule1(m,n,h)
        rule2(m,n,h)
        rule3(m,n,h)

        while True:
            sat = pycosat.solve(cnf)
            if sat != 'UNSAT':
                C = toArray(id,sat,L2)
                if (verification(C,m,n)):
                    SL.append(C)
            
                ss = []
                for i in range(len(C)):
                    for j in range(len(C[i])):
                        ss.append(-baseMN(i,j,int(C[i][j][1])))
                cnf.append(ss)
            else:
                break

#####Exhaustive#####

def idfier(cells,m,n):
    x = 0
    id = []
    HL = []
    for i in range(m):
        for j in range(n):
            if (cells[i][j] != '*'):
                x = x + 1
                id.append(cells[i][j])
                cells[i][j] = cells[i][j] + str(x)
                HL.append(cells[i][j])
    return cells, id, HL

def possibleRegion(cells,m,n,r,c):
    minr, maxr, minc, maxc = -1,m,-1,n
    list = []

    i = r-1
    while (i > -1):
        if (cells[i][c] != '*'):
            minr = i
            list.append(cells[i][c])
            break
        i = i - 1

    i = r+1
    while (i < m):
        if (cells[i][c] != '*'):
            maxr = i
            list.append(cells[i][c])
            break
        i = i + 1
    
    j = c-1
    while (j > -1):
        if (cells[r][j] != '*'):
            minc = j
            list.append(cells[r][j])
            break
        j = j - 1
    
    j = c+1
    while (j < n):
        if (cells[r][j] != '*'):
            maxc = j
            list.append(cells[r][j])
            break
        j = j + 1

    clim = maxc
    i = r - 1
    while (i > minr):
        j = c + 1
        while (j < clim):
            if (cells[i][j] != '*'):  
                list.append(cells[i][j])
                clim = j
                break
            j = j + 1
        i = i - 1

    clim = minc
    i = r + 1
    while (i < maxr):
        j = c - 1
        while (j > clim):
            if (cells[i][j] != '*'):
                list.append(cells[i][j])
                clim = j
                break
            j = j - 1
        i = i + 1

    clim = minc
    i = r - 1
    while (i > minr):
        j = c - 1
        while (j > clim):
            if (cells[i][j] != '*'):
                list.append(cells[i][j])
                clim = j
                break
            j = j - 1
        i = i - 1

    clim = maxc
    i = r + 1
    while (i < maxr):
        j = c + 1
        while (j < clim):
            if (cells[i][j] != '*'):
                list.append(cells[i][j])
                clim = j
                break
            j = j + 1
        i = i + 1

    return list

def hint(id,m,n):
    hintsArr = []
    hintsLoc = []
    for i in range (m):
        for j in range (n):
            temp = []
            if (id[i][j] == '*'):
                temp.append(i)
                temp.append(j)
                hintsLoc.append(temp)
                hintsArr.append(possibleRegion(B,m,n,i,j))
    return hintsLoc, hintsArr

def combination(arr):
     
    n = len(arr)
    temp2 = []
    indices = [0 for i in range(n)]
 
    while (1):
        temp1 = []
        for i in range(n):
            temp1.append(arr[i][indices[i]])
        temp2.append(temp1)
 
        next = n - 1
        while (next >= 0 and
              (indices[next] + 1 >= len(arr[next]))):
            next-=1
 
        if (next < 0):
            return temp2
 
        indices[next] += 1
 
        for i in range(next + 1, n):
            indices[i] = 0


def exhaustive():
    global B,m,n,h,SL

    B, id, HL = idfier(B,m,n)
    hintLocList, hintList = hint(B,m,n)
    xlist = combination(hintList)

    for i in range(len(xlist)):
        for j in range(len(hintLocList)):
            B[hintLocList[j][0]][hintLocList[j][1]] = xlist[i][j]


        if(verification(B,m,n) and corner(B,m,n)):
            temp = []
            for a in range(len(B)):
                temp2 = []
                for b in range(len(B[a])):
                    temp2.append(B[a][b])
                temp.append(temp2)
            SL.append(temp)


#########################################

def browseFiles():
    global m, n, B, filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    
    with open(filename) as textFile:
      B = [line.split() for line in textFile]

    n = int(B[0].pop(1))
    m = int(B[0].pop(0))
    B.pop(0)

    for widget in instance.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(instance, bg='Yellow')
    canvas.grid(row=0, column=0)

    gridFrame = tk.Frame(canvas)

    framex = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
    framex.grid(row=1, columnspan=n, sticky='news')
    label = tk.Label(master=framex, text=str(m) + 'x' + str(n))
    label.pack()
    for j in range(len(B)):
        for k in range(len(B[j])):
            frame = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=(j+1)+1, column=k, sticky='news')
            label = tk.Label(master=frame, text=B[j][k], width=4, height=2)
            label.pack()

    canvas.create_window((0,0), window=gridFrame, anchor=tk.NW)

    gridFrame.update_idletasks() 
    bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.
    w, l = bbox[2]-bbox[1], bbox[3]-bbox[1]
    dw, dh = int((w/n) * n), int((l/(m+1) * (m+1)))
    canvas.configure(scrollregion=bbox, width=dw, height=dh)

def reset():
  global B, m, n, h, res, SL, filename

  m = 0
  n = 0
  h = 0
  B = []

  with open(filename) as textFile:
      B = [line.split() for line in textFile]

  n = int(B[0].pop(1))
  m = int(B[0].pop(0))
  B.pop(0)

  for widget in instance.winfo_children():
      widget.destroy()

  canvas = tk.Canvas(instance, bg='Yellow')
  canvas.grid(row=0, column=0)

  gridFrame = tk.Frame(canvas)

  framex = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
  framex.grid(row=1, columnspan=n, sticky='news')
  label = tk.Label(master=framex, text=str(m) + 'x' + str(n))
  label.pack()
  for j in range(len(B)):
      for k in range(len(B[j])):
          frame = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
          frame.grid(row=(j+1)+1, column=k, sticky='news')
          label = tk.Label(master=frame, text=B[j][k], width=4, height=2)
          label.pack()

  canvas.create_window((0,0), window=gridFrame, anchor=tk.NW)

  gridFrame.update_idletasks()  
  bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

  # Define the scrollable region as entire canvas with only the desired
  # number of rows and columns displayed.
  w, l = bbox[2]-bbox[1], bbox[3]-bbox[1]
  dw, dh = int((w/n) * n), int((l/(m+1) * (m+1)))
  canvas.configure(scrollregion=bbox, width=dw, height=dh)
  
  res = []
  SL = []

def sollist():
    global B,m,n,h,res,SL,SLi

    start_time = time.time() 
    exhaustive()
    end_time = time.time() - start_time
    print(end_time)

    t = len(SL)

    for widget in rightframe2.winfo_children():
      widget.destroy()

    canvas = tk.Canvas(rightframe2, bg='Yellow')
    canvas.grid(row=0, column=0)

    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(rightframe2, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    gridFrame = tk.Frame(canvas)

    if (t>0):
        for i in range(t):
            framex = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
            framex.grid(row=i*(len(SL[i])+1), columnspan=n, sticky='news')
            label = tk.Label(master=framex, text="Solution "+str(i+1))
            label.pack()
            for j in range(len(SL[i])):
                for k in range(len(SL[i][j])):
                    frame = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=(j+1)+i*(len(SL[i])+1), column=k, sticky='news')
                    label = tk.Label(master=frame, text=SL[i][j][k], width=4, height=2)
                    label.pack()
    else:
        t = t + 1
        framex = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
        framex.grid(row=1, columnspan=n, sticky='news')
        label = tk.Label(master=framex, text="No Solution")
        label.pack()

    canvas.create_window((0,0), window=gridFrame, anchor=tk.NW)

    gridFrame.update_idletasks() 
    bbox = canvas.bbox(tk.ALL)  

    w, l = bbox[2]-bbox[1], bbox[3]-bbox[1]
    dw, dh = int((w/n) * n), int((l/(t*(m+1)) * (m+1)))
    canvas.configure(scrollregion=bbox, width=dw, height=dh)
    
    reset()

def sollist2():
    global B,m,n,h,res,SL,SLi

    start_time = time.time() 
    satsolver()
    end_time = time.time() - start_time
    print(end_time)

    t = len(SL)

    for widget in rightframe2.winfo_children():
      widget.destroy()

    canvas = tk.Canvas(rightframe2, bg='Yellow')
    canvas.grid(row=0, column=0)

    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(rightframe2, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    gridFrame = tk.Frame(canvas)

    if (t>0):
        for i in range(t):
            framex = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
            framex.grid(row=i*(len(SL[i])+1), columnspan=n, sticky='news')
            label = tk.Label(master=framex, text="Solution "+str(i+1))
            label.pack()
            for j in range(len(SL[i])):
                for k in range(len(SL[i][j])):
                    frame = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=(j+1)+i*(len(SL[i])+1), column=k, sticky='news')
                    label = tk.Label(master=frame, text=SL[i][j][k], width=4, height=2)
                    label.pack()
    else:
        t = t + 1
        framex = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
        framex.grid(row=1, columnspan=n, sticky='news')
        label = tk.Label(master=framex, text="No Solution")
        label.pack()

    canvas.create_window((0,0), window=gridFrame, anchor=tk.NW)

    gridFrame.update_idletasks() 
    bbox = canvas.bbox(tk.ALL)  
    
    w, l = bbox[2]-bbox[1], bbox[3]-bbox[1]
    dw, dh = int((w/n) * n), int((l/(t*(m+1)) * (m+1)))
    canvas.configure(scrollregion=bbox, width=dw, height=dh)
    
    reset()

####################################

gui =tk.Tk()

leftframe = tk.Frame(gui,relief=tk.GROOVE, borderwidth=5, width=10, height=100)
leftframe2 = tk.Frame(leftframe)  

button_explore = tk.Button(leftframe2, text = "Browse Files", command = browseFiles)

rightframe = tk.Frame(gui,relief=tk.GROOVE, borderwidth=5, width=10, height=100)
rightframe2 = tk.Frame(rightframe)

button = tk.Button(leftframe2, text="Exhaustive", command=sollist)
button2 = tk.Button(leftframe2, text="SAT Solver", command=sollist2)

instance = tk.Frame(leftframe2)

leftframe.pack(fill=tk.BOTH, side=tk.LEFT, expand=True) 
leftframe2.pack(anchor=tk.CENTER) 
button_explore.grid(column = 1, row = 1, columnspan = 2, sticky='news')
button.grid(column = 1, row = 2)
button2.grid(column = 2, row = 2)

instance.grid(column = 1, row = 3, columnspan = 2)

rightframe.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
rightframe2.pack(anchor=tk.CENTER)    

gui.title('Tatamibari Solver')
gui.geometry('500x150')
gui.mainloop()