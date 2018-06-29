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
        
        form = web.input(name="Nameless job", sequence="AGCGTGA")

        form.result = compute(form.sequence )

        return render.index(greeting = form.sequence, greeting2 = form.name, result = form.result[0], computeTime=form.result[1])
        

if __name__ == "__main__":
    app.run()