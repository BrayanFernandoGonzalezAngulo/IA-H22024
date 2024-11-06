let diseases = {};
let currentSymptoms = [];
let symptomIndex = 0;
let score = {};

// Cargar datos del JSON
fetch('data.json')
  .then(response => response.json())
  .then(data => {
    diseases = data;
    initialize();
  });

function initialize() {
  // Inicializar el puntaje de cada enfermedad en 0
  for (let disease in diseases) {
    score[disease] = 0;
  }
  nextSymptom();
}

function nextSymptom() {
  // Tomar un síntoma de cada enfermedad
  const diseaseNames = Object.keys(diseases);
  currentSymptoms = [];
  
  for (let disease of diseaseNames) {
    const symptoms = diseases[disease];
    if (symptomIndex < symptoms.length) {
      currentSymptoms.push({ disease, symptom: symptoms[symptomIndex] });
    }
  }
  
  if (currentSymptoms.length > 0) {
    document.getElementById('question').innerText = `¿Tienes este síntoma? ${currentSymptoms[0].symptom}`;
  } else {
    showResults();
  }
}

function answer(response) {
  if (response === 'yes') {
    for (let item of currentSymptoms) {
      score[item.disease]++;
    }
  }
  
  symptomIndex++;
  nextSymptom();
}

function showResults() {
  // Calcular porcentaje para cada enfermedad
  let results = [];
  
  for (let disease in score) {
    const totalSymptoms = diseases[disease].length;
    const matchPercentage = ((score[disease] / totalSymptoms) * 100).toFixed(2);
    results.push({ disease, matchPercentage });
  }
  
  // Ordenar resultados y mostrar las tres enfermedades más probables
  results.sort((a, b) => b.matchPercentage - a.matchPercentage);
  const top3 = results.slice(0, 3);
  
  const resultText = top3.map(result => 
    `${result.disease}: ${result.matchPercentage}%`).join('<br>');
  
  document.getElementById('results').innerHTML = resultText;
  document.getElementById('question-container').style.display = 'none';
  document.getElementById('result-container').style.display = 'block';
}
