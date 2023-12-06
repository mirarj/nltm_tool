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
        # create a TM object in pytm
        tm_file = request.FILES['inputFile'].file
        DIR = os.path.dirname(__file__)
        with open(os.path.join(DIR, 'scripts', 'tm.py'), "wb") as f:
            f.write(tm_file.read())
    
        # run /mnt/c/Users/miraj/Desktop/study/capstone/ntmt_github/pytm_web/scripts/tm.py --dfd | dot -Tpng -o sample.png
        
        ps = subprocess.Popen((os.path.join(DIR, 'scripts', 'tm.py'), '--dfd'), stdout=subprocess.PIPE)
        output = subprocess.check_output(('dot', '-Tpng', '-o', os.path.join(DIR, 'static', 'out.png')), stdin=ps.stdout)
        svg = out_tm.dfd()

        
        if form.is_valid():
            # process file
            return render(request, 'pytm_web/upload.html', {'form': form})
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