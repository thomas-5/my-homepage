from flask import Flask, render_template, request, session
from model import *
from utilities import *
import io
import sys
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 

@app.route('/')
def linear_program_solver_home():
    form_data = session.get('form_data', {})
    return render_template('lp-solver.html', form_data=form_data)

@app.route('/submit', methods=['POST'])
def solve_linear_program():
    # Retrieve form data
    form_data = {
        'constraint-matrix-A': request.form.get('constraint-matrix-A'),
        'constraint-vector-b': request.form.get('constraint-vector-b'),
        'objective-vector-cT': request.form.get('objective-vector-cT'),
        'objective-constant-z': request.form.get('objective-constant-z'),
        'problem-type': request.form.get('problem-type'),
        'show-phase-one-detail': request.form.get('show-phase-one-detail'),
        'show-canonical': request.form.get('show-canonical'),
        'starting-basis': request.form.get('starting-basis')
    }
    session['form_data'] = form_data
    
    A = convert_str_to_array(form_data['constraint-matrix-A'])
    b = convert_str_to_array(form_data['constraint-vector-b'])
    cT = convert_str_to_array(form_data['objective-vector-cT'])
    z = convert_str_to_array(form_data['objective-constant-z'])
   
    output = io.StringIO()
    sys.stdout = output
    
    print(f"form_data: {form_data}")
    
    captured_output = output.getvalue()
    sys.stdout = sys.__stdout__
    
    response = render_template('lp-solver.html', result=True, output=captured_output, form_data=form_data)
    return response


if __name__ == "__main__":
    app.run(port=5001)