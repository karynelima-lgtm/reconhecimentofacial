const MODEL_URL = 'https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@master/weights';
const THRESHOLD = 0.6;

const statusEl = document.getElementById('status');
const resultBox = document.getElementById('resultBox');
const resultText = document.getElementById('resultText');
const distanceText = document.getElementById('distanceText');
const confidenceText = document.getElementById('confidenceText');
const compareBtn = document.getElementById('compareBtn');

const imageInput1 = document.getElementById('image1');
const imageInput2 = document.getElementById('image2');

const preview1 = document.getElementById('preview1');
const preview2 = document.getElementById('preview2');
const placeholder1 = document.getElementById('placeholder1');
const placeholder2 = document.getElementById('placeholder2');

function setStatus(message, type = 'info') {
  statusEl.textContent = message;
  statusEl.className = `status ${type}`;
}

function renderPreview(inputEl, previewEl, placeholderEl, file) {
  if (!file) {
    previewEl.style.display = 'none';
    placeholderEl.style.display = 'block';
    return;
  }

  const reader = new FileReader();
  reader.onload = (event) => {
    previewEl.src = event.target.result;
    previewEl.style.display = 'block';
    placeholderEl.style.display = 'none';
  };
  reader.readAsDataURL(file);
}

imageInput1.addEventListener('change', (event) => {
  const file = event.target.files[0];
  renderPreview(imageInput1, preview1, placeholder1, file);
});

imageInput2.addEventListener('change', (event) => {
  const file = event.target.files[0];
  renderPreview(imageInput2, preview2, placeholder2, file);
});

async function carregarModelos() {
  if (!window.faceapi) {
    throw new Error('A biblioteca face-api.js não foi carregada.');
  }

  await Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
    faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
    faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  ]);
}

async function extrairDescricao(file) {
  const img = await faceapi.bufferToImage(file);
  const detection = await faceapi
    .detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withFaceDescriptor();

  if (!detection) {
    throw new Error('Nenhum rosto foi detectado na imagem.');
  }

  return detection.descriptor;
}

async function compararImagens() {
  const file1 = imageInput1.files[0];
  const file2 = imageInput2.files[0];

  if (!file1 || !file2) {
    setStatus('Selecione as duas imagens antes de comparar.', 'error');
    return;
  }

  compareBtn.disabled = true;
  resultBox.classList.add('hidden');
  setStatus('Processando imagens e comparando rostos...', 'info');

  try {
    await carregarModelos();

    const descriptor1 = await extrairDescricao(file1);
    const descriptor2 = await extrairDescricao(file2);

    const distance = faceapi.euclideanDistance(descriptor1, descriptor2);
    const samePerson = distance <= THRESHOLD;
    const similarity = Math.max(0, 100 * (1 - distance / 1.5));

    resultText.innerHTML = samePerson
      ? '<span class="same">São a mesma pessoa.</span>'
      : '<span class="different">São pessoas diferentes.</span>';

    distanceText.textContent = `Distância euclidiana: ${distance.toFixed(4)}`;
    confidenceText.textContent = `Similaridade estimada: ${similarity.toFixed(1)}%`;
    resultBox.classList.remove('hidden');

    setStatus(
      samePerson
        ? 'Comparação concluída: rostos semelhantes dentro do limite estabelecido.'
        : 'Comparação concluída: rostos diferentes no limiar atual.',
      samePerson ? 'success' : 'info'
    );
  } catch (error) {
    console.error(error);
    setStatus(error.message || 'Erro ao comparar as imagens.', 'error');
  } finally {
    compareBtn.disabled = false;
  }
}

compareBtn.addEventListener('click', compararImagens);

window.addEventListener('DOMContentLoaded', async () => {
  try {
    await carregarModelos();
    setStatus('Modelos carregados. Você já pode comparar as imagens.', 'success');
  } catch (error) {
    setStatus('Não foi possível carregar os modelos. Verifique sua conexão com a internet.', 'error');
    console.error(error);
  }
});
