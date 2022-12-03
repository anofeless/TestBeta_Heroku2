# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:21:45 2022

@author: asier
"""
import os
CategoryList=['NotScaled-Advance','NotScaled-Base','Scaled-Advance','Scaled-Base']
WodNames=[ ['AlphaTest-1-PartA','AlphaTest-1-PartB'],
                         ['AlphaTest-2-PartA','AlphaTest-2-PartB'],
                          ]
WodName=WodNames[1][1]
files=[f for f in os.listdir(os.getcwd()) if f.endswith('.png')]
for i,f in enumerate(files):
    os.rename(f,WodName+'_'+CategoryList[i]+'.png')
    print(f)