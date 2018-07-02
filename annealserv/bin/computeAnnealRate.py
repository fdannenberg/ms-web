from multistrand.concurrent import MergeSim, MergeSimSettings
from multistrand.experiment import standardOptions, hybridization

A_TIME_OUT = 2.0
MAX_TRIALS = 20000
WALL_TIME_TIMEOUT = 30

    
def first_step_simulation(strand_seq, successC, T=20.0, material="DNA"):
 
    print ("Running first step mode simulations for %s (with Boltzmann sampling)..." % (strand_seq))
        
    def getOptions(trials, material):
         
        o = standardOptions(tempIn=25.0, trials=200, timeOut=A_TIME_OUT) 
        hybridization(o, strand_seq, trials)
        
        return o
    
    MergeSimSettings.max_trials = MAX_TRIALS
    
    myMultistrand = MergeSim()
    myMultistrand.setOptionsFactory2(getOptions, 60, material)
    myMultistrand.setTerminationCriteria(successC)
    myMultistrand.settings.timeOut = WALL_TIME_TIMEOUT
    myMultistrand.run()
    
    print myMultistrand.results
    
    return myMultistrand
#     return (myMultistrand.results , myMultistrand.runTime, myMultistrand.nForward.value, myMultistrand.nReverse.value)


def compute(strand_seq, materialIn=None):
    
    myMultistrand = first_step_simulation(strand_seq, 24, T=25.0, material=materialIn)

    result = myMultistrand.results
    myTime = myMultistrand.runTime
    nFor = myMultistrand.nForward.value
    nRev = myMultistrand.nReverse.value
    
    k1 = result.k1()
    low, high = result.doBootstrap()

    return "{:.2e}".format(float(k1)), "{:.2f}".format(float(myTime)), str(nFor), str(nRev)
