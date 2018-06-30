import web
from computeAnnealRate import compute

urls = (
  '/annealserv', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

MAX_SEQ_LEN = 16


class Index(object):
    def GET(self):
        return render.start_form()

    def POST(self):
        
        form = web.input(substrate="Nameless job", sequence="AGCGTGA")

        if len(form.sequence) > MAX_SEQ_LEN:
            return render.errorpage(greeting = form.sequence, substrate = "-", result = 1e-36, computeTime=999.0)
        try:
            form.result = compute(form.sequence, form.substrate )

        except Exception as e:
            return render.errorpage(greeting = form.sequence, substrate = form.substrate, result = 1e-36, computeTime=999.0)

        if float(form.result[0]) < 10.0 ** -30:
            return render.errorpage(greeting = form.sequence, substrate = form.substrate, result = 1e-36, computeTime=999.0)
        
        
        return render.index(greeting = form.sequence, substrate = form.substrate, result = form.result[0], computeTime=form.result[1])

if __name__ == "__main__":
    app.run()