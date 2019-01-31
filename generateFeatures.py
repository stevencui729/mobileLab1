import numpy as np

def normalizeFFT(data):
    top = np.max(data)
    bottom = np.min(data)
    mid = np.average(data)
    normData = (data - mid)
    normData /= top - bottom
    return normData

def generateFeatures(trace):
    channels = ['xAccl', 'yAccl', 'zAccl']
    varDict = {channel:np.var(trace[channel]) for channel in channels}

    relTime = np.subtract(trace['time'], (trace['time'])[0])
    #Useful - https://virtualviking.net/tag/numpy/

    powerSpectrums = {}
    spectrumPeaks = {}
    midPowers = {}
    for channel in channels:
        normData = normalizeFFT(trace[channel])
        spectrum = np.abs(np.fft.fft(normData))
        spectrum *= spectrum
        powerSpectrums[channel] = spectrum
        maxInd = np.argmax(spectrum)#[:int(n/2)+1])
        totalEnergy = np.sum(spectrum)
        #top = spectrum[maxInd] / energy #Might want energy for something later
        spectrumPeaks[channel] = maxInd
        midPoint = len(spectrum)/2
        minCut = int(midPoint-midPoint/2)
        maxCut = int(midPoint+midPoint/2)
        midPowers[channel] = np.sum(spectrum[minCut:maxCut])/totalEnergy
    return varDict, powerSpectrums, midPowers, relTime
