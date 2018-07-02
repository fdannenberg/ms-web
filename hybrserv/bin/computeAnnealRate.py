from multistrand.concurrent import Literals, MergeSim, MergeSimSettings
from multistrand.experiment import standardOptions, hybridization

A_TIME_OUT = 4.0
MAX_TRIALS = 20000
WALL_TIME_TIMEOUT = 30

REQ_SUCCESS = 24
TRIALS = 100

    
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
    
#     print myMultistrand.results
    
    return myMultistrand


def statespace_dissociation(form):
    
    return None


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
        
        myBuilderRate = statespace_dissociation(form)
        
        resultDict['rate'] = "1.0"
    
    elif form.experiment == "threewaybm":
        
        myBuilderRate = statespace_threewaybm(form)

        resultDict['rate'] = "1.0"
    
    else:
        raise Exception("Experiment not found")

    return resultDict
