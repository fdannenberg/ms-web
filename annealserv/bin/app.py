import web
from computeAnnealRate import compute

urls = (
  '/annealserv', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class Index(object):
    def GET(self):
        return render.start_form()

    def POST(self):
        
        form = web.input(substrate="Nameless job", sequence="AGCGTGA")

        try:
            form.result = compute(form.sequence, form.substrate )
            return render.index(greeting = form.sequence, substrate = form.substrate, result = form.result[0], computeTime=form.result[1])

        except ValueError:
            return render.errorpage(sequence = form.sequence)
        

if __name__ == "__main__":
    app.run()