from django.shortcuts import render
from .forms import UploadDFDFileForm
from .scripts.img_test import *
from pytm import TM
import pydot
import subprocess

# base editor view
def editor(request):
    generate() # generate random color cat picture
    return render(request, "pytm_web/editor.html")

# view for uploading file
def upload_file(request):
    # checks to see if request method is POST which means form is submitted
    if request.method == 'POST':
        # request.POST has form data, request.FILE has file data
        form = UploadDFDFileForm(request.POST, request.FILES)
        
        # this is a BytesIO stream
        # equivalently, this is a .py file containing the instructions to
        #   create a TM object in pytm
        tm_file = request.FILES['inputFile'].file
        DIR = os.path.dirname(__file__)
        with open(os.path.join(DIR, 'scripts', 'tm.py'), "wb") as f:
            f.write(tm_file.read())
        
        from .scripts.tm import out_tm
        # NOTE: for the time being, the TM object you create in your uploaded
        # .py file MUST BE CALLED out_tm EXACTLY to be recognized by our
        # prototype. TODO: how can we change this?

        svg = out_tm.dfd()
        print(type(svg))
        
        testdot = "strict graph {\n a -- b \n  a -- b \n  b -- a [color=blue]}"

        with open(os.path.join(DIR, 'static', 'dfd.dot'), "w") as f:
            f.write(svg)
            
        # (graph,) = pydot.graph_from_dot_file(os.path.join(DIR, 'static', 'dfd.dot'))
        graphs = pydot.graph_from_dot_data(svg)
        graphs.write_png('somefile.png')

        

        # (graph, ) = pydot.graph_from_dot_file(out_tm.process().dfd())
        # graph.write_png(os.path.join(DIR, 'static', 'tm.png'))
        
        if form.is_valid():
            # process file
            return render(request, 'pytm_web/upload.html', {'form': form, 'svg': svg})
    else:
            # if request method is not POST, make an empty form
        form = UploadDFDFileForm()
            # renders template upload.html, passing in the form
            # NEED TO IMPLEMENT upload.html TEMPLATE
    return render(request, 'pytm_web/upload.html', {'form': form})

################################################################################

# helper to convert a BytesIO to a TM object
# def process_tm_file(file, model_name="Threat Model"):
#     tm = TM(model_name)

#     return tm