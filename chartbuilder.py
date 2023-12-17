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
import random
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from PIL import Image, ImageOps
import os

class ChartBuilder():
    
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
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def setTitle(self, title = None):
        self.title = title
    
    def setXLabel(self, xlabel = None, ylabel = None):
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
        
    def __showbgimage__(self, minmax: Union[tuple, None] = None, aspect = 'auto'):
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
        return self.__markers #returns avalaible markers
        
    def getColorsList(self):
        return self.__colors #returns avalaible colors
    
    def __is_sequence__(self, obj):
        t = type(obj)
        return hasattr(t, '__len__') and hasattr(t, '__getitem__')
        
class Scatter(ChartBuilder):

    class ScatterData():
        dataset: list ## [(x1,y1),(x2,y2),...]
        label: Union[str, None]
        color: str
        marker: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
        __markers = [*Line2D.markers.keys()]
    
        def __init__(self, dataset: Union[list, tuple] , label = None, color = None, marker = None):
            self.dataset = list(dataset)
            self.label = label
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
            if marker is None or marker not in (self.__markers):
                marker = self.__markers[0]
            self.marker = marker
    
    def Plot(self, *data: ScatterData):
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
                    x = [value[0] for value in item.dataset if self.__is_sequence__(value) and len(value) == 2]
                    y = [value[1] for value in item.dataset if self.__is_sequence__(value) and len(value) == 2]
                if item.label is not None:
                    ax.scatter(x, y, label=item.label, color=item.color, marker=item.marker)
                    legend = True
                else:
                    ax.scatter(x, y, color=item.color, marker=item.marker)
        
        min_X, max_X = plt.xlim()
        min_Y, max_Y = plt.ylim()
        
        if hasattr(self, 'imgbackground') and self.imgbackground is not None:
            self.__showbgimage__( (min_X, max_X, min_Y, max_Y) )
        
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
        
    class LineData():
        dataset: list ## [(x1,y1),(x2,y2),...]
        label: Union[str, None]
        color: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
    
        def __init__(self, dataset: Union[list, tuple] , label = None, color = None):
            self.dataset = ChartDataHelper.data_sort_by_x(list(dataset))
            self.label = label
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
        
    def Plot(self, *data: LineData):
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
                    x = [value[0] for value in item.dataset if self.__is_sequence__(value) and len(value) == 2]
                    y = [value[1] for value in item.dataset if self.__is_sequence__(value) and len(value) == 2]
                if item.label is not None:
                    ax.plot(x, y, label=item.label, color=item.color)
                    legend = True
                else:
                    ax.plot(x, y, color=item.color)
        
        min_X, max_X = plt.xlim()
        min_Y, max_Y = plt.ylim()
        
        if hasattr(self, 'imgbackground') and self.imgbackground is not None:
            self.__showbgimage__( (min_X, max_X, min_Y, max_Y) )
            
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
    
    class HistData():
        values: list
        step: int
        hist_title: Union[str, None]
        color: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
        
        def __init__(self, dataset: Union[list, tuple], step: int = 10, hist_title = None, color = None):
            self.values = list(dataset)
            self.step = step
            self.hist_title = hist_title
            if color is None or color not in (self.__colors):
                color = self.__colors[random.randint(0,len(self.__colors)-1)]
            self.color = color
            
    def Plot(self, *data: HistData):
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
                    self.__showbgimage__( (min_X, max_X, min_Y, max_Y) )
                
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
    
    class BarData():
        x_values: list
        y_values: list
        bar_title: Union[str, None]
        color: str
        
        __colors = [*mcolors.BASE_COLORS.keys(), *mcolors.CSS4_COLORS.keys()]
        
        def __init__(self, dataset: Union[list, tuple], bar_title = None, color = None):
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
                    self.__showbgimage__( (min_X, max_X, min_Y, max_Y) )
                
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
    
    custom_x_ticks = None
    custom_item_names: Union[list, None] = None
    
    class PieData():
        values: list
        labels: list
        minvalue: float
        pie_title: Union[str, None]
        
        def __init__(self, dataset: Union[list, tuple], pie_title = None, minpercent: int = 0):
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
        pass
    
    def EnableGrid(self):
        pass
    
    def DisableGrid(self):
        pass
        
    def HideTicks(self):
        pass
    
    def setItemNames(self, item_names: list):
        self.custom_item_names = item_names
    
    def Plot(self, *data: PieData):
        
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
                    self.__showbgimage__( (min_X, max_X, min_Y, max_Y), 'equal' )
                
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
    
    @staticmethod
    def data_count(src_data: list):
        # input: 
        #   src_data: list or tuple of source data, [x1,x2,...]
        # returns set of tuple(s): {(item, count(item)),...}
        return set([(item, src_data.count(item)) for item in src_data])
        
    @staticmethod
    def data_sort_by_x(x_y_data: list):
        # input: x_y_data: list or tuple(s) of x & y data,  [(x,y),...]
        return sorted(x_y_data, key=lambda v: v[0])
    
    @staticmethod
    def data_sort_by_y(x_y_data: list):
        # input: x_y_data: list or tuple(s) of x & y data,  [(x,y),...]
        return sorted(x_y_data, key=lambda v: v[1])
    
    @staticmethod
    def data_percentage(counted_data: list):
        # input: 
        #   counted_data: list of tuple(s), [(item1, count(item1)), (item2, count(item2),...)] - source_data prepared with data_prepare_count()
        # returns list of tuple(s) with percents: [(item, item_percent),...]
        counted_data = list(counted_data)
        total_summ = sum([val[1] for val in counted_data])
        for i in range(len(counted_data)):
            percent = round(((counted_data[i][1] * 100) / total_summ), 2)
            value = counted_data[i][0]
            counted_data[i] = (value, percent) 
        return counted_data
    
    @staticmethod
    def data_to_ranges(src_data: list, step: int = 10):
        # input: 
        #   list or tuple(s) of source data, [x1,x2,...]
        #   step: int
        max_value = max(src_data)
        min_value = min(src_data)
        bins = [i for i in range(min_value-1, max_value+step, step)]
        out_data = [(b, b+step) for b in bins for value in src_data if b <= value < b+step ]
        return out_data
    
    @staticmethod
    def map_prepare(mapfile: str):
        ## Prepare map: add borders = (width|height) / 20:
        axis_margin_ratio = 20 ## Yep, it's a magic (magic of matplotlib)
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
        mapfile = f"img/prepared_map_{width}_{height}.jpg"
        img2.save(mapfile, quality = 80)
        corner_points = [(0,0),(0,height),(width,0),(width, height)]
        
        return mapfile, width, height, corner_points

    @staticmethod
    def data_crop(src_data: list, min_x, min_y, max_x, max_y):
        out_data = [item for item in src_data if item[0] > min_x and item[0] < max_x and item[1] > min_y and item[1] < max_y]
        return out_data
