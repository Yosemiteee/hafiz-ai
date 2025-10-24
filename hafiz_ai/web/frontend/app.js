const passageSelect = document.getElementById('passage-select');
const passageContent = document.getElementById('passage-content');
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');
const transcriptText = document.getElementById('transcript-text');
const speechStatus = document.getElementById('speech-status');
const manualInput = document.getElementById('manual-input');
const manualSubmit = document.getElementById('manual-submit');
const accuracyLabel = document.getElementById('accuracy');
const suggestionsPanel = document.getElementById('feedback-suggestions');
const missingList = document.getElementById('missing-words');
const extraList = document.getElementById('extra-words');
const mispronouncedList = document.getElementById('mispronounced-words');

const state = {
  passages: [],
  selectedPassage: null,
  recognition: null,
  transcript: '',
  debounceTimer: null,
};

async function fetchPassages() {
  const response = await fetch('/api/v1/passages');
  if (!response.ok) {
    throw new Error('Pasaj listesi alınamadı');
  }
  const data = await response.json();
  state.passages = data;
  renderPassageOptions();
  if (data.length > 0) {
    selectPassage(data[0].id);
  }
}

function renderPassageOptions() {
  passageSelect.innerHTML = '';
  state.passages.forEach((passage) => {
    const option = document.createElement('option');
    option.value = passage.id;
    option.textContent = `${passage.surah} (${passage.ayah_range})`;
    passageSelect.appendChild(option);
  });
}

function selectPassage(passageId) {
  const passage = state.passages.find((item) => item.id === passageId);
  if (!passage) return;
  state.selectedPassage = passage;
  passageContent.innerHTML = `
    <h3>${passage.surah} <span>(${passage.ayah_range})</span></h3>
    <p class="arabic">${passage.arabic_text}</p>
    <p class="transliteration">${passage.transliteration}</p>
    <p class="translation">${passage.translation_tr}</p>
  `;
  evaluateTranscript(state.transcript);
}

async function evaluateTranscript(transcript) {
  if (!transcript || !state.selectedPassage) {
    updateFeedback(null);
    return;
  }
  const payload = {
    passage_id: state.selectedPassage.id,
    transcript,
  };
  try {
    const response = await fetch('/api/v1/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error('Değerlendirme başarısız oldu');
    }
    const data = await response.json();
    updateFeedback(data);
  } catch (error) {
    console.error(error);
  }
}

function updateFeedback(result) {
  if (!result) {
    accuracyLabel.textContent = '';
    suggestionsPanel.innerHTML = '<p>Henüz analiz yapılmadı.</p>';
    [missingList, extraList, mispronouncedList].forEach((list) => (list.innerHTML = ''));
    return;
  }

  accuracyLabel.textContent = `Doğruluk: ${result.accuracy_score.toFixed(1)}%`;
  suggestionsPanel.innerHTML = '';

  result.suggestions.forEach((suggestion) => {
    const p = document.createElement('p');
    p.textContent = suggestion;
    suggestionsPanel.appendChild(p);
  });

  renderChipList(missingList, result.missing_words);
  renderChipList(extraList, result.extra_words);
  renderChipList(mispronouncedList, result.mispronounced_words);
}

function renderChipList(element, items) {
  element.innerHTML = '';
  if (!items || items.length === 0) {
    const empty = document.createElement('li');
    empty.textContent = '—';
    empty.classList.add('muted');
    element.appendChild(empty);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    element.appendChild(li);
  });
}

function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    speechStatus.textContent = 'Tarayıcınız gerçek zamanlı tanımayı desteklemiyor';
    speechStatus.classList.remove('offline');
    speechStatus.classList.add('warning');
    return;
  }

  state.recognition = new SpeechRecognition();
  state.recognition.lang = 'ar-SA';
  state.recognition.interimResults = true;
  state.recognition.continuous = true;

  state.recognition.onstart = () => {
    speechStatus.textContent = 'Dinliyor';
    speechStatus.classList.remove('offline');
    speechStatus.classList.add('online');
  };

  state.recognition.onend = () => {
    speechStatus.textContent = 'Mikrofon Kapalı';
    speechStatus.classList.remove('online');
    speechStatus.classList.add('offline');
    startButton.disabled = false;
    stopButton.disabled = true;
  };

  state.recognition.onerror = (event) => {
    console.error('Speech recognition error', event);
  };

  state.recognition.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      const transcript = event.results[i][0].transcript.trim();
      if (event.results[i].isFinal) {
        finalTranscript += `${transcript} `;
      } else {
        interimTranscript += `${transcript} `;
      }
    }

    state.transcript = `${state.transcript} ${finalTranscript}`.trim();
    const displayText = `${state.transcript} ${interimTranscript}`.trim();
    transcriptText.textContent = displayText;
    scheduleEvaluation(state.transcript);
  };
}

function scheduleEvaluation(transcript) {
  if (state.debounceTimer) {
    clearTimeout(state.debounceTimer);
  }
  state.debounceTimer = setTimeout(() => {
    evaluateTranscript(transcript);
  }, 600);
}

startButton.addEventListener('click', () => {
  if (!state.recognition) {
    setupSpeechRecognition();
  }
  if (!state.recognition) {
    return;
  }
  state.transcript = '';
  transcriptText.textContent = '';
  startButton.disabled = true;
  stopButton.disabled = false;
  state.recognition.start();
});

stopButton.addEventListener('click', () => {
  if (!state.recognition) return;
  state.recognition.stop();
  evaluateTranscript(state.transcript);
});

passageSelect.addEventListener('change', (event) => {
  selectPassage(event.target.value);
});

manualSubmit.addEventListener('click', () => {
  const text = manualInput.value.trim();
  transcriptText.textContent = text;
  state.transcript = text;
  evaluateTranscript(text);
});

fetchPassages().catch((error) => {
  console.error(error);
});

setupSpeechRecognition();
