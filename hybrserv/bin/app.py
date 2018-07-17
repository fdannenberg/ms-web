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

SERVER_NAME = "HybrServ v0.14"
DISCLAIMER = "    Hybridization rate computation is based on First Step Mode. The computation ends when N successful trajectories are found or after max(N,30) seconds, whichever occurs earlier. The maximum sequence length is 100 nt.  Dissociation and toehold-mediated branch migration rate computation is based on an unpublished rare event simulation method. The simulation starts 5*N trials with timeout 3.0 ms along each point in a predetermined pathway. The computation time is unrestricted.  Dissociation: The maximum sequence length is 20 nt. Threeway branch migration: The sum of sequence lengths should be less than 50 nt.  "

WEB_TEXT = dict()
WEB_TEXT['title'] = SERVER_NAME
WEB_TEXT['disclaimer'] = DISCLAIMER


class Index(object):
    
    def GET(self):
        
        return render.start_form(WEB_TEXT)

    def POST(self):
        
        form_f = web.input(substrate="Nameless job", sequence="AGCGTGA")
        
        if form_f.experiment == "hybridization" and len(form_f.sequence) > 100 or len(form_f.sequence) < 3 :
            form_f.substrate = "Length requirements not met"
            return render.errorpage(1e-36, form_f, WEB_TEXT)
        
        if form_f.experiment == "dissociation" and len(form_f.sequence) > 20 or len(form_f.sequence) < 3 :
            form_f.substrate = "Length requirements not met"
            return render.errorpage(1e-36, form_f, WEB_TEXT)
        
        if form_f.experiment == "threewaybm" and (len(form_f.sequence) + len(form_f.ltoehold) + len(form_f.rtoehold)) > 50 or len(form_f.sequence) < 3 :
            form_f.substrate = "Length requirements not met"
            return render.errorpage(1e-36, form_f, WEB_TEXT)
        
        try:
            result = compute(form_f)

        except Exception as e:
            print str(e)
            form_f.substrate = "Exception"
            return render.errorpage(1e-36, form_f, WEB_TEXT)

        if form_f.experiment == "threewaybm":
            return render.result_threewaybm(result, form_f, WEB_TEXT)
        
        if float(float(result['rate'])) < 10.0 ** -30:
            return render.errorpage(1e-36, form_f, WEB_TEXT)

        if form_f.experiment == "dissociation":
            return render.result_dissociation(result, form_f, WEB_TEXT)
    
        return render.result_association(result, form_f, WEB_TEXT)


if __name__ == "__main__":
    app.run()
