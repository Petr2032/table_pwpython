#!/usr/bin/env python

import wx
import wx.grid
import os
import re


class Table(wx.grid.Grid):
    def __init__(self, parent, *arg, row=1, col=1):
        wx.grid.Grid.__init__(self,parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.row = row
        self.col = col

        # Grid
        self.CreateGrid(self.row, self.col)
        self.EnableEditing(True)
        self.EnableGridLines(True)
        self.EnableDragGridSize(False)
        self.SetMargins(0, 0)

        # Columns
        self.EnableDragColMove(False)
        self.EnableDragColSize(True)
        self.SetColLabelSize(30)
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.EnableDragRowSize(True)
        self.SetRowLabelSize(80)
        self.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance
        self.SetLabelFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.SetLabelTextColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))

        # Cell Defaults
        self.SetDefaultCellBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetDefaultCellFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_TOP)
        self.SetFont(wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
    #Очистка содержания таблицы
    def clear(self):
        self.ClearGrid()
    
    # Добавить указанное количество строк с низу
    def addRowDown(self, num):
        self.AppendRows(numRows=num)
    
    # Добавить указанное количество строк с верху
    def addColUp(self, num):
        pass
    # Добавить указанное количество строк в указанную позицию
    def addRowUp(self, mpos, num): 
        self.InsertRows(pos=mpos, numRows=num)
    
    # Добавить указанное количество колонок слева
    def addColL(self, num):
        pass

    # Удалить указанное количество колонок
    def delCol(self, mpos, num):
        self.DeleteCols(pos=mpos, numCols=num)
    
    # Добавить указанное количество колонок справа
    def addColR(self, num):
        self.AppendCols(numCols=num)

    # Добавить указанное количество колонок в указанную позицию
    def addColpos(self,mpos, num):
        self.InsertCols(pos=mpos, numCols=num)
    # Удалить указанное количество колонок
    def delRow(self, mpos, num):
        self.DeleteRows(pos=mpos, numRows=num)
     
    #Запись данные в ячейку с указанием номера ячейки
    def setValue(self, row, col, value):
        pass
    #Создать таблицу с заданным количеством строк и столбцов
    def setTable(self, row, col):
        #Удаляем все строки и столбцы
        self.DeleteCols(pos=0, numCols = self.GetNumberCols())
        self.DeleteRows(pos=0, numRows = self.GetNumberRows())
        self.AppendRows(row)
        self.AppendCols(col)

    #Загрузка в таблицу массив (размер массива подгоняется под размер массива)
    # Ячейки предворительно очистить и удалить ненужные строки
    def setValues(self, values):
        self.values = values
        self.row = 0
        self.col = 0        
        #Вычислить количество строк и количество столбцов в массиве
        self.row = len(self.values)
        for self.r in range(self.row):
            if self.col < len(self.values[self.r]):
                self.col = len(self.values[self.r])
        #Создаем необходимую таблицу
        self.setTable(self.row, self.col)
        #Очищаем её
        self.ClearGrid()
        #Записываем данные
        for self.r in range(self.row):
            for self.c in range(len(self.values[self.r])):
                    self.SetCellValue(self.r, self.c, self.values[self.r][self.c])
    #Методы получения, выбранных ячеек


class Frame(wx.Frame):
    def __init__(self, parent):

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Сбор данныйх измерений", pos=wx.DefaultPosition, size=wx.Size(
            1000, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        
        bSizer = wx.BoxSizer(wx.VERTICAL)
        self.m_grid1 = Table(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, row=10, col=10)

        bSizer.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.pattern = r"-?[\d.]+b?"
        self.massiv = []
        with open('нт 508_7.txt', 'r') as self.f:
            for self.st in self.f:
                self.massiv.append(re.findall(self.pattern, self.st))
        
        self.m_grid1.setValues(self.massiv)


if __name__ == '__main__':
    app = wx.App()
    frame = Frame(None)
    frame.Show()

    app.MainLoop()
