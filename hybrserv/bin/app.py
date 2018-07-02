import web, time
from computeAnnealRate import compute

urls = (
  '/hybrserv', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

MAX_SEQ_LEN = 100


class Index(object):
    
    def GET(self):
        return render.start_form()

    def POST(self):
        
        form = web.input(substrate="Nameless job", sequence="AGCGTGA")
        
        if len(form.sequence) > MAX_SEQ_LEN or len(form.sequence) < 3 :
            return render.errorpage(result=1e-36, form=form)
        
        try:
            result = compute(form)

        except Exception as e:
            print str(e)
            form.substrate = "Exception"
            return render.errorpage(result=1e-36, form=form)

        if float(float(result['rate'])) < 10.0 ** -30:
            return render.errorpage(result=1e-36, form=form)
        
        return render.resultpage(result=result, form=form)


if __name__ == "__main__":

    app.run()
