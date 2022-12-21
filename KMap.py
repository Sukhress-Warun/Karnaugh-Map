def grper(rect,consider_unavail):
	grp=[]
	for i in range(rect[0][0],rect[3][0]+1):
		for j in range(rect[0][1],rect[3][1]+1):
			if(mat[i%row][j%col]!=0 and (avail[i%row][j%col] or consider_unavail)):
				grp.append((i%row,j%col))
				continue
			else:
				return None
	for (i,j) in grp:
		avail[i][j]=False
	return grp

def fourposs(x,y,dim):
	if(row<dim[0] or col<dim[1]):
		return None
	topleft=[x-dim[0]+1,y-dim[1]+1]
	bottomleft=[x,y-dim[1]+1]
	topright=[x-dim[0]+1,y]
	bottomright=[x,y]
	rect=[topleft,topright,bottomleft,bottomright]
	transform_x=[0,1,0,-1]
	transform_y=[1,-1,1,-1]
	for i in range(4):
		grp=grper(rect,False)
		if(grp!=None):
			return grp
		for j in rect:
			j[0]+=transform_x[i]*(dim[0]-1)
			j[1]+=transform_y[i]*(dim[1]-1)
	for i in range(4):
		grp=grper(rect,True)
		if(grp!=None):
			return grp
		for j in rect:
			j[0]+=transform_x[i]*(dim[0]-1)
			j[1]+=transform_y[i]*(dim[1]-1)
	return None

def grp_detect(x,y):
	for i in (16,8,4,2,1):
		for j in DIMDICT[i]:
			grp=fourposs(x,y,j)
			if(grp!=None):
				return grp

#neccessary values
ROWDICT={2:["0","1"] , 3:["0","1"], 4:["00","01","11","10"]}
COLDICT={2:["0","1"] , 3:["00","01","11","10"] , 4:["00","01","11","10"]}
DIMDICT={16:[(4,4)] , 8:[(2,4),(4,2)] , 4:[(1,4),(2,2),(4,1)] , 2:[(1,2),(2,1)] , 1:[(1,1)] }

n=int(input("Enter how many variables: "))

#check for error
if (n<2 or n>4):
	print("Error")
	quit()

#initialization
variables=input("Enter names of variables seperated by space\n").split()
mat=[]
row,col=2 if(n<4)else 4 , 4 if(n>2)else 2
rowref=ROWDICT[row]
colref=COLDICT[col]
for i in range(row):
	mat.append(list(map(int,input().split())))
avail=[[True for i in range(col)]for j in range(row)]

groups=[]
for i in range(row):
	for j in range(col):
		if(mat[i][j]==1 and avail[i][j]):
			grp=grp_detect(i,j)
			if(grp!=None):
				groups.append(grp)

filter_grp=[True for i in range(len(groups))]
for i in range(len(groups)):
	flgs=0
	for j in range(len(groups[i])):
		for k in range(len(groups)):
			if i!=k and groups[i][j] in groups[k]:
				flgs+=1
				break
	if flgs==len(groups[i]):
		filter_grp[i]=False
groups=list(map(lambda x:x[1],list(filter(lambda x:filter_grp[x[0]],enumerate(groups)))))

bingroups=[]
for i in groups:
	rset,cset=zip(*i)
	rset=set(rset)
	cset=set(cset)
	grp=[list(map(lambda x:rowref[x],rset)),list(map(lambda x:colref[x],cset))]
	bingroups.append(grp)

expression=[]
for i in bingroups:
	variable_l=list(zip(*i[0]))
	variable_l+=list(zip(*i[1]))
	term=""
	for j in range(len(variable_l)):
		zc=variable_l[j].count('0')
		oc=variable_l[j].count('1')
		if(zc==oc):
			continue
		elif(oc>zc):
			term+=variables[j]
		else:
			term+=variables[j]+"\'"
	expression.append(term)

print(*expression,sep="+")