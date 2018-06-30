from multistrand.concurrent import MergeSim, MergeSimSettings
from multistrand.experiment import standardOptions, hybridization

A_TIME_OUT = 1.0
MAX_TRIALS = 200000

# class customResult(object):
#     
#     def __init__(self):
#     
#         self.thing = 'x'
    
def first_step_simulation(strand_seq, successC, T=20.0, material="DNA"):
 
    print ("Running first step mode simulations for %s (with Boltzmann sampling)..." % (strand_seq))
        
    def getOptions(trials, material):
         
        o = standardOptions(tempIn=25.0, trials=200, timeOut = A_TIME_OUT) 
        hybridization(o, strand_seq, trials)
        
        return o
    
    MergeSimSettings.max_trials = MAX_TRIALS
    
    myMultistrand = MergeSim()
    myMultistrand.setOptionsFactory2(getOptions, 60, material)
    myMultistrand.setTerminationCriteria(successC)
    myMultistrand.run()
    
    print myMultistrand.results
    
    return (myMultistrand.results.kEff(concentration = 10 ** -9) , myMultistrand.runTime)


def compute(strand_seq, materialIn=None):
    
    result, myTime = first_step_simulation(strand_seq, 24, T=25.0, material=materialIn)

    return "{:.2e}".format(float(result)), "{:.2f}".format(float(myTime))
