import web, time
from call_multistrand import compute
from web import form

urls = (
  '/hybrserv', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

# Defining the buttons. 'id' stands for HTML id of the element.
# #'value' is the value of the button as perceived by Python.
# #'html' is the text displayed in HTML page. 'class_' is HTML class
# modForm = form.Form(
#     form.Textbox('Temp:', id='modMe', value="loaded"),
# )


class Index(object):
    
    def GET(self):
        
        return render.start_form()

    def POST(self):
        
        form_f = web.input(substrate="Nameless job", sequence="AGCGTGA")
        
        if form_f.experiment == "hybridization" and len(form_f.sequence) > 100 or len(form_f.sequence) < 3 :
            form_f.substrate = "Too long"
            return render.errorpage(result=1e-36, form_f=form_f)
        
        if form_f.experiment == "dissociation" and len(form_f.sequence) > 20 or len(form_f.sequence) < 3 :
            form_f.substrate = "Too long"
            return render.errorpage(result=1e-36, form_f=form_f)
        
        if form_f.experiment == "threewaybm" and (len(form_f.sequence) + len(form_f.ltoehold) + len(form_f.rtoehold)) > 50 or len(form_f.sequence) < 3 :
            form_f.substrate = "Too long"
            return render.errorpage(result=1e-36, form_f=form_f)
        
        try:
            result = compute(form_f)

        except Exception as e:
            print str(e)
            form_f.substrate = "Exception"
            return render.errorpage(result=1e-36, form_f=form_f)

        if form_f.experiment == "threewaybm":
            return render.result_threewaybm(result=result, form_f=form_f)
        
        if float(float(result['rate'])) < 10.0 ** -30:
            return render.errorpage(result=1e-36, form_f=form_f)

        if form_f.experiment == "dissociation":
            return render.result_dissociation(result=result, form_f=form_f)

    
        return render.result_association(result=result, form_f=form_f)


if __name__ == "__main__":
    app.run()
