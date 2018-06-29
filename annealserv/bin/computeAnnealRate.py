from multistrand.concurrent import MergeSim
from multistrand.experiment import standardOptions

A_TIME_OUT = 1.0
MAX_SEQ_LEN = 40

class customResult(object):
    
    def __init__(self):
    
        self.thing = 'x'
    
 
def first_step_simulation(strand_seq, trials, T=20.0, material="DNA"):
 
    print ("Running first step mode simulations for %s (with Boltzmann sampling)..." % (strand_seq))
        
    def getOptions(trials, material):
         
        o = standardOptions("First Step", tempIn=25.0, trials=200, timeOut = A_TIME_OUT) 
        hybridization(o, strand_seq, trials)
        
          
        return o
      
    myMultistrand.setOptionsFactory2(getOptions, trials, material)
    myMultistrand.run()
    dataset = myMultistrand.results
 
    
#     myResult =customResult()
#     
#     myResult.k1 =migrationRate(dataset, 50e-9).k1()
#     myResult.runTime = myMultistrand.runTime
    
    return migrationRate(dataset, 50e-9).k1() #, myMultistrand.runTime


def compute(strand_seq):
    
    if len(strand_seq) < MAX_SEQ_LEN:
        result = first_step_simulation(strand_seq, 200, T=25.0, material="DNA")
    else:
        result = 10 ** - 99
    

    return "{:.2e}".format(float(result.k1)), '999.0'
