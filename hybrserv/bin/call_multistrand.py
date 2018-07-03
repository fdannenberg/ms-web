import time

from multistrand.concurrent import Literals, MergeSim, MergeSimSettings
from multistrand.experiment import standardOptions, hybridization
from multistrand.builder import Builder, BuilderRate, dissociationString, hybridizationString
from multistrand.objects import StopCondition

A_TIME_OUT = 4.0
MAX_TRIALS = 20000
WALL_TIME_TIMEOUT = 30

REQ_SUCCESS = 30
TRIALS = 100

BUILDER_TRIALS = 12
BUILDER_TIMEOUT = 3e-5

    
def first_step_simulation(form):
 
    strand_seq = form['sequence']
 
    print ("Running first step mode simulations for %s (with Boltzmann sampling)..." % (strand_seq))
        
    def getOptions(trials):
         
        o = standardOptions(tempIn=float(form['temperature']), timeOut=A_TIME_OUT) 
        
        o.num_simulations = TRIALS
        hybridization(o, strand_seq, trials)
        o.sodium = form['sodium']
        o.magnesium = form['magnesium']
        o.concentration = 1.0E-9
        
        if "RNA" == form['substrate']:
            o.substrate_type = Literals.substrateRNA
        
        return o
    
    MergeSimSettings.max_trials = MAX_TRIALS
    
    myMultistrand = MergeSim()
    myMultistrand.setOptionsFactory1(getOptions, TRIALS)
    myMultistrand.setTerminationCriteria(REQ_SUCCESS)
    myMultistrand.settings.timeOut = WALL_TIME_TIMEOUT
    myMultistrand.run()
    
    return myMultistrand


def statespace_dissociation(form):
    
    strand_seq = form['sequence']
    
    ''' do not set the initial state -- allow builder to do this '''

    def getOptions(arguments):
         
        o = standardOptions()
        o.simulation_mode = Literals.trajectory
        o.num_simulations = BUILDER_TRIALS

        o.sodium = form['sodium']
        o.magnesium = form['magnesium']
        o.temperature = float(form['temperature'])
        o.simulation_time = BUILDER_TIMEOUT 
        
        if "RNA" == form['substrate']:
            o.substrate_type = Literals.substrateRNA
        
        endComplex = arguments[0]
        
        stopSuccess = StopCondition(Literals.success, [(endComplex, Literals.exact_macrostate, 0)])
        o.stop_conditions = [stopSuccess]
        
        return o
 
    startStates = hybridizationString(strand_seq)
    endState = startStates[-1]
    
    Builder.verbosity = True
    
    myBuilder = Builder(getOptions, [endState[0]])
    
    ''' setting the precision to just 2 states will ensure the builder stops after a single iteration. '''
    startTime = time.time()
    myBuilder.genUntilConvergenceWithInitialState(2 , startStates[:(len(startStates) - 1)])
    buildTime = time.time() - startTime

    bRate = BuilderRate(myBuilder)
    
    return bRate , buildTime


def statespace_threewaybm(form):
    
    return None


def compute(form):

    resultDict = dict()
    
    if form.experiment == "association":

        myMultistrand = first_step_simulation(form)
    
        result = myMultistrand.results
        myTime = myMultistrand.runTime
        nFor = myMultistrand.nForward.value
        nRev = myMultistrand.nReverse.value
        
        k1 = result.k1()
        low, high = result.doBootstrap()
        
        resultDict['rate'] = "{:.2e}".format(float(k1))
        resultDict['myTime'] = "{:.2f}".format(float(myTime))
        resultDict['nFor'] = str(nFor)
        resultDict['nRev'] = str(nRev)
        resultDict['rLow'] = "{:.2e}".format(float(low))
        resultDict['rHigh'] = "{:.2e}".format(float(high))
        resultDict['temp'] = "{:.1f}".format(float(form['temperature']))

    elif form.experiment == "dissociation":
        
        bRate, bTime = statespace_dissociation(form) 
        
        resultDict['rate'] = "{:.2e}".format(bRate.averageTimeFromInitial())
        resultDict['nStates'] = str(bRate.n_states)
        resultDict['nTransitions'] = str(bRate.n_transitions)
        resultDict['buildTime'] = "{:.2f}".format(bTime)
        resultDict['solveTime'] = "{:.2f}".format(bRate.matrixTime)
    
    elif form.experiment == "threewaybm":
        
        myBuilderRate = statespace_threewaybm(form)

        resultDict['rate'] = "1.0"
    
    else:
        raise Exception("Experiment not found")

    return resultDict
