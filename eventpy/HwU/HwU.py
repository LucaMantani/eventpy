import pandas as pd


class HwU_parser:

    def __init__(self, file):

        self.file = file
        self.histograms = self.read()

    def read(self):
        
        with open(self.file, 'r') as f:
            in_hist = False
            histograms = []
            hist = []
            for x in f:
                if x.startswith("##"):
                    self.entries_info = x.lstrip("##& ").rstrip("\n").split("&")

                if x.startswith(r"<\histogram>"):
                    histograms.append(Histogram(hist, self.entries_info, title))
                    hist = []
                    in_hist = False

                if in_hist:
                    hist.append(x.split())

                if x.startswith(r"<histogram>"):
                    in_hist = True
                    title = x.lstrip(r"<histogram>")

            return histograms



class Histogram:

    def __init__(self, data, data_info, title):
        # print(data)
        self.data = pd.DataFrame(data, columns=data_info, dtype=float)
        self.data.name = title

