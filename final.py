#Problem 3-2
# You have a bucket with 4 red balls and 4 green balls. You draw 3 balls out of the bucket. Assume that once 
# you draw a ball out of the bucket, you don't replace it. What is the probability of drawing 3 balls of the same color?

# Write a Monte Carlo simulation to solve the above problem. Feel free to write a helper function if you wish.

def drawing_without_replacement_sim(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns a float - the fraction of times 3 
    balls of the same color were drawn in the first 3 draws.
    '''
    def do_trial():
        bucket = ['R','R','R','R','G','G','G','G']
        in_hand = []

        def select_ball(bucket):
            while len(in_hand) < 3:
                ball = random.choice(bucket)
                in_hand.append(ball)
                bucket.remove(ball)
                select_ball(bucket)
            return in_hand
        
        return select_ball(bucket)

    def calc():
        result = do_trial()
        if result == ['G','G','G'] or result == ['R', 'R', 'R']:
            return 1
        else:
            return 0
    
    total = 0
    for trial in range(numTrials):
        total += calc()

    return total/numTrials


#PROBLEM 4

import random, pylab

# You are given this function
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# You are given this class
class Die(object):
    def __init__(self, valList):
        """ valList is not empty """
        self.possibleVals = valList[:]
    def roll(self):
        return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
    """
      - values, a sequence of numbers
      - numBins, a positive int
      - xLabel, yLabel, title, are strings
      - Produces a histogram of values with numBins bins and the indicated labels
        for the x and y axis
      - If title is provided by caller, puts that title on the figure and otherwise
        does not title the figure
    """
    pylab.hist(values, bins = numBins)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    if title != None:
        pylab.title(title)
    pylab.show()
    
                    
# Implement this -- Coding Part 2 of 2
def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number
        over numTrials runs of numRolls rolls.
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """
    max_count_list = []
    for trial in range(numTrials):
        
        all_trial_rolls = []
        
        for roll in range(numRolls):
            all_trial_rolls.append(die.roll())
        max_count = 1
        count = 1
        for roll in range(len(all_trial_rolls)):
            try:
                if all_trial_rolls[roll] == all_trial_rolls[roll + 1]:
                    count += 1
                    if count > max_count:
                        max_count = count
                else:
                    count = 1
            except IndexError as e:
                break
        max_count_list.append(max_count)
        
    makeHistogram(max_count_list, 10, 'Longest Run', 'Number of Trials', 'Longest Run Histogram')
    return sum(max_count_list)/len(max_count_list)

    
# One test case
print(getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000))


#Problem 6
# Write a function that meets the specifications below. You do not have to use dynamic programming.

# Hint: You might want to use bin() on an int to get a string, get rid of the first two characters, add 
# leading 0's as needed, and then convert it to a numpy array of ints. Type help(bin) in the console.

# For example,

# If choices = [1,2,2,3] and total = 4 you should return either [0 1 1 0] or [1 0 0 1]
# If choices = [1,1,3,5,3] and total = 5 you should return [0 0 0 1 0]
# If choices = [1,1,1,9] and total = 4 you should return [1 1 1 0]
# More specifically, write a function that meets the specifications below:

def find_combination(choices, total):
    """
    choices: a non-empty list of ints
    total: a positive int
 
    Returns result, a numpy.array of length len(choices) 
    such that
        * each element of result is 0 or 1
        * sum(result*choices) == total
        * sum(result) is as small as possible
    In case of ties, returns any result that works.
    If there is no result that gives the exact total, 
    pick the one that gives sum(result*choices) closest 
    to total without going over.
    """
    import itertools
    import numpy as np
    l = []
    for value in itertools.product('10', repeat = len(choices)):
        l.append(value)
    
    l2 = []
    for tup in l:
        l2.append(np.array([int(x) for x in tup]))

    next_best_answer = []
    best_answers = []
    best_answer_index = []
    
    for a in l2:
        if sum(a*choices) == total:
            best_answers.append(a)
            best_answer_index.append(sum(a))
        elif sum(a*choices) < total:
            next_best_answer.append(sum(a*choices))
        else:
            next_best_answer.append(0)

    if len(best_answers) > 0:
        return best_answers[best_answer_index.index(min(best_answer_index))]
    else:
        if max(next_best_answer) == 0:
            return np.array(len(choices)*[0])
        return l2[next_best_answer.index(max(next_best_answer))]


#Problem 8
# For this problem you are going to simulate growth of fox and rabbit population in a forest!

# The following facts are true about the fox and rabbit population:

# The maximum population of rabbits is determined by the amount of vegetation in the forest, which is relatively stable.

# There are never fewer than 10 rabbits; the maximum population of rabbits is 1000.

# For each rabbit during each time step, a new rabbit will be born with a probability of prabbit reproduction

# prabbit reproduction=1.0−current rabbit populationmax rabbit population

# In other words, when the current population is near the maximum, the probability of giving birth is very low, and when 
# the current population is small, the probability of giving birth is very high.

# The population of foxes is constrained by number of rabbits.

# There are never fewer than 10 foxes.

# At each time step, after the rabbits have finished reproducing, a fox will try to hunt a rabbit with success rate of pfox eats rabbit

# pfox eats rabbit=current rabbit populationmax rabbit population
# In other words, the more rabbits, the more likely a fox will eat one.

# If a fox succeeds in hunting, it will decrease the number of rabbits by 1 immediately. Remember that the population of rabbits is never lower than 10.

# Additionally, if a fox succeeds in hunting, then it has a 1/3 probability of giving birth in the current time-step.

# If a fox fails in hunting then it has a 10 percent chance of dying in the current time-step.

# If the starting population is below 10 then you should do nothing. You should not increase the population nor set the population to 10. 
# Start with 500 rabbits and 30 foxes.

# At the end of each time step, record the number of foxes and rabbits.

# Run the simulation for 200 time steps, and then plot the population of rabbits and the population of foxes as a function of time step. 
# (You do not need to paste your code for plotting for Part A of this problem).

# Use the following steps, and the template file rabbits.py (click to download .py file), as guides in your implementation of this simulation.

# Step 1: Write the procedure, rabbitGrowth, that updates the number of rabbits during the first part of a time step

# Step 2: Write the procedure, foxGrowth, that updates the number of rabbits and foxes during the second part of a time step

# Step 3: Write the master procedure, runSimulation, that loops for some amount of time steps, doing the first part and then the second part of 
# the simulation. Record the two populations in two different lists, and return those lists.

import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    rabbit_repro_prob = 1 - CURRENTRABBITPOP/MAXRABBITPOP

    new_rabbits = 0
    
    for rabbit in range(CURRENTRABBITPOP):
        if rabbit_repro_prob > random.random():
            new_rabbits += 1

    if CURRENTRABBITPOP + new_rabbits > MAXRABBITPOP:
        CURRENTRABBITPOP = MAXRABBITPOP
    else:
        CURRENTRABBITPOP += new_rabbits
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    
    new_foxes = 0
    dead_foxes = 0

    for fox in range(CURRENTFOXPOP):
        if CURRENTRABBITPOP <= 10:
            break
        else:
            fox_eat_prob = CURRENTRABBITPOP/MAXRABBITPOP
            if fox_eat_prob > random.random():
                CURRENTRABBITPOP -= 1
                if 1/3 > random.random():
                    new_foxes += 1
            else:
                if 9/10 > random.random():
                    dead_foxes += 1
    CURRENTFOXPOP = CURRENTFOXPOP + new_foxes - dead_foxes

    
            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbit_populations, fox_populations = [], []
    for timestep in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)

    return (rabbit_populations, fox_populations)

x = runSimulation(200)
wabits = x[0]
foxy = x[1]
pylab.plot(wabits, 'bd')
pylab.plot(foxy, 'rd')
pylab.title('blue is bunny, red is fox')


coeff = pylab.polyfit(range(len(wabits)), wabits, 2)
pylab.plot(pylab.polyval(coeff, range(len(wabits))))

coeff = pylab.polyfit(range(len(foxy)), foxy, 2)
pylab.plot(pylab.polyval(coeff, range(len(foxy))))

pylab.show()