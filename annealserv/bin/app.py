import web, time
from computeAnnealRate import compute

urls = (
  '/annealserv', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

MAX_SEQ_LEN = 32


class Index(object):
    
    prev_time = -99999.9
    computedRates = 0
    
    def GET(self):
        return render.start_form()

    def POST(self):
        
        form = web.input(substrate="Nameless job", sequence="AGCGTGA")
                
        if len(form.sequence) > MAX_SEQ_LEN or len(form.sequence) < 3 :
            return render.errorpage(greeting=form.sequence, substrate=form.substrate, result=1e-36, computeTime=999.0, nFor=0, nRev=0)
        
        if (time.time() - self.prev_time) < 8.0:
            return render.errorpage(greeting="Please do not submit jobs this quickly!", substrate=form.substrate, result=1e-36, computeTime=999.0, nFor=0, nRev=0)
        
        try:
#             self.prev_time = time.time()
            form.result = compute(form.sequence, form.substrate)
#             self.computedRates = self.computedRates + 1
#             print "Rates computes = " + str(self.computedRates) + "\n"

        except Exception as e:
            print str(e)
            return render.errorpage(greeting=form.sequence, substrate="Exception", result=1e-36, computeTime=999.0, nFor=0, nRev=0)

        if float(form.result[0]) < 10.0 ** -30:
            return render.errorpage(greeting=form.sequence, substrate=form.substrate, result=1e-36, computeTime=999.0, nFor=0, nRev=0)
        
        return render.index(greeting=form.sequence, substrate=form.substrate, result=form.result[0], computeTime=form.result[1], nFor=form.result[2], nRev=form.result[3])


if __name__ == "__main__":

    app.run()
