window.onload = function() {
    MathJax.Hub.Typeset();
    updatePreview();
    updateDisplay();
};

const simplexRadio = document.getElementById('simplex');
const twoPhaseRadio = document.getElementById('two-phase-simplex');
const phase1Details= document.getElementById('phase1-details');
const startingBasis = document.getElementById('starting-basis');
const inputIds = ['matrix-A', 'vector-b', 'vector-cT', 'constant-z'];


simplexRadio.addEventListener('change', updateDisplay);
twoPhaseRadio.addEventListener('change', updateDisplay);

inputIds.forEach((inputId) => {
    const inputElement = document.getElementById(inputId);
    inputElement.addEventListener('change', updatePreview);
  });


function updateDisplay() {
    if (simplexRadio.checked) {
        phase1Details.style.display = 'none';
        startingBasis.style.display = 'block';
    } else if (twoPhaseRadio.checked) {
        phase1Details.style.display = 'block';
        startingBasis.style.display = 'none';
    }
}

function updatePreview() {
    var A = document.getElementById('matrix-A').value;
    var b = document.getElementById('vector-b').value;
    var cT = document.getElementById('vector-cT').value;
    var z = document.getElementById('constant-z').value;
    A = matrixToLatex(A);
    b = matrixToLatex(b);
    cT = matrixToLatex(cT);
    if (A == "Invalid Matrix" || b == "Invalid Matrix" || cT == "Invalid Matrix"){
        var output = document.getElementById('preview-box');
        output.textContent = "Invalid Input";
        return;
    }
    if (z === "0"){
        var input = "\\text{max }" + cT + "x\\\\" + "\\text{s.t.}" + A + "x=" + b + "\\\\x" + "\\ge 0";
    } else {
        var input = "\\text{max }" + cT + "x+" + z + "\\\\" + "\\text{s.t.}" + A + "x=" + b + "\\\\x" + "\\ge 0";
    }
    console.log(input)
    var output = document.getElementById('preview-box');
    output.textContent = input;
    output.innerHTML = "\\(" + input + "\\)";
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, output]);
    return;
}

// Utilities
function matrixToLatex(matrixStr) {
    // Convert the string to a matrix array
    try {
        var matrix = JSON.parse(matrixStr);
        var rows = matrix.length;
        var columns = matrix[0].length;
        var isVector = columns === undefined;
    } catch (error){
        return "Invalid Matrix";
    }

    var latex = "\\begin{pmatrix}\n";

    if (isVector){
        for (var i = 0; i < rows; i++){
            latex += matrix[i];
            if (i !== rows - 1) {
                latex += " & ";
            }
        }
    } else {
        for (var i = 0; i < rows; i++) {
            for (var j = 0; j < columns; j++) {
            latex += matrix[i][j];
            if (j !== columns - 1) {
                latex += " & ";
            }
            }
            if (i !== rows - 1) {
            latex += " \\\\\n";
            }
        }
    }
    latex += "\\end{pmatrix}";
    console.log(latex);
    return latex;
}

