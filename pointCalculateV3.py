# -*- coding: utf-8 -*-
import math
import numpy as np
import os
from collections import OrderedDict
from waveDetect import *
#----------------------------------------------------------------------------------------------------------------------------

SearchStart = 1000  #搜索起点
SearchRange = 1000 #搜索宽度

distance = 1000 #两次波之间的间距
waveWidth = 300

h = 25.0 #工件厚度
f = 1e8 # 采样频率

#----------------------------------------------------------------------------------------------------------------------------
try:
    from scipy import fftpack
except:
    print('scipy is not found!')
from matplotlib import cm
def settings():
    '''
    参数设置字典
    colorMap：特征热力图所使用的颜色表
    flip: 对图像矩阵进行旋转、转置等操作可以设置为:np.fliplr 左右旋转  np.flipud 上下旋转 np.transpose 转置 np.rot90 逆时针旋转90度等操作
    '''
    settings = {}
    settings['colorMap'] = cm.gray
    settings['flip'] = np.fliplr
    return settings
def calculatePoint((x,y),waveform,argsDict):
    '''
    点计算函数
    x,y,z:点的坐标

    waveform:波形数据
    returnDict:返回的字典，字典的键值为名称，
    如果键值中含有_label则会在波形图中显示该点的位置.
    如果键值中含有_map则会生成该特征的热力图.
    如果键值中含有_waveform则会在波形图中显示该曲线.  
    如果键值中含有_background则会在作为背景显示.  
	
    argsDict为参数字典，目前支持以下参数：
        batchMode： 表示是否批处理生成模式，可以利用这个变量来分别是否是单次选取波形还是批量生成数据
        stepSizeX:x轴每步走的步距
        stepSizeY:y轴每步走的步距
        workDir:工作目录
        dataMode:文件模式，有txt/h5/saz三种模式
        label: 当前波形的标签，类型string,txt模式下是文件名，其他模式下含有坐标
		
    '''
    returnDict = OrderedDict()
    returnDict['label_map'] = argsDict['label'] #标签，用于显示文件名和坐标
    
    surface = waveSnippe(SearchStart,SearchRange,waveform)  #根据提供的搜索位置和长度创建一个波形片段
    returnDict['surface_label'] = surface.getMaxLocation() #获取最大值位置
    if not argsDict['batchMode']:
        returnDict['surface_waveform'] = surface.getWaveRangeArray()
    bottom1 = surface.getNextSnippe(distance,waveWidth)
    #根据提供的距离和波形宽度查找下一个波形片段
    returnDict['bottom1_label'] = bottom1.getMaxLocation() #获取最大值位置
    returnDict['bottom1_map'] = bottom1.getMaxAmplitude() #获取最大值幅值
    
    bottom2 = bottom1.getNextSnippe(distance,waveWidth) #根据提供的距离和波形宽度查找下一个波形片段
    returnDict['bottom2_label'] = bottom2.getMaxLocation() #获取最大值位置
    returnDict['bottom2_map'] = bottom2.getMaxAmplitude() #获取最大值幅值
    #计算速度V21
    t21 =  bottom2.getMaxLocation()- bottom1.getMaxLocation() #一次底波和二次底波时间差
    v21 = 2.0*(1.0*h/1000)*f/t21
    returnDict['v21_map'] = v21
    #计算衰减比例
    de = bottom1.getMaxAmplitude()/ bottom2.getMaxAmplitude()
    #计算速度V10
    t21 =  bottom1.getMaxLocation()- surface.getMaxLocation() #一次底波和二次底波时间差
    v21 = 2.0*(1.0*h/1000)*f/t21
    returnDict['v10_map'] = v21
    
    #计算噪声
    noise = surface.getNextSnippe(-100,50)
    returnDict['noise_map'] = noise.getMaxAmplitude() #获取噪声的幅值
    returnDict['noise_label'] = noise.getMaxLocation()
    
    
    
    
    
    
    return returnDict