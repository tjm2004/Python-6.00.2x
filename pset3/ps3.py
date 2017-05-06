# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab
random.seed(0)
from ps3b_precompiled_36 import *

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''


# PROBLEM 1

class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() <= self.getClearProb():
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        '''
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        '''
        if random.random() <= (self.getMaxBirthProb() * (1 - popDensity)):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException(Exception)





class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.getViruses())


    def update(self):
        '''
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        '''

        for virus in self.getViruses()[:]:
            if virus.doesClear():
                self.viruses.remove(virus)

        pop_dense = self.getTotalPop()/self.getMaxPop()

        for virus in self.getViruses():
            try:
                self.viruses.append(virus.reproduce(pop_dense))
            except NoChildException as e:
                continue





#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """    
    from operator import add

    def trial():
        viruses = [SimpleVirus(maxBirthProb, clearProb) for x in list(range(numViruses))]
        Bob = Patient(viruses, maxPop)
        virus_population = []
        for x in range(300):
            Bob.update()
            virus_population.append(Bob.getTotalPop())
        return virus_population

    total_virus_population = [0.0 for x in range(300)]
    
    for x in list(range(numTrials)):
        total_virus_population = list(map(add, trial(), total_virus_population))

    avg_virus_population = []
    for timestep in total_virus_population:
        avg_virus_population.append(timestep/numTrials)

    pylab.plot(avg_virus_population, label='Virus Population')
    pylab.legend(loc='upper left')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.title('SimpleVirus simulation')
    pylab.show()

# simulationWithoutDrug(100,1000,.1,0.05,50)
#simulationWithoutDrug(100, 200, 0.2, 0.8, 1)
# simulationWithoutDrug(100,1000,.1,.05,100)

#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        try:
            return self.getResistances()[drug]
        except KeyError as e:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        for drug in activeDrugs:
            if self.isResistantTo(drug):
                continue
            else:
                raise NoChildException
        #virus is resistant to all drugs:
        if random.random() <= (self.getMaxBirthProb() * (1 - popDensity)):
            #virus has reproduced
            new_resistances = {}
            for resistance in self.getResistances():
                if random.random() <= self.getMutProb():
                    new_resistances[resistance] = not self.getResistances()[resistance]
                else:
                    new_resistances[resistance] = self.getResistances()[resistance]
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), new_resistances, self.getMutProb())
        else:
            raise NoChildException

      

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.activeDrugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.activeDrugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        total = 0
        for virus in self.getViruses():
            resistant = True
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    continue
                else:
                    resistant = False
                    break
            if resistant:
                total += 1
        return total



    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        
        for virus in self.getViruses()[:]:
            if virus.doesClear():
                self.getViruses().remove(virus)

        pop_dense = self.getTotalPop()/self.getMaxPop()


        for virus in self.getViruses()[:]:
            try:
                x = virus.reproduce(pop_dense, self.getPrescriptions())
                if x is not None:
                    self.getViruses().append(x)
            except NoChildException as e:
                continue

        return len(self.getViruses())




#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    from operator import add

    def trial():
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for x in list(range(numViruses))]
        Mary = TreatedPatient(viruses, maxPop)
        total_virus_pop_at_timesteps = []
        g_resistant_virus_pop_at_timesteps = []

        for x in range(150):
            Mary.update()
            total_virus_pop_at_timesteps.append(Mary.getTotalPop())
            g_resistant_virus_pop_at_timesteps.append(Mary.getResistPop(['guttagonol']))
        Mary.addPrescription('guttagonol')
        for x in range(150):
            Mary.update()
            total_virus_pop_at_timesteps.append(Mary.getTotalPop())
            g_resistant_virus_pop_at_timesteps.append(Mary.getResistPop(['guttagonol']))
        return total_virus_pop_at_timesteps, g_resistant_virus_pop_at_timesteps

    total_virus_population = [0.0 for x in range(300)]
    g_resistant_virus_population = [0.0 for x in range(300)]

    for x in list(range(numTrials)):
        total, g_total = trial()
        total_virus_population = list(map(add, total, total_virus_population))
        g_resistant_virus_population = list(map(add, g_total, g_resistant_virus_population))

    a_t_v_p = []
    a_gr_v_p = []

    for timestep in total_virus_population:
        a_t_v_p.append(timestep/numTrials)
    for timestep in g_resistant_virus_population:
        a_gr_v_p.append(timestep/numTrials)

    pylab.plot(a_t_v_p, label='total V pop')
    pylab.plot(a_gr_v_p, label='total resistant V pop')
    pylab.legend(loc='upper right')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.title('SimpleVirus simulation')
    pylab.show()


#simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
simulationWithDrug(100, 1000, .1, .005, {'guttagonal': False}, .005, 10)
simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
