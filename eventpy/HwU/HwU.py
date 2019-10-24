import pandas as pd
import numpy as np


class HwU_parser:
    """
    This is a class that reads a HwU file produced by NLO FixedOrder analysis
    in Madgraph.
    """

    def __init__(self, file):

        self.file = file
        self.histograms = self.read()

    def read(self):

        with open(self.file, 'r') as f:
            in_hist = False
            histograms = []
            hist = []
            title = ""
            for x in f:
                if x.startswith("##"):
                    self.entries_info = x.lstrip("##& ")\
                                        .rstrip("\n").split(" & ")

                    if self.entries_info[-1] == '':
                        self.entries_info = self.entries_info[:-1]

                if x.startswith(r"<\histogram>"):
                    histograms.append(Histogram(hist,
                                                self.entries_info,
                                                title))
                    hist = []
                    title = ""
                    in_hist = False

                if in_hist:
                    hist.append(x.split())

                if x.startswith(r"<histogram>"):
                    in_hist = True
                    title = x.lstrip(r"<histogram>")

            return histograms


class Histogram:
    """
    Histogram class for HwU hisograms.
    """

    def __init__(self, data, data_info, title):

        self.data = pd.DataFrame(data, columns=data_info, dtype=float)
        self.name = title

    def __str__(self):

        return self.name + "\n" + self.data.__str__()

    def bins(self):
        return np.append(self.data.loc[:, "xmin"].values,
                         (self.data.loc[:, "xmax"].values[-1]))
