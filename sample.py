# Usage of ChartBuilder module:

from chartbuilder.chartbuilder import Scatter, Pie, Bar, LineGraph, Hist, ChartDataHelper as CDH

import random

a = [[random.gauss(3, 1.2),random.gauss(7, 1.2)] for i in range(400)]
b = [[random.gauss(5, 1.2),random.gauss(3, 1.2)] for i in range(400)]
c = [[random.gauss(7, 1.2),random.gauss(5, 1.2)] for i in range(400)]

p1 = Scatter('Sample 1 - Scatter', 'Value X', 'Value Y')
p1.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p1.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p1.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p1.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p1.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p1.DisableGrid()                           ## Optional, disable grid
data = []
data.append(p1.ScatterData(a, 'Dataset A', 'g'))
data.append(p1.ScatterData(b, 'Dataset B', 'b'))
data.append(p1.ScatterData(c, 'Dataset C', 'r'))
p1.fileToSave(r'result/01_scatter-1.svg')    ## Optional, file to save current chart
p1.Plot(*data)

a = [round(random.gauss(7, 1.1)) for i in range(400)]
b = [round(random.gauss(7, 1.2)) for i in range(400)]
c = [round(random.gauss(7, 1.5)) for i in range(400)]
d = [round(random.gauss(7, 1.7)) for i in range(400)]

ac = CDH.data_count(a)
bc = CDH.data_count(b)
cc = CDH.data_count(c)
dc = CDH.data_count(d)

p2 = Scatter('Sample 2 - Scatter', 'Value', 'Count')
p2.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p2.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p2.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p2.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p2.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p2.DisableGrid()                           ## Optional, disable grid
data = []
data.append(p2.ScatterData(ac, 'Dataset A (sigma 1.1)', 'g', 'o'))
data.append(p2.ScatterData(bc, 'Dataset B (sigma 1.2)', 'r', 'd'))
data.append(p2.ScatterData(cc, 'Dataset C (sigma 1.5)', 'b', 'v'))
data.append(p2.ScatterData(dc, 'Dataset D (sigma 1.7)', 'm', 's'))
p2.fileToSave(r'result/02_scatter-2.svg')    ## Optional, file to save current chart
p2.Plot(*data)

p3 = LineGraph('Sample 3 - Line Diagram', 'Value', 'Count')
p3.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p3.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p3.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p3.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p3.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p3.DisableGrid()                           ## Optional, disable grid
data = []
data.append(p3.LineData(ac, 'Dataset A (sigma 1.1)', 'r'))
data.append(p3.LineData(bc, 'Dataset B (sigma 1.2)', 'g'))
data.append(p3.LineData(cc, 'Dataset C (sigma 1.5)', 'b'))
data.append(p3.LineData(dc, 'Dataset D (sigma 1.7)', 'm'))
p3.fileToSave(r'result/03_linegraph.svg')    ## Optional, file to save current chart
p3.Plot(*data)

a = [random.randint(1,99) for i in range(400)]
b = [random.randint(1,99) for i in range(400)]

ac = CDH.data_count([value for value in a])
bc = CDH.data_count([value for value in b])

p4 = Bar('Sample 4 - Bar Diagram', 'Value', 'Count')
p4.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p4.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p4.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p4.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p4.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p4.DisableGrid()                           ## Optional, disable grid
data = []
data.append(p4.BarData(ac, 'Dataset A', 'b'))
data.append(p4.BarData(bc, 'Dataset B',  'y'))
p4.fileToSave(r'result/04_bar.svg')          ## Optional, file to save current chart
p4.Plot(*data)

p5 = Hist('Sample 5 - Histogram', 'Value', 'Count')
p5.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p5.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p5.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p5.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p5.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p5.DisableGrid()                           ## Optional, disable grid
data = []
data.append(p5.HistData(a, 10, 'Dataset A','r'))
data.append(p5.HistData(b, 10, 'Dataset B', 'g'))
p5.fileToSave(r'result/05_histogram.svg')    ## Optional, file to save current chart
p5.Plot(*data)

#agc = CDH.data_count([value for value in CDH.data_to_ranges(a, 10)])
#bgc = CDH.data_count([value for value in CDH.data_to_ranges(b, 10)])

ag = CDH.data_count([ (value//10)+0.5 for value in a])
bg = CDH.data_count([ (value//10)+0.5 for value in b])

p6 = Bar('Sample 6 - Bar Diagram with values groups in ranges (Another way to build histogram)', 'Value, x10', 'Count')
p6.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p6.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p6.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p6.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p6.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p6.DisableGrid()                           ## Optional, disable grid
data = []
data.append(p6.BarData(ag, 'Dataset A', 'b'))
data.append(p6.BarData(bg, 'Dataset B',  'y'))
p6.fileToSave(r'result/06_bar.svg')          ## Optional, file to save current chart
p6.Plot(*data)

agp = CDH.data_percentage(ag)
bgp = CDH.data_percentage(bg)

item_names = [ f"{i} - {i+9}" for i in range(0,100,10) ]

p7 = Bar('Sample 7 - Bar diagram with custom names on x-axis and % on y-axis (histogram in %)', 'Range', '% of values')
p7.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
p7.setBgColor('whitesmoke', alpha = 0.9)    ## Optional, set chart background color (base colors or CSS4)
#p7.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p7.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
#p7.HideTicks()                             ## Optional, hide x & y ticks & disable grid
#p7.DisableGrid()                           ## Optional, disable grid
p7.setXTicks(item_names)                    ## Optional, set custom values to x-ticks
data = []
data.append(p7.BarData(agp, 'Dataset A', 'c'))
data.append(p7.BarData(bgp, 'Dataset B',  'm'))
p7.fileToSave(r'result/07_bar.svg')          ## Optional, file to save current chart
p7.Plot(*data)

p8 = Pie('Sample 8 - Pie Diagramm')
p8.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
#p8.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p8.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
data = []
data.append(p8.PieData(ag, 'Dataset A'))
data.append(p8.PieData(bg, 'Dataset B (filtered)', minpercent = 8))
p8.fileToSave(r'result/08_pie.svg')          ## Optional, file to save current chart
p8.Plot(*data)

p9 = Pie('Sample 9 - Pie Diagramm with custom names')
p9.setFaceColor('darkgray', alpha = 0.5)    ## Optional, set background color (base colors or CSS4)
#p9.setFontColor('white')                   ## Optional, set title, axis labels, x & y ticks color (base colors or CSS4)
#p9.setBgImage(r'img/bgimage.jpg')           ## Optional, set chart background image
p9.setItemNames(item_names)                 ## Optional, set custom names to pie chart items
data = []
data.append(p9.PieData(ag, 'Dataset A'))
data.append(p9.PieData(bg, 'Dataset B (filtered)', minpercent = 8))
p9.fileToSave(r'result/09_pie.svg')          ## Optional, file to save current chart
p9.Plot(*data)

## Create test dataset for maps:
a = [
    *[[random.gauss(100, 20),random.gauss(100, 20)] for i in range(50)],
    *[[random.gauss(i+random.randint(-10,10), 7), random.gauss(i+random.randint(-10,10), 7)] for i in range(100, 500, 10)], 
    *[[random.gauss(500, 20),random.gauss(500, 20)] for i in range(100)],
    *[(1000, 800)] # point outside the map
]
b = [
    *[[random.gauss(100, 20),random.gauss(400, 20)] for i in range(50)],
    *[[random.gauss(i+random.randint(-10,10), 7), random.gauss(500-i+random.randint(-10,10), 7)] for i in range(100, 300, 10)], 
    *[[random.gauss(300, 20),random.gauss(200, 20)] for i in range(100)],
    *[(1000, 800)] # points outside the map
]

prepared_map, width, height, corner_points = CDH.map_prepare(r'img/square_map.jpg') ## square map image used as background image

ac = CDH.data_crop(a, 0, 0, width, height) ## remove points outside the map from the set
bc = CDH.data_crop(b, 0, 0, width, height) ## remove points outside the map from the set

p10 = Scatter('Square Map')
p10.setSize(width, height)
p10.setBgImage(prepared_map)
p10.HideTicks()
data = []
data.append(p10.ScatterData(corner_points, None, 'k', "+")) ## set corner points
data.append(p10.ScatterData(ac, 'Route A track', 'r'))
data.append(p10.ScatterData(bc, 'Route B track', 'b'))
p10.fileToSave(r'result/10_square_map.svg')
p10.Plot(*data)

prepared_map, width, height, corner_points = CDH.map_prepare(r'img/rectangular_map.jpg') ## rectangular map image used as background image

ac = CDH.data_crop(a, 0, 0, width, height) ## remove points outside the map from the set
bc = CDH.data_crop(b, 0, 0, width, height) ## remove points outside the map from the set

p11 = Scatter('Rectangular Map')
p11.setSize(width, height)
p11.setBgImage(prepared_map)
p11.HideTicks()
data = []
data.append(p10.ScatterData(corner_points, None, 'k', "+")) ## set corner points
data.append(p10.ScatterData(ac, 'Route A track', 'r'))
data.append(p10.ScatterData(bc, 'Route B track', 'b'))
p11.fileToSave(r'result/11_rectangular_map.svg')
p11.Plot(*data)
