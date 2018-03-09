# coding: utf-8
# 
# 
# author: zjs
# 
# 

import numpy as np
from PIL import Image
import math


#
#目前只能进行基2图像进行傅里叶正反变换 没有进行补零
#
#打开图像，取到图像N*N数组 N必须是2的整数幂
#

im = Image.open("lena.jpg") 
im_arr = np.array(im)
height,width= im_arr.shape
tmp = np.zeros((height,width),dtype=np.complex)
dft_arr = np.zeros((height,width),dtype=np.uint8)
idft_arr = np.zeros((height,width),dtype=np.uint8)

tp = np.zeros((height),dtype=np.complex)
fft_arr = np.zeros((height,width),dtype=np.complex)
ifft_arr = np.zeros((height,width),dtype=np.complex)

#*********************************************************
#DFT
#使用numpy矩阵乘法即可
#*********************************************************


def DFT_matrix(N):
	i,j = np.meshgrid(np.arange(N),np.arange(N))
	omega = np.exp(-2j*np.pi/N)
	W = np.power(omega,i*j)
	return W

def DFT(Arr, N):
	dft_of_arr = np.dot(np.dot(DFT_matrix(N),Arr),DFT_matrix(N))
	return dft_of_arr


dft_arr= (abs(DFT(im_arr,height))).astype(np.uint8)
im_dft = Image.fromarray(dft_arr)
im_dft.save("dft.jpg")
im_dft.show()

#*********************************************************
#IDFT 同DFT 逆向即可
#*********************************************************

def IDFT_matrix(N):
	i, j = np.meshgrid(np.arange(N), np.arange(N))
	omega = np.exp( 2j * np.pi/ N )
	W = np.power( omega, i * j ) / N
	return W

def IDFT(Arr, N):
	idft_of_arr = IDFT_matrix(N).dot(DFT(im_arr,height)).dot(IDFT_matrix(N))
	return idft_of_arr


idft_arr = (abs(IDFT(dft_arr,width))).astype(np.uint8)
im_idft = Image.fromarray(idft_arr)
im_idft.save("idft.jpg")
im_idft.show()

#*********************************************************
#FFT
#*********************************************************

def FFT(Arr,N):
	Arr=np.array(Arr)
	p=0
	angle=0.0
	temp = np.zeros((N),dtype=np.complex)
	r=int(math.log2(N))
	for j in range(1<<r):#对数据进行排序
		p=0;
		for i in range(r):
			if(j&(1<<i)):
				p+=(1<<(r-i-1))
		temp[j]=Arr[p];
	W=np.power(np.exp(-2j*np.pi/N),np.arange(N/2))
	Arr2 = np.zeros((N),dtype=np.complex)
	for k in range(r):#蝶形算法 r：阶数 j：分区2^K i：每个区块顺序数
		for j in range((1<<k)):
			p=j*(1<<(r-k-1))
			for i in range(j,N,1<<(k+1)):
				Arr2[i] = temp[i] + temp[i+(1<<k)]* W[p]
				Arr2[i+(1<<k)] = temp[i] - temp[i+(1<<k)] * W[p]
		temp,Arr2 = Arr2,temp
	return temp

#TestCase
# a=[[1, 2, 3, 4, 4, 5, 0, 0],
#    [3, 2, 1, 2, 4, 5, 0, 0],
#    [2, 3, 4, 5, 1, 2, 0, 0],
#    [2, 4, 5, 2, 1, 2, 0, 0],
#    [3, 2, 4, 8, 9, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0]]

# temx = np.array((a),np.complex)
# print(DFT(temx, 8))
# temx = np.zeros((height,height),dtype=np.complex)
# temx = (im_arr).astype(np.complex)
# out = np.zeros((height,height),dtype=np.complex)
# for i in range(height):
# 	tp = temx[i]
# 	temx[i] = FFT(tp, height)
# for i in range(height):
# 	out[:,i] = FFT(temx[:,i],height)

# print(out)
# print(DFT(im_arr,height))
# idft_arr = (abs(out)).astype(np.uint8)
# im_idft = Image.fromarray(idft_arr)
# im_idft.show()
# print((abs(fft_arr)).astype(np.uint8))
# 

for i in range(width):
	tmp[i,:] = FFT(im_arr[i,:],height)
for i in range(height):
	fft_arr[:,i] = FFT(tmp[:,i],width)
im_fft = Image.fromarray((abs(fft_arr)).astype(np.uint8))
im_fft.save("fft.jpg")
im_fft.show()

#*********************************************************
#IFFT 同FFT使用蝶形算法
#*********************************************************

def IFFT(Arr,N):
	Arr=np.array(Arr)
	p=0
	angle=0.0
	temp = np.zeros((N),dtype=np.complex)
	r=int(math.log2(N))
	for j in range(1<<r):
		p=0;
		for i in range(r):
			if(j&(1<<i)):
				p+=(1<<(r-i-1))
		temp[j]=Arr[p];
	W=np.power(np.exp(2j*np.pi/N),np.arange(N/2))
	Arr2 = np.zeros((N),dtype=np.complex)
	for k in range(r):
		for j in range((1<<k)):
			p=j*(1<<(r-k-1))
			for i in range(j,N,1<<(k+1)):
				Arr2[i] = temp[i] + temp[i+(1<<k)]* W[p]
				Arr2[i+(1<<k)] = temp[i] - temp[i+(1<<k)] * W[p]
		temp,Arr2 = Arr2,temp
	return temp


for i in range(width):
	tmp[i,:] = IFFT(fft_arr[i,:],height)
for i in range(height):
	ifft_arr[:,i] = IFFT(tmp[:,i],width)
im_ifft = Image.fromarray((abs(ifft_arr/(height*height))).astype(np.uint8))
im_ifft.save("ifft.jpg")
im_ifft.show()