const API_BASE = "http://localhost:8000";

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let selectedLang = "english";
let currentAudioUrl = null;

const micBtn = document.getElementById("micBtn");
const micLabel = document.getElementById("micLabel");
const waveContainer = document.getElementById("waveContainer");
const transcriptionText = document.getElementById("transcriptionText");
const translationText = document.getElementById("translationText");
const translationLabel = document.getElementById("translationLabel");
const playBtn = document.getElementById("playBtn");
const audioPlayer = document.getElementById("audioPlayer");
const statusEl = document.getElementById("status");

document.querySelectorAll(".lang-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".lang-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedLang = btn.dataset.lang;
    translationLabel.textContent =
      selectedLang === "mandarin" ? "Tradução (Mandarim)" : "Tradução (Inglês)";
  });
});

micBtn.addEventListener("click", async () => {
  if (isRecording) {
    stopRecording();
  } else {
    await startRecording();
  }
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = handleRecordingStop;
    mediaRecorder.start();

    isRecording = true;
    micBtn.classList.add("recording");
    micLabel.textContent = "Clique para parar";
    waveContainer.classList.add("active");
    setStatus("Gravando...");
  } catch (err) {
    setStatus("Permissão de microfone negada.");
  }
}

function stopRecording() {
  if (mediaRecorder) {
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(t => t.stop());
  }
  isRecording = false;
  micBtn.classList.remove("recording");
  micBtn.classList.add("loading");
  micLabel.textContent = "Processando...";
  waveContainer.classList.remove("active");
}

async function handleRecordingStop() {
  const blob = new Blob(audioChunks, { type: "audio/wav" });
  await sendAudio(blob);
}

async function sendAudio(blob) {
  setStatus("Transcrevendo e traduzindo...");
  playBtn.style.display = "none";

  const formData = new FormData();
  formData.append("audio", blob, "recording.wav");
  formData.append("target_language", selectedLang);

  try {
    const response = await fetch(`${API_BASE}/translate`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Erro no servidor");
    }

    const data = await response.json();

    transcriptionText.textContent = data.transcription || "—";
    translationText.textContent = data.translation || "—";
    currentAudioUrl = `${API_BASE}${data.audio_url}`;
    playBtn.style.display = "block";
    setStatus("Pronto!");

  } catch (err) {
    setStatus(`${err.message}`);
    transcriptionText.textContent = "Erro ao processar.";
    translationText.textContent = "—";
  } finally {
    micBtn.classList.remove("loading");
    micLabel.textContent = "Clique para falar";
  }
}

playBtn.addEventListener("click", () => {
  if (currentAudioUrl) {
    audioPlayer.src = currentAudioUrl;
    audioPlayer.play();
    setStatus("Reproduzindo tradução...");
    audioPlayer.onended = () => setStatus("Pronto!");
  }
});

function setStatus(msg) {
  statusEl.textContent = msg;
}