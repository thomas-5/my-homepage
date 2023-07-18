from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def linear_program_solver_home():
    return render_template('lp-solver.html')

@app.route('/submit', methods=['POST'])
def handle_form_submission():
    # Retrieve form data
    A = request.form.get('constraint-matrix-A')
    b = request.form.get('constraint-vector-b')
    cT = request.form.get('objective-vector-cT')
    z = request.form.get('objective-constant-z')
    
    result = False
    if A == "1":
        result = True
        
    # Return a response
    return render_template('lp-solver.html', result=result)


if __name__ == "__main__":
    app.run(port=5001)