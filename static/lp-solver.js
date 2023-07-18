window.onload = function() {
    MathJax.Hub.Typeset();
};

const simplexRadio = document.getElementById('simplex');
const twoPhaseRadio = document.getElementById('two-phase-simplex');
const phase1Details= document.getElementById('phase1-details');
const startingBasis = document.getElementById('starting-basis');

simplexRadio.addEventListener('change', function() {
    phase1Details.style.display = 'none';
    startingBasis.style.display = 'block';
});

twoPhaseRadio.addEventListener('change', function() {
    phase1Details.style.display = 'block';
    startingBasis.style.display = 'none';
});