# -*- coding: utf-8 -*-
import numpy as np

class waveSnippe():
    '''
    波形片段
    '''
    def __init__(self,offset, length, parentWaveform):
        '''
        初始化，传入波片段的起始位置、长度、全波数据
        '''
        self.offset = offset #位置
        self.length = length #长度
        self.waveform = parentWaveform[offset:offset+length] #波形数据
        self.parentWaveform = parentWaveform
        self.getLocation = self.getMaxLocation
        self.paramDict = {}
    def getMaxLocation(self):
        '''
        返回最大值的位置
        '''
        if not 'maxLocation' in self.paramDict:
            self.paramDict['maxLocation'] = self.offset + self.waveform.argmax()
        return self.paramDict['maxLocation']
    def getMinLocation(self):
        '''
        返回最小值的位置
        '''
        if not 'minLocation' in self.paramDict:
            self.paramDict['minLocation'] =  self.offset + self.waveform.argmin()
        return self.paramDict['minLocation']
    def getMaxAmplitude(self):
        '''
        返回最大值位置的幅值
        '''
        if not 'maxAmplitude' in self.paramDict:
            self.paramDict['maxAmplitude'] =  self.waveform.max()
        return self.paramDict['maxAmplitude']
    def getMinAmplitude(self):
        '''
        返回最小值位置的幅值
        '''
        if not 'minAmplitude' in self.paramDict:
            self.paramDict['minAmplitude'] =  self.waveform.min()
        return self.paramDict['minAmplitude']
    def getWaveRangeArray(self):
        '''
        返回波形的范围
        '''
        if not 'waveRangeArray' in self.paramDict:
            self.paramDict['waveRangeArray'] = np.zeros((self.parentWaveform.shape[0]))
            self.paramDict['waveRangeArray'][self.offset:self.offset+self.length] +=self.getMaxAmplitude() *0.5
        return self.paramDict['waveRangeArray']
    def getNextSnippe(self,distance,length):
        '''
        返回下一个波，根据当前波的位置
        '''
        newoffset = self.getLocation() + distance - length/2
        return waveSnippe(newoffset,length,self.parentWaveform)