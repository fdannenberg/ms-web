import web, time
from call_multistrand import compute

urls = (
  '/hybrserv', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')


class Index(object):
    
    def GET(self):
        return render.start_form()

    def POST(self):
        
        form = web.input(substrate="Nameless job", sequence="AGCGTGA")
        
        if form.experiment == "hybridization" and len(form.sequence) > 100 or len(form.sequence) < 3 :
            return render.errorpage(result=1e-36, form=form)
        
        if form.experiment == "dissociation" and len(form.sequence) > 20 or len(form.sequence) < 3 :
            return render.errorpage(result=1e-36, form=form)
        
        try:
            result = compute(form)

        except Exception as e:
            print str(e)
            form.substrate = "Exception"
            return render.errorpage(result=1e-36, form=form)

        if float(float(result['rate'])) < 10.0 ** -30:
            return render.errorpage(result=1e-36, form=form)

        if form.experiment == "dissociation":
            return render.result_dissociation(result=result, form=form)

        if form.experiment == "threewaybm":
            return render.result_threewaybm(result=result, form=form)
    
        return render.result_association(result=result, form=form)
        

if __name__ == "__main__":

    app.run()
