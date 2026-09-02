const MODEL_URL = 'https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@master/weights';
const THRESHOLD = 0.6;

const modelSelect = document.getElementById('modelSelect');
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

const DETECTOR_CONFIGS = {
  tinyFaceDetector: {
    label: 'Tiny Face Detector',
    load: () => faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
    options: () => new faceapi.TinyFaceDetectorOptions({ inputSize: 416, scoreThreshold: 0.5 }),
  },
  ssdMobilenetv1: {
    label: 'SSD Mobilenet V1',
    load: () => faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),
    options: () => new faceapi.SsdMobilenetv1Options({ minConfidence: 0.5 }),
  },
};

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

  const modeloSelecionado = modelSelect.value;
  const config = DETECTOR_CONFIGS[modeloSelecionado] || DETECTOR_CONFIGS.tinyFaceDetector;

  await Promise.all([
    config.load(),
    faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
    faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  ]);
}

function getDetectorOptions() {
  const modeloSelecionado = modelSelect.value;
  const config = DETECTOR_CONFIGS[modeloSelecionado] || DETECTOR_CONFIGS.tinyFaceDetector;
  return config.options();
}

async function extrairDescricao(file) {
  const img = await faceapi.bufferToImage(file);
  const detection = await faceapi
    .detectSingleFace(img, getDetectorOptions())
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
    const modeloSelecionado = modelSelect.value;
    const config = DETECTOR_CONFIGS[modeloSelecionado] || DETECTOR_CONFIGS.tinyFaceDetector;

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
      `${config.label} selecionado. ${samePerson ? 'Comparação concluída: rostos semelhantes dentro do limite estabelecido.' : 'Comparação concluída: rostos diferentes no limiar atual.'}`,
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
  modelSelect.addEventListener('change', async () => {
    setStatus(`Modelo selecionado: ${DETECTOR_CONFIGS[modelSelect.value].label}. Recarregando recursos...`, 'info');
    try {
      await carregarModelos();
      setStatus(`Modelo carregado: ${DETECTOR_CONFIGS[modelSelect.value].label}. Você já pode comparar as imagens.`, 'success');
    } catch (error) {
      setStatus('Não foi possível carregar os modelos selecionados. Verifique sua conexão com a internet.', 'error');
      console.error(error);
    }
  });

  try {
    await carregarModelos();
    setStatus(`Modelo carregado: ${DETECTOR_CONFIGS[modelSelect.value].label}. Você já pode comparar as imagens.`, 'success');
  } catch (error) {
    setStatus('Não foi possível carregar os modelos. Verifique sua conexão com a internet.', 'error');
    console.error(error);
  }
});
