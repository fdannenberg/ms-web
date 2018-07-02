import web, time
from computeAnnealRate import compute

urls = (
  '/annealserv', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

MAX_SEQ_LEN = 80


class Index(object):
    
#     computedRates = 0
    
    def GET(self):
        return render.start_form()

    def POST(self):
        
        form = web.input(substrate="Nameless job", sequence="AGCGTGA")
                
        if len(form.sequence) > MAX_SEQ_LEN or len(form.sequence) < 3 :
            return render.errorpage(sequence=form.sequence, substrate=form.substrate, result=1e-36)
        
#         if (time.time() - prev_time) < 8.0:
#             return render.errorpage(greeting="Please do not submit jobs this quickly!", substrate=form.substrate, result=1e-36)
        
        try:
            form.result = compute(form.sequence, form.substrate)
#             self.computedRates = self.computedRates + 1
#             print "Rates computes = " + str(self.computedRates) + "\n"

        except Exception as e:
            print str(e)
            return render.errorpage(sequence=form.sequence, substrate="Exception", result=1e-36)

        if float(float(form.result['rate'])) < 10.0 ** -30:
            return render.errorpage(sequence=form.sequence, substrate=form.substrate, result=1e-36)
        
        return render.index(sequence=form.sequence, substrate=form.substrate, result=form.result)


if __name__ == "__main__":

    app.run()
