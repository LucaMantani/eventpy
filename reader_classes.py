import numpy as np
# from bs4 import BeautifulSoup
from Analysis_functions import *
import xml.etree.ElementTree as ET


class Process:
    """
    Class process that takes a text file in one of the supported formats
    and recognise events and particles.
    Return: object of the class.
    """

    supported_file_formats = ['lhe']

    def __init__(self, txt_file):

        file_format = txt_file.split('.')[-1]

        if file_format not in Process.supported_file_formats:
            print("File format %s not recognised." % file_format)
        else:
            if file_format == 'lhe':
                self.events = self.read_lhe(txt_file)

            self._num_events = len(self.events)

            self._cross_section = sum([event.weight for event in self.events])

    # def read_lhe(self, txt_file):

    #     with open(txt_file, 'r') as f:
    #         soup = BeautifulSoup(f, "lxml")

    #         events = []

    #         for event in soup.find_all('event'):
    #             events.append(Event(event.string.strip('\n').split('\n'),
    #                                 'lhe'))

    #     return events

    def read_lhe(self, txt_file):

        events = []

        try:
            for event, element in ET.iterparse(txt_file, events=['end']):
                if element.tag == 'event':
                    events.append(Event(element.text.split('\n')[1:-1], 'lhe'))

        except ET.ParseError:
            return events

        return events

    @property
    def num_events(self):
        return self._num_events

    @property
    def cross_section(self):
        return self._cross_section

    def __str__(self):
        return "Number of events: %i\nCross section: %f\n"\
                % (self.num_events, self.cross_section) +\
               ''.join([event.__str__() for event in self.events])


class Event:
    """
    Event class, reads the event provided as a list of strings
    in a specified format, extracts the weight and
    defines the various particles.
    Return: object of the class.
    """

    def __init__(self, event, event_type):

        if event_type == 'lhe':

            general_info = event[0].strip().split()
            self._tot_particles = int(general_info[0])
            self._weight = float(general_info[2])

            self.particles = []

            for line in event[1:]:
                line = line.strip().split()

                if line[0].lstrip('-').isdigit():
                    self.particles.append(Particle(line, 'lhe'))

            self.initial_states = [particle
                                   for particle in self.particles
                                   if particle.status == -1]
            self.final_states = [particle
                                 for particle in self.particles
                                 if particle.status == 1]

    @property
    def weight(self):
        return self._weight

    @property
    def tot_particles(self):
        return self._tot_particles

    def __str__(self):
        return "\nEvent weight: %f\nTotal number of particles: %i\n"\
                % (self.weight, self.tot_particles) +\
               ''.join([particle.__str__() for particle in self.particles])


class Particle:
    """
    Particle class, reads a string in a specific format describing a particle.
    Return: object of the class.
    """

    def __init__(self, particle_info, particle_type):

        if particle_type == 'lhe':
            self._pdg = int(particle_info[0])
            self._status = int(particle_info[1])
            self._px = float(particle_info[6])
            self._py = float(particle_info[7])
            self._pz = float(particle_info[8])
            self._E = float(particle_info[9])
            self._M = float(particle_info[10])
            self._ctau = float(particle_info[11])
            self._DV = self._ctau * versor(self.mom3)

    @property
    def pdg(self):
        return self._pdg

    @property
    def status(self):
        return self._status

    @property
    def px(self):
        return self._px

    @property
    def py(self):
        return self._py

    @property
    def pz(self):
        return self._pz

    @property
    def E(self):
        return self._E

    @property
    def M(self):
        return self._M

    @property
    def ctau(self):
        return self._ctau

    @property
    def mom(self):
        return np.array([self._E, self._px, self._py, self._pz])

    @property
    def mom3(self):
        return np.array([self._px, self._py, self._pz])

    @property
    def p3(self):
        return np.sqrt(self._px ** 2 + self._py ** 2 + self._pz ** 2)

    @property
    def pT(self):
        return np.sqrt(self._px**2 + self._py**2)

    @property
    def y(self):
        return 0.5 * np.log((self._E + self._pz)/(self._E - self._pz))

    @property
    def eta(self):
        return 0.5 * np.log((self.p3 + self._pz)/(self.p3 - self._pz))

    @property
    def ET(self):
        return np.sqrt(self._M ** 2 + self.pT ** 2)

    @property
    def beta(self):
        return self.p3 / self._E

    @property
    def gamma(self):
        return 1 / np.sqrt(1 - self.beta ** 2)

    @property
    def theta(self):
        return np.arctan2(self.pT, self._pz)

    @property
    def phi(self):
        return np.arctan2(self._py, self._px)

    @property
    def DV(self):
        return self._DV

    def isin(self, particles):
        for particle in particles:
            if self._pdg == particle.pdg:
                return True
        return False

    def is_pdg(self, pdg):
        return self._pdg == pdg

    def set_DV(self, DV):
        self._DV = DV

    def delta_R(self, particle):
        return np.sqrt((self.eta - particle.eta)**2 +
                       (self.phi - particle.phi)**2)

    def __str__(self):
        return "\nParticle information:\n" +\
               "pdg: %i\n" % self.pdg +\
               "status: %i\n" % self.status +\
               "px: %f\n" % self.px +\
               "py: %f\n" % self.py +\
               "pz: %f\n" % self.pz +\
               "E: %f\n" % self.E +\
               "M: %f\n" % self.M +\
               "ctau: %f\n" % self.ctau
