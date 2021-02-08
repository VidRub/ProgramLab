class ExamException(Exception):
    pass


class CSVFile:
    def __init__(self,name):
        if not isinstance(name,str):
            raise ExamException("Non e' stato dato un nome di file")
        self.name = name

        try:
            open(name)
        except:
            raise ExamException("File non in directory")


class CSVTimeSeriesFile(CSVFile):
    def get_data(self):
        file_content = open(self.name,"r")
        file_list = []


        for line in file_content:
            TmpElem = line.split(",")
            try:
                int(TmpElem[0])
                float(TmpElem[1])
            except:
                continue
            TmpEpoch = int(TmpElem[0])
            TmpTemperature = float(TmpElem[1])
            TmpList = [TmpEpoch,TmpTemperature]
            file_list.append(TmpList)

        if len(file_list) == 0:
            raise ExamException("Lista vuota")
        
        for i in range(0,len(file_list)-1):
            if file_list[i][0] >= file_list[i+1][0]:
                raise ExamException("Lista non ordinata o epoch duplicati")

        return file_list 


def daily_stats(time_series):
    Somma = 0
    Cont = 0
    Max = None
    Min = None
    index = 0
    DailyList = []

    if len(time_series) == 1:
        DailyList.append([time_series[0][1],time_series[0][1],time_series[0][1]])
    else:
        for line in time_series:
            if index<len(time_series) - 1:
                NextDay = time_series[index+1][0] - (time_series[index+1][0] % 86400)
            Midnight = line[0] - (line[0] % 86400)

            
            Temperature = line[1]


            
            if Max == None:
                Max = Temperature
            if Min == None:
                Min = Temperature
            if Max < Temperature:
                Max = Temperature
            if Min > Temperature:
                Min = Temperature
            Somma = Somma + Temperature
            Cont = Cont+1

            if NextDay != Midnight:
                Media = Somma/Cont
                DailyList.append([Min,Max,Media])
                Somma = 0
                Cont = 0
                Max = None
                Min = None


            index = index + 1

            if index == len(time_series):
                Media = Somma/Cont
                DailyList.append([Min,Max,Media])
                break

        
        
    return DailyList

