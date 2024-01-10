# Simple chartbuilder based on matplotlib library
# Homepage: https://github.com/greentracery/ChartBuilder
# Requirements:
# - matplotlib
# - Pillow (PIL)
# Usage:
# p = Scatter('Main Title', 'X Axis Label', 'Y Axis Label')
# [optional] p.setSize(width, height, dpi)
# [optional] p.fileToSave('filename') # png, svg, pdf
# p.Plot(
#       p.ScatterData( dataset1 = list of tuple(s) [(x, y), ], 'Legend Label 1', 'Color 1' = ['g' | 'r' | 'b' etc ]),
#       p.ScatterData( dataset2 = list of tuple(s) [(x, y), ], 'Legend Label 2', 'Color 2' = ['g' | 'r' | 'b' etc ]),
#       p.ScatterData( dataset3 = list of tuple(s) [(x, y), ], 'Legend Label 3', 'Color 3' = ['g' | 'r' | 'b' etc ]),
#       ...
# )
# p = Pie('Main Title')
# [optional] p.setSize(width, height, dpi) # image height = count(datasets) * height
# [optional] p.fileToSave('filename') # png, svg, pdf
# p.Plot(
#       p.PieData( dataset1 = list of tuple(s) [(value , name), ], 'Pie Title 1', min_value), #items smaller than min_value will be ignored
#       p.PieData( dataset2 = list of tuple(s) [(value , name), ], 'Pie Title 2', min_value),
#       p.PieData( dataset3 = list of tuple(s) [(value , name), ], 'Pie Title 3', min_value),
#       ...
# )

from typing import List, Union
from abc import ABC, abstractmethod
import random
import os
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from PIL import Image, ImageOps

class ChartBuilder(ABC): #Prohibits the creation of the class object directly
    """ 
        Abstract class for ChartBuilder, prototype of all avalaible chart types
        
        property: title: title (or supertitle) for diagramm (all diagramms in one image)
        property: xlabel: name of x-axis
        property: ylabel: name of y-axis
        property: filename: name of image file to save diagramm
        property: imgbackground: name of image file used as background image
        property: facecolor: font color (base or CSS4) for all image
        property: facecolor_alpha: opacity for all image, default 1.0
        property: bgcolor: background color (base or CSS4) for diagramm figure 
        property: bgcolor_alpha: opacity for diagramm figure background color, default 1.0
        property: fontcolor: font color (base or CSS4) for title (supertitle), x-axis, y-axis, default 'black'
        property: grid: enable or disable grid lines, default True
        property: ticks: enable or disable ticks on x-axis & y-axis, default True
        property: custom_x_ticks: custom sign for ticks on x-axis, default None
        property: dpi: resolution, default 90
        property: width: image width, defalt 800
        property: height: image height, default 600
        
        method: setTitle(title): set title property
        method: setXLabel(xlabel): set xlabel property
        method: setYLabel(ylabel): set ylabel property
        method: setSize(width, height): set width & height properties
        method: fileToSave(filename): set filename property
        method: EnableGrid(): set grid property to True
        method: DisableGrid(): set grid property to False
        method: HideTicks(): set ticks property to False
        method: setFaceColor(facecolor, alpha): set facecolor & facecolor_alpha properties
        method: setBgColor(bgcolor, alpha): set bgcolor & bgcolor_alpha properties
        method: setBgImage(filename): set imgbackground property
        method: showbgimage(minmax, aspect): read background image file & apply it as background of diagramm
        method: setFontColor(color): set fontcolor property
        method: getMarkersList(): return avalaible markers
        method: getColorsList(): return avalaible colors
        method: is_sequence(object): return is the object an instance of set, list, tuple or dictionary
    """
    
    title: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    filename: Union[str, None]
    imgbackground: Union[str, None]
    facecolor: Union[str, None]
    facecolor_alpha: float = 1.0
    bgcolor: Union[str, None]
    bgcolor_alpha: float = 1.0
    fontcolor: str = 'black'
    
    grid: bool = True
    ticks: bool = True
    
    custom_x_ticks: Union[list, None] = None
    
    dpi: int = 90
    width: int = 800
    height: int = 600
    
    margins = {
        "left"   : 0.084,
        "right"  : 0.920,
        "top"    : 0.900,
        "bottom" : 0.092
    }
    
    __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
    __markers = [*Line2D.markers.keys()]
    
    def __init__(self, title = None, xlabel = None, ylabel = None):
        """
            Creates an instance of an object 
            
            :param title: title (or supertitle) for diagramm (all diagramms in one image)
            :param xlabel: name of x-axis
            :param ylabel: name of y-axis
        """
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def setTitle(self, title = None):
        self.title = title
    
    def setXLabel(self, xlabel = None):
        self.xlabel = xlabel
    
    def setYLabel(self, ylabel = None):
        self.ylabel = ylabel
    
    def setSize(self, widht: int, height: int):
        self.width = widht
        self.height = height
        
    def fileToSave(self, filename: str):
        self.filename = filename
    
    def EnableGrid(self):
        self.grid = True
    
    def DisableGrid(self):
        self.grid = False
        
    def HideTicks(self):
        self.ticks = False
        
    def setXTicks(self, x_ticks: list):
        self.custom_x_ticks = x_ticks
    
    def setFaceColor(self, facecolor: str, alpha: float = 1.0):
        if alpha > 1:
            alpha = 1.0 
        if alpha < 0:
            alpha = 0.0 
        if facecolor in (self.__colors):
            self.facecolor = facecolor
            self.facecolor_alpha = alpha
    
    def setBgColor(self, bgcolor: str, alpha: float = 1.0):
        if alpha > 1:
            alpha = 1.0 
        if alpha < 0:
            alpha = 0.0 
        if bgcolor in (self.__colors):
            self.bgcolor = bgcolor
            self.bgcolor_alpha = alpha
    
    def setBgImage(self, filename: str):
        self.imgbackground = filename
        
    def showbgimage(self, minmax: Union[tuple, None] = None, aspect = 'auto'):
        """
            This method read background image file & apply it as background of diagramm
            
            :param minmax: set of image corners (min_X, max_X, min_Y, max_Y) 
            :param aspect: 'auto' | 'equal'
        """
        try:
            img = plt.imread(self.imgbackground)
            if minmax is not None:
                extent = list(minmax)
            else:
                extent = [0, self.width / self.dpi, 0, self.height / self.dpi]
            plt.imshow(img, interpolation='antialiased', aspect = aspect, extent=extent)
        except FileNotFoundError:
            pass
        except OSError as e:
            pass
        except SystemError as e:
            pass
        except Exception as e:
            pass
            
    def setFontColor(self, fontcolor:str):
        if fontcolor in (self.__colors):
            self.fontcolor = fontcolor
            
    def getMarkersList(self):
        """ Return avalaible markers """
        return self.__markers
        
    def getColorsList(self):
        """ Return avalaible colors """
        return self.__colors
    
    def is_sequence(self, obj):
        t = type(obj)
        return hasattr(t, '__len__') and hasattr(t, '__getitem__')
        
    @abstractmethod
    def Plot(self):
        pass
        
class Scatter(ChartBuilder):
    """ 
        ChartBuilder implementation for Scatter diagramm 
        
        method: Plot(*data): biuld diagramm and show it (or save into the file)
    """
    class ScatterData():
        """ This class describe data structure for Scatter diagramm """
        dataset: list ## [(x1,y1),(x2,y2),...]
        label: Union[str, None]
        color: str
        marker: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
        __markers = [*Line2D.markers.keys()]
    
        def __init__(self, dataset: Union[list, tuple] , label = None, color = None, marker = None):
            """ 
                Creates an instance of an object ScatterData 
                
                :param dataset: Source data sequence
                :param label: name of dataset
                :param color: color for this dataset
                :param marker: type of marker
            """
            self.dataset = list(dataset)
            self.label = label
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
            if marker is None or marker not in (self.__markers):
                marker = self.__markers[0]
            self.marker = marker
    
    def Plot(self, *data: ScatterData):
        """
            This method biuld diagramm and show it (or save into the file)
            
            :param *data: one or more sets of source data
        """
        legend = False
        
        fig = plt.figure(dpi = self.dpi, figsize = (self.width / self.dpi, self.height / self.dpi) )
        if hasattr(self, 'facecolor') and self.facecolor is not None:
            fig.set(facecolor = self.facecolor)
            fig.set(alpha = self.facecolor_alpha)
        
        fig.subplots_adjust(**self.margins)
        
        ax = fig.add_subplot(1,1,1)
        if hasattr(self, 'bgcolor') and self.bgcolor is not None:
            ax.set(facecolor = self.bgcolor)
            ax.set(alpha = self.bgcolor_alpha)
        
        for item in data:
            if isinstance(item, self.ScatterData):
                if item.dataset is not None:
                    x = [value[0] for value in item.dataset if self.is_sequence(value) and len(value) == 2]
                    y = [value[1] for value in item.dataset if self.is_sequence(value) and len(value) == 2]
                if item.label is not None:
                    ax.scatter(x, y, label=item.label, color=item.color, marker=item.marker)
                    legend = True
                else:
                    ax.scatter(x, y, color=item.color, marker=item.marker)
        
        min_X, max_X = plt.xlim()
        min_Y, max_Y = plt.ylim()
        
        if hasattr(self, 'imgbackground') and self.imgbackground is not None:
            self.showbgimage( (min_X, max_X, min_Y, max_Y) )
        
        if self.title is not None:
            plt.title(self.title, color = self.fontcolor)
        if self.xlabel is not None:
            plt.xlabel(self.xlabel, color = self.fontcolor)
        if self.ylabel is not None:
            plt.ylabel(self.ylabel, color = self.fontcolor)
        if legend:
            plt.legend()
        
        if self.grid:
            plt.grid(True)
        else:
            plt.grid(False)
        
        if not self.ticks:
            plt.xticks([])
            plt.yticks([])
        else:
            ax.tick_params(axis = "x", colors = self.fontcolor)
            ax.tick_params(axis = "y", colors = self.fontcolor)
        
        if hasattr(self, 'filename') and self.filename is not None:
            plt.savefig(self.filename)
        else:
            plt.show()

class LineGraph(ChartBuilder):
    """ 
        ChartBuilder implementation for LineGraph diagramm 
        
        method: Plot(*data): biuld diagramm and show it (or save into the file)
    """
    class LineData():
        """ This class describe data structure for LineGraph diagramm """
        dataset: list ## [(x1,y1),(x2,y2),...]
        label: Union[str, None]
        color: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
    
        def __init__(self, dataset: Union[list, tuple] , label = None, color = None):
            """ 
                Creates an instance of an object LineData
                
                :param dataset: Source data sequence
                :param label: name of dataset
                :param color: color for this dataset
            """
            self.dataset = ChartDataHelper.data_sort_by_x(list(dataset))
            self.label = label
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
        
    def Plot(self, *data: LineData):
        """
            This method biuld diagramm and show it (or save into the file)
            
            :param *data: one or more sets of source data
        """
        legend = False
        
        fig = plt.figure(dpi = self.dpi, figsize = (self.width / self.dpi, self.height / self.dpi) )
        if hasattr(self, 'facecolor') and self.facecolor is not None:
            fig.set(facecolor = self.facecolor)
            fig.set(alpha = self.facecolor_alpha)
        
        fig.subplots_adjust(**self.margins)
        
        ax = fig.add_subplot(1,1,1)
        if hasattr(self, 'bgcolor') and self.bgcolor is not None:
            ax.set(facecolor = self.bgcolor)
            ax.set(alpha = self.bgcolor_alpha)
        
        for item in data:
            if isinstance(item, self.LineData):
                if item.dataset is not None:
                    x = [value[0] for value in item.dataset if self.is_sequence(value) and len(value) == 2]
                    y = [value[1] for value in item.dataset if self.is_sequence(value) and len(value) == 2]
                if item.label is not None:
                    ax.plot(x, y, label=item.label, color=item.color)
                    legend = True
                else:
                    ax.plot(x, y, color=item.color)
        
        min_X, max_X = plt.xlim()
        min_Y, max_Y = plt.ylim()
        
        if hasattr(self, 'imgbackground') and self.imgbackground is not None:
            self.showbgimage( (min_X, max_X, min_Y, max_Y) )
            
        if self.title is not None:
            plt.title(self.title, color = self.fontcolor)
        if self.xlabel is not None:
            plt.xlabel(self.xlabel, color = self.fontcolor)
        if self.ylabel is not None:
            plt.ylabel(self.ylabel, color = self.fontcolor)
        if legend:
            plt.legend()
        
        if self.grid:
            plt.grid(True)
        else:
            plt.grid(False)
            
        if not self.ticks:
            plt.xticks([])
            plt.yticks([])
        else:
            ax.tick_params(axis = "x", colors = self.fontcolor)
            ax.tick_params(axis = "y", colors = self.fontcolor)
        
        if hasattr(self, 'filename') and self.filename is not None:
            plt.savefig(self.filename)
        else:
            plt.show()

class Hist(ChartBuilder):
    """ 
        ChartBuilder implementation for Histogramm 
        
        method: Plot(*data): biuld diagramm and show it (or save into the file)
    """
    class HistData():
        """ This class describe data structure for Histogramm """
        values: list
        step: int
        hist_title: Union[str, None]
        color: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
        
        def __init__(self, dataset: Union[list, tuple], step: int = 10, hist_title = None, color = None):
            """ 
                Creates an instance of an object HistData 
                
                :param dataset: Source data sequence
                :param step: step for histogramm bins
                :param hist_title: title of diagramm
                :param color: color for this dataset
            """
            self.values = list(dataset)
            self.step = step
            self.hist_title = hist_title
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
            
    def Plot(self, *data: HistData):
        """
            This method biuld diagramm and show it (or save into the file)
            
            :param *data: one or more sets of source data
        """
        legend = False
        
        diag_cnt = 0
        for item in data:
            if isinstance(item, self.HistData):
                diag_cnt += 1
          
        fig = plt.figure(dpi = self.dpi, figsize = (self.width / self.dpi, diag_cnt * self.height / self.dpi) )
        if hasattr(self, 'facecolor') and self.facecolor is not None:
            fig.set(facecolor = self.facecolor)
            fig.set(alpha = self.facecolor_alpha)
        
        fig.subplots_adjust(**self.margins)
        
        axs_cnt = 1
        for item in data:
            if isinstance(item, self.HistData):
                ax = fig.add_subplot(diag_cnt, 1, axs_cnt)
                if hasattr(self, 'bgcolor') and self.bgcolor is not None:
                    ax.set(facecolor = self.bgcolor)
                    ax.set(alpha = self.bgcolor_alpha)
                
                max_value = max(item.values)
                min_value = min(item.values)
                bins = [i for i in range(min_value-1, max_value+item.step, item.step)]
                ax.hist(item.values, bins , histtype='bar', rwidth=0.8, color=item.color)
                
                min_X, max_X = plt.xlim()
                min_Y, max_Y = plt.ylim()
                        
                if hasattr(self, 'imgbackground') and self.imgbackground is not None:
                    self.showbgimage( (min_X, max_X, min_Y, max_Y) )
                
                if self.grid:
                    ax.grid(True)
                else:
                    ax.grid(False)
                
                if item.hist_title is not None:
                    plt.title(item.hist_title, color = self.fontcolor)
                if self.xlabel is not None:
                    plt.xlabel(self.xlabel, color = self.fontcolor)
                if self.ylabel is not None:
                    plt.ylabel(self.ylabel, color = self.fontcolor)
                
                if not self.ticks:
                    plt.xticks([])
                    plt.yticks([])
                else:
                    ax.tick_params(axis = "x", colors = self.fontcolor)
                    ax.tick_params(axis = "y", colors = self.fontcolor)
                
                axs_cnt += 1
        
        if self.title is not None:
            fig.suptitle(self.title, color = self.fontcolor)
            
        if hasattr(self, 'filename') and self.filename is not None:
            plt.savefig(self.filename)
        else:
            plt.show()

class Bar(ChartBuilder):
    """ 
        ChartBuilder implementation for Bar diagramm 
        
        method: Plot(*data): biuld diagramm and show it (or save into the file)
    """
    class BarData():
        """ This class describe data structure for Bar diagramm """
        x_values: list
        y_values: list
        bar_title: Union[str, None]
        color: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
        
        def __init__(self, dataset: Union[list, tuple], bar_title = None, color = None):
            """ 
                Creates an instance of an object BarData 
                
                :param dataset: Source data sequence
                :param bar_title: title of diagramm
                :param color: color for this dataset 
            """
            dataset = ChartDataHelper.data_sort_by_x(list(dataset))
            x_values, y_values = [], []
            for item in dataset:
                x_values.append(item[0])
                y_values.append(item[1])
            self.y_values = y_values
            self.x_values = x_values
            self.bar_title = bar_title
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
            
    def Plot(self, *data: BarData):
        """
            This method biuld diagramm and show it (or save into the file)
            
            :param *data: one or more sets of source data
        """
        legend = False
        
        diag_cnt = 0
        for item in data:
            if isinstance(item, self.BarData):
                diag_cnt += 1
          
        fig = plt.figure(dpi = self.dpi, figsize = (self.width / self.dpi, diag_cnt * self.height / self.dpi) )
        if hasattr(self, 'facecolor') and self.facecolor is not None:
            fig.set(facecolor = self.facecolor)
            fig.set(alpha = self.facecolor_alpha)
        
        fig.subplots_adjust(**self.margins)
        
        axs_cnt = 1
        for item in data:
            if isinstance(item, self.BarData):
                ax = fig.add_subplot(diag_cnt, 1, axs_cnt)
                if hasattr(self, 'bgcolor') and self.bgcolor is not None:
                    ax.set(facecolor = self.bgcolor)
                    ax.set(alpha = self.bgcolor_alpha)
                
                ax.bar(item.x_values, item.y_values, color=item.color)
                
                min_X, max_X = plt.xlim()
                min_Y, max_Y = plt.ylim()
                        
                if hasattr(self, 'imgbackground') and self.imgbackground is not None:
                    self.showbgimage( (min_X, max_X, min_Y, max_Y) )
                
                if self.grid:
                    plt.grid(True)
                else:
                    plt.grid(False)
                
                if item.bar_title is not None:
                    plt.title(item.bar_title, color = self.fontcolor)
                    
                if self.xlabel is not None:
                    plt.xlabel(self.xlabel, color = self.fontcolor)
                if self.ylabel is not None:
                    plt.ylabel(self.ylabel, color = self.fontcolor)
                    
                if not self.ticks:
                    plt.xticks([])
                    plt.yticks([])
                else:
                    ax.tick_params(axis = "x", colors = self.fontcolor)
                    ax.tick_params(axis = "y", colors = self.fontcolor)
                    if self.custom_x_ticks is not None:
                        if len(self.custom_x_ticks) == len(item.x_values):
                            plt.xticks(item.x_values, self.custom_x_ticks)
                        else:
                            plt.xlabel(f'Error: count of custom x-ticks and count of values doesn\'t match')
                axs_cnt += 1
        
        if self.title is not None:
            fig.suptitle(self.title, color = self.fontcolor)
            
        if hasattr(self, 'filename') and self.filename is not None:
            plt.savefig(self.filename)
        else:
            plt.show()

class Pie(ChartBuilder):
    """ 
        ChartBuilder implementation for Pie diagramm 
        
        property: custom_item_names: cutmom names for diagramm items (pie sectors)
        
        method: Plot(*data): biuld diagramm and show it (or save into the file)
        method: setItemNames(item_names): set property custom_item_names
    """
    custom_x_ticks = None
    custom_item_names: Union[list, None] = None
    
    class PieData():
        """ This class describe data structure for Pie diagramm """
        values: list
        labels: list
        minvalue: float
        pie_title: Union[str, None]
        
        def __init__(self, dataset: Union[list, tuple], pie_title = None, minpercent: int = 0):
            """ 
                Creates an instance of an object PieData 
                
                :param dataset: Source data sequence
                :param pie_title: Title of diagramm
                :param minpersent: minimum value (in %) below which verities will be discarded
            """
            dataset = ChartDataHelper.data_sort_by_x(list(dataset))
            values, labels = [], []
            for item in dataset:
                labels.append(item[0])
                values.append(item[1])
            self.labels = labels
            self.values = values
            summ = sum([val for val in values])
            min_value = minpercent * summ / 100
            self.minvalue = min_value
            self.pie_title = pie_title
    
    def setXTicks(self, x_ticks: list):
        """ Override an inherited method setXTicks """
        pass
    
    def EnableGrid(self):
        """ Override an inherited method EnableGrid """
        pass
    
    def DisableGrid(self):
        """ Override an inherited method DisableGrid """
        pass
        
    def HideTicks(self):
        """ Override an inherited method HideTicks """
        pass
    
    def setItemNames(self, item_names: list):
        """
            This method set property custom_item_names
            
            :param item_names: list of custom item names
        """
        self.custom_item_names = item_names
    
    def Plot(self, *data: PieData):
        """
            This method biuld diagramm and show it (or save into the file)
            
            :param *data: one or more sets of source data
        """
        diag_cnt = 0
        for item in data:
            if isinstance(item, self.PieData):
                diag_cnt += 1
          
        fig = plt.figure(dpi = self.dpi, figsize = (self.width / self.dpi, diag_cnt * self.height / self.dpi) )
        if hasattr(self, 'facecolor') and self.facecolor is not None:
            fig.set(facecolor = self.facecolor)
            fig.set(alpha = self.facecolor_alpha)
        
        axs_cnt = 1
        for item in data:
            if isinstance(item, self.PieData):
                if self.custom_item_names is not None and len(self.custom_item_names) == len(item.labels):
                    for i in range(len(item.labels)):
                        item.labels[i] = self.custom_item_names[i]
                filtered_dataset = [ (item.values[i], item.labels[i]) for i in range(len(item.values)) if item.values[i] >= item.minvalue]
                item.values = [value[0] for value in filtered_dataset]
                item.labels = [value[1] for value in filtered_dataset]
                
                total = sum(item.values)
                labels = [f"{n} ({v/total:.1%})" for n,v in zip(item.labels, item.values)]
                
                ax = fig.add_subplot(diag_cnt, 1, axs_cnt)
                if hasattr(self, 'bgcolor') and self.bgcolor is not None:
                    fig.set(facecolor = self.bgcolor)
                    fig.set(alpha = self.bgcolor_alpha)
                
                ax.pie(item.values, autopct='%1.1f%%', shadow=True, startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle. 
                ax.legend(bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25), loc = 'best', labels = labels )
                
                min_X, max_X = plt.xlim()
                min_Y, max_Y = plt.ylim()
                
                if hasattr(self, 'imgbackground') and self.imgbackground is not None:
                    self.showbgimage( (min_X, max_X, min_Y, max_Y), 'equal' )
                
                if item.pie_title is not None:
                    plt.title(item.pie_title, color = self.fontcolor)
                
                axs_cnt += 1
        
        if self.title is not None:
            fig.suptitle(self.title, color = self.fontcolor)
        
        if hasattr(self, 'filename') and self.filename is not None:
            plt.savefig(self.filename)
        else:
            plt.show()

class ChartDataHelper():
    """ This class contains auxiliary methods for data preprocessing """
    @staticmethod
    def data_count(src_data: list):
        """
            This method counts the number of repetitions for each element of the original sequence
            
            :param src_data: Original sequence (list or tuple)
            :return: The sequence of tuples, contains (element, count of element)
        """
        return set([(item, src_data.count(item)) for item in src_data])
        
    @staticmethod
    def data_sort_by_x(x_y_data: list):
        """
            This method sort sequence of lists (or tuples) by first item of each list (tuple)
            
            :param x_y_data: Original sequence (list or tuple of lists|tuples)
            :return: Sorted sequence
        """
        return sorted(x_y_data, key=lambda v: v[0])
    
    @staticmethod
    def data_sort_by_y(x_y_data: list):
        """
            This method sort sequence of lists (or tuples) by second item of each list (tuple)
            
            :param x_y_data: Original sequence (list or tuple of lists|tuples)
            :return: Sorted sequence
        """
        return sorted(x_y_data, key=lambda v: v[1])
    
    @staticmethod
    def data_percentage(counted_data: list):
        """
            This method count of items in sequence to percentage.
            
            :param counted_data: The sequence of tuples, contains (element, count_of_element)
            :return: The sequence of tuples, contains (element, item_percentage)
        """
        counted_data = list(counted_data)
        total_summ = sum([val[1] for val in counted_data])
        for i in range(len(counted_data)):
            percent = round(((counted_data[i][1] * 100) / total_summ), 2)
            value = counted_data[i][0]
            counted_data[i] = (value, percent) 
        return counted_data
    
    @staticmethod
    def data_to_ranges(src_data: list, step: int = 10):
        """
            This method forms ranges with a given step from the source data.
            Used for naming of x-axis in bar diagramm or for naming in pie diagramm
            
            :param src_data: Original sequence (list, set or tuple)
            :param step: Step for forming bins borders
            :return: Sequence of ranges (list of tuples contains values [(start_of_bin, end_of_bin),...]
        """
        max_value = max(src_data)
        min_value = min(src_data)
        bins = [i for i in range(min_value-1, max_value+step, step)]
        out_data = [(b, b+step) for b in bins for value in src_data if b <= value < b+step ]
        return out_data
    
    @staticmethod
    def map_prepare(mapfile: str):
        """
            This method prepare map file for using as tracking (scatter) background
            
            :param mapfile: filename of image with map
            :return: filename of prepared map, map width, map height, map corners
        """
        ## Prepare map: add borders = (width|height) / 20:
        axis_margin_ratio = 20 ## Yep, it's a magic (magic of matplotlib)
        abs_mapfile_path = os.path.abspath(mapfile)
        fname = os.path.basename(abs_mapfile_path)
        abs_folder = abs_mapfile_path.replace(fname, '')
        im = Image.open(mapfile)
        (width, height) = im.size
        img = ImageOps.expand(im, border=int(max(width, height)/axis_margin_ratio), fill='#ffffff')
        (new_width, new_height) = img.size
        crops = (
            ( 0 + (new_width - int(width + 2*(width/axis_margin_ratio)))//2 ), # top left x
            ( 0 + (new_height - int(height + 2*(height/axis_margin_ratio)))//2 ), # top left y
            (new_width - (new_width - int(width + 2*(width/axis_margin_ratio)))//2 ), # bottom right x
            (new_height - (new_height - int(height + 2*(height/axis_margin_ratio)))//2 ), # bottom right y
        )
        img2 = img.crop(crops)
        mapfile = f"{abs_folder}prepared_map_{width}_{height}.jpg"
        img2.save(mapfile, quality = 80)
        corner_points = [(0,0),(0,height),(width,0),(width, height)]
        
        return mapfile, width, height, corner_points

    @staticmethod
    def data_crop(src_data: list, min_x, min_y, max_x, max_y):
        """
            This method excludes elements outside a range from a sequence
            
            :param src_data: Original sequence (list or tuple of lists|tuples)
            :param min_x: lower limit of the range 
            :param min_y: lower limit of the range
            :param max_x: upper range limit
            :param max_y: upper range limit
            :return: Filtered sequence
        """
        out_data = [item for item in src_data if item[0] > min_x and item[0] < max_x and item[1] > min_y and item[1] < max_y]
        return out_data
