import numpy as np
import random as rd

cp = capacity = 600 #600(100)背包容量
tw = thingsweight = np.array([30, 42, 8, 43, 37, 46, 17, 16, 8, 49, 10, 9, 10, 24, 27, 51, 24, 31, 51, 38, 7, 17, 25, 42, 8, 44, 37, 50, 38, 13, 20, 41, 40, 19, 34, 6, 48, 11, 37, 44, 30, 38, 16, 8, 20, 14, 40, 4, 13, 16])
tv = thingsvalue = np.array([97, 81, 50, 68, 78, 70, 33, 61, 54, 101, 85, 13, 73, 92, 60, 44, 15, 12, 52, 22, 52, 58, 53, 3, 16, 64, 32, 19, 37, 68, 62, 56, 8, 54, 39, 10, 32, 20, 87, 101, 62, 72, 1, 38, 73, 48, 74, 11, 55, 59])
# tw = thingsweight = np.array([30, 42, 8, 43, 37, 46, 17, 16, 8, 49])		#物品重量    		
# tv = thingsvalue = np.array([97, 81, 50, 68, 78, 70, 33, 61, 54, 101])		#物品价值
rs = reset = [1]				#归一化矩阵
bw = bagWeight = []				#包包现在的重量
av = adaptValue = []			#包包现在的价值
p = 100							#种群规模
mat = 0.9						#交配概率
var = 0.1						#变异概率
x = 1000							#迭代次数

#生成个体
b = []
c = []
for a in range(p):
	for  i in range(len(tw)):
		b.append(rd.randint(0,1))
	c.append(b)
	b = []
ch = choise = np.array(c)		#choise基因码集合(0，1，0，0，0，1，1.....)
bw = ch.dot(tw.T)
av = ch.dot(tv.T)
rsl = np.array(rs*len(av))
allv = av.dot(rsl.T) 	#所有价值(适应度)总和
print(ch,bw)

def RWS(sp1):			#轮盘赌算法
	m = 0					
	r = rd.random()
	for i in range(len(sp1)):
		m = m + sp1[i]
		if(r <= m):
			return i
			break

#随机竞争选择
def compitition(av1,bw1,allv1,ch0):		#传入现在价值，现在重量，所有价值(数)
	sp = av1/allv1  		#select probabily选择概率
	ch1 = ch0 				#种群基因副本
	C1 = RWS(sp)
	C2 = RWS(sp)
	for c in range(len(bw1)):
		while(bw1[c] > 600):
			k = rd.randint(0,49)
			chn = ch[c]
			if(chn[k] == 1):
				chn[k] = 0
				ch[c] = chn
			bw1[c] = ch[c].dot(tw.T)
	acb = av/bw1 			#价值comper重量(平均价值)
	a = -(bw1 - 600)		#重量和容量的差距		
	b = acb*a				#适应度差距	
	for i in range(p):
		if(b[C1] > b[C2]):ch1[i] = ch0[C2] 
		else: ch1[i] = ch0[C1]
	ch0 = ch1				#新群体
	return ch0 					#返还选择后的种群

#交配
def mating(chk):
	ch0 = chk						#种族副本
	ch1 = []
	for i in range(len(chk)):
		r = rd.random()
		if r <= mat:
			ch1.append(chk[i])
			np.delete(ch0,chk[i])
	for a in range(len(ch1)-1):
		ch2 = ch1[a]
		ch3 = ch1[a+1]
		e1 = rd.randint(0,25)				#两个交配位
		e2 = rd.randint(25,49)
		ch2[e1],ch3[e1] = ch3[e1],ch2[e1]	#交配1
		ch2[e2],ch3[e2] = ch3[e2],ch2[e2]	#交配2
		np.append(ch0,ch2)
		np.append(ch0,ch3)
	chk = np.array(ch0)
	return chk

#变异
def variation(chm): 
	for i in range(len(chm)):
		ch4 = chm[i]
		r = rd.random()
		if(r <= var):
			e = rd.randint(0,len(tw)-1)
			if(ch4[e] == 0):ch4[e] = 1
			else:ch4[e] = 0 
			chm[i] = ch4
	return chm

for i in range(x):			#进行x次数的代
	ch = compitition(av,bw,allv,ch)
	ch = mating(ch)
	ch = variation(ch)
	bw = ch.dot(tw.T)
	av = ch.dot(tv.T)
	rsl = np.array(rs*len(av))
	allv = av.dot(rsl.T) 	#所有价值(适应度)总和

print(ch,"\n",bw,"\n",av)
for i in range(len(ch)):
	if bw[i] > 600:
		bw[i] = 0
		av[i] = 0
print(max(av))


