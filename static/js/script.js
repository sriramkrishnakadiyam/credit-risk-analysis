/**
 * Credit Risk Classification — Client-side JavaScript
 * Form validation and UI enhancements
 */

document.addEventListener('DOMContentLoaded', () => {
    // ── Bootstrap form validation & safe submission ───────────
    const form = document.getElementById('predictionForm');
    const alertBox = document.getElementById('validationAlert');

    if (form) {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');

                if (alertBox) {
                    alertBox.classList.remove('d-none');
                }

                // Smooth scroll to the first invalid field and focus it
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
                return false;
            }

            // Valid form: hide any error alert
            if (alertBox) {
                alertBox.classList.add('d-none');
            }

            // Show loading spinner safely without cancelling submission
            const btn = document.getElementById('submitBtn');
            if (btn) {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Classifying Risk…';
                btn.style.pointerEvents = 'none';
                setTimeout(() => {
                    btn.disabled = true;
                }, 100);
            }
        });

        // Hide alert box when user edits an input
        form.addEventListener('input', () => {
            if (form.checkValidity() && alertBox) {
                alertBox.classList.add('d-none');
            }
        });
        form.addEventListener('change', () => {
            if (form.checkValidity() && alertBox) {
                alertBox.classList.add('d-none');
            }
        });
    }

    // ── Quick Fill Sample Data for Testing ────────────────────
    window.fillSampleData = function(type) {
        const samples = {
            low: {
                duration_months: 12,
                credit_amount: 1500,
                installment_rate: "2",
                purpose: "A43",
                num_existing_credits: "1",
                status_checking_account: "A13",
                credit_history: "A32",
                savings_account: "A64",
                other_installment_plans: "A143",
                other_debtors: "A101",
                age: 38,
                personal_status_sex: "A93",
                num_dependents: "1",
                telephone: "A192",
                foreign_worker: "A202",
                employment_since: "A75",
                job: "A173",
                property: "A121",
                housing: "A152",
                residence_since: "4",
            },
            high: {
                duration_months: 48,
                credit_amount: 9500,
                installment_rate: "4",
                purpose: "A40",
                num_existing_credits: "2",
                status_checking_account: "A11",
                credit_history: "A33",
                savings_account: "A61",
                other_installment_plans: "A141",
                other_debtors: "A101",
                age: 23,
                personal_status_sex: "A92",
                num_dependents: "1",
                telephone: "A191",
                foreign_worker: "A201",
                employment_since: "A71",
                job: "A171",
                property: "A124",
                housing: "A151",
                residence_since: "1",
            }
        };

        const data = samples[type] || samples.low;
        for (const [key, val] of Object.entries(data)) {
            const el = document.getElementById(key);
            if (el) {
                el.value = val;
                el.dispatchEvent(new Event('change'));
            }
        }

        if (form) {
            form.classList.remove('was-validated');
        }
        if (alertBox) {
            alertBox.classList.add('d-none');
        }
    };

    // ── Animate progress bars on result page ───────────────────
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = target;
        }, 300);
    });

    // ── Animate metric values on dashboard ─────────────────────
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.metric-card, .feature-card').forEach(card => {
        observer.observe(card);
    });

    // ── Auto-dismiss flash messages after 5 seconds ────────────
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ── Smooth scroll for anchor links ─────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});

// ── AI Chat Interactive Client ─────────────────────────────────

// Simple markdown formatter for chat bubbles
function formatChatMarkdown(text) {
    if (!text) return "";
    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Bold **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Italic *text*
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    // Inline code `text`
    html = html.replace(/`(.*?)`/g, '<code class="px-1 bg-dark bg-opacity-50 rounded text-info">$1</code>');

    // Bullet points
    const lines = html.split('\n');
    let inList = false;
    let result = [];

    for (let line of lines) {
        let trimmed = line.trim();
        if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
            if (!inList) {
                result.push('<ul class="mb-2 ps-3">');
                inList = true;
            }
            result.push(`<li>${trimmed.substring(2)}</li>`);
        } else if (/^\d+\.\s/.test(trimmed)) {
            if (!inList) {
                result.push('<ol class="mb-2 ps-3">');
                inList = true;
            }
            result.push(`<li>${trimmed.replace(/^\d+\.\s/, '')}</li>`);
        } else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            if (trimmed) {
                result.push(`<p class="mb-2">${trimmed}</p>`);
            }
        }
    }
    if (inList) {
        result.push('</ul>');
    }

    return result.join('');
}

// ── Voice & Speech Synthesis Utilities ─────────────────────────
let speechRecognition = null;
let isRecognizing = false;
let popupRecognition = null;
let isPopupRecognizing = false;

// Text-to-Speech (Voice Output)
function speakText(rawText, btnElement) {
    if (!('speechSynthesis' in window)) {
        alert("Speech synthesis is not supported in this browser.");
        return;
    }

    // If already speaking, stop
    if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
        document.querySelectorAll('.msg-action-btn.speaking').forEach(b => {
            b.classList.remove('speaking');
            b.innerHTML = '<i class="bi bi-volume-up"></i> Listen';
        });
        const stopBtn = document.getElementById('stopVoiceBtn');
        if (stopBtn) stopBtn.classList.add('d-none');
        if (btnElement && btnElement.dataset.speaking === "true") {
            btnElement.dataset.speaking = "false";
            return;
        }
    }

    // Clean markdown/symbols for clear, natural speech
    const cleanSpeech = rawText
        .replace(/[*_#`~>\[\]()]/g, '')
        .replace(/DM/g, 'Deutsche Mark')
        .replace(/P\(Bad\)/g, 'Probability of bad credit')
        .replace(/\\le/g, 'less than or equal to')
        .replace(/\\ge/g, 'greater than or equal to')
        .replace(/\\%/g, ' percent');

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // Pick best natural voice if available
    const voices = window.speechSynthesis.getVoices();
    const naturalVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Guy')));
    if (naturalVoice) {
        utterance.voice = naturalVoice;
    }

    const stopBtn = document.getElementById('stopVoiceBtn');
    if (stopBtn) stopBtn.classList.remove('d-none');

    if (btnElement) {
        btnElement.classList.add('speaking');
        btnElement.dataset.speaking = "true";
        btnElement.innerHTML = '<i class="bi bi-stop-circle-fill"></i> Stop';
    }

    utterance.onend = () => {
        if (btnElement) {
            btnElement.classList.remove('speaking');
            btnElement.dataset.speaking = "false";
            btnElement.innerHTML = '<i class="bi bi-volume-up"></i> Listen';
        }
        if (stopBtn) stopBtn.classList.add('d-none');
    };

    utterance.onerror = () => {
        if (btnElement) {
            btnElement.classList.remove('speaking');
            btnElement.dataset.speaking = "false";
            btnElement.innerHTML = '<i class="bi bi-volume-up"></i> Listen';
        }
        if (stopBtn) stopBtn.classList.add('d-none');
    };

    window.speechSynthesis.speak(utterance);
}

function stopSpeech() {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    document.querySelectorAll('.msg-action-btn.speaking').forEach(b => {
        b.classList.remove('speaking');
        b.innerHTML = '<i class="bi bi-volume-up"></i> Listen';
    });
    const stopBtn = document.getElementById('stopVoiceBtn');
    if (stopBtn) stopBtn.classList.add('d-none');
}

// Speech-to-Text (Voice Input) for main chat
function toggleVoiceRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
        alert("Speech Recognition is not supported by your browser. Please use Chrome, Edge, or Safari.");
        return;
    }

    const micBtn = document.getElementById('voiceMicBtn');
    const micIcon = document.getElementById('voiceMicIcon');
    const banner = document.getElementById('voiceRecordingBanner');
    const input = document.getElementById('chatInput');

    if (isRecognizing && speechRecognition) {
        speechRecognition.stop();
        return;
    }

    speechRecognition = new SpeechRec();
    speechRecognition.continuous = false;
    speechRecognition.interimResults = false;
    speechRecognition.lang = 'en-US';

    speechRecognition.onstart = () => {
        isRecognizing = true;
        if (micBtn) micBtn.classList.add('recording');
        if (banner) {
            banner.classList.remove('d-none');
            banner.classList.add('d-flex');
        }
    };

    speechRecognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (input) {
            input.value = transcript;
            // Automatically submit spoken question
            document.getElementById('chatForm').dispatchEvent(new Event('submit', { cancelable: true }));
        }
    };

    speechRecognition.onerror = (event) => {
        console.warn("Speech recognition error:", event.error);
        stopVoiceRecognition();
    };

    speechRecognition.onend = () => {
        stopVoiceRecognition();
    };

    speechRecognition.start();
}

function stopVoiceRecognition() {
    isRecognizing = false;
    const micBtn = document.getElementById('voiceMicBtn');
    const banner = document.getElementById('voiceRecordingBanner');
    if (micBtn) micBtn.classList.remove('recording');
    if (banner) {
        banner.classList.add('d-none');
        banner.classList.remove('d-flex');
    }
    if (speechRecognition) {
        try { speechRecognition.stop(); } catch (e) {}
    }
}

// Speech-to-Text for floating popup widget
function togglePopupVoiceRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
        alert("Speech Recognition is not supported by your browser. Please use Chrome, Edge, or Safari.");
        return;
    }

    const micBtn = document.getElementById('popupVoiceMicBtn');
    const input = document.getElementById('popupChatInput');

    if (isPopupRecognizing && popupRecognition) {
        popupRecognition.stop();
        isPopupRecognizing = false;
        if (micBtn) micBtn.classList.remove('recording');
        return;
    }

    popupRecognition = new SpeechRec();
    popupRecognition.continuous = false;
    popupRecognition.interimResults = false;
    popupRecognition.lang = 'en-US';

    popupRecognition.onstart = () => {
        isPopupRecognizing = true;
        if (micBtn) micBtn.classList.add('recording');
    };

    popupRecognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (input) {
            input.value = transcript;
            document.getElementById('popupChatForm').dispatchEvent(new Event('submit', { cancelable: true }));
        }
    };

    popupRecognition.onerror = () => {
        isPopupRecognizing = false;
        if (micBtn) micBtn.classList.remove('recording');
    };

    popupRecognition.onend = () => {
        isPopupRecognizing = false;
        if (micBtn) micBtn.classList.remove('recording');
    };

    popupRecognition.start();
}

// Copy Message to Clipboard
function copyMessageText(btn) {
    const content = btn.closest('.msg-content').querySelector('.msg-text-body');
    if (content) {
        const text = content.innerText;
        navigator.clipboard.writeText(text).then(() => {
            const original = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check2 text-success"></i> Copied!';
            setTimeout(() => {
                btn.innerHTML = original;
            }, 2000);
        });
    }
}

// ── Dedicated ChatGPT-style submit with streaming typing effect ──
async function handleChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const container = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('chatSendBtn');

    if (!input || !container) return;
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';

    // Append user message bubble
    container.innerHTML += `
        <div class="chat-message user-message d-flex gap-2 animate-fade-in">
            <div class="msg-avatar text-light bg-primary bg-opacity-50"><i class="bi bi-person-fill fs-5"></i></div>
            <div class="msg-content p-3">
                <p class="mb-0">${msg.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</p>
            </div>
        </div>
    `;

    // Append typing indicator
    const typingId = 'typing-' + Date.now();
    container.innerHTML += `
        <div id="${typingId}" class="chat-message bot-message d-flex gap-2 animate-fade-in">
            <div class="msg-avatar">🛡️</div>
            <div class="msg-content p-3 glass-card border-secondary border-opacity-25">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    container.scrollTop = container.scrollHeight;

    if (sendBtn) sendBtn.disabled = true;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();

        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();

        const rawReply = data.reply || data.error || "No response received.";
        const formattedReply = formatChatMarkdown(rawReply);
        const msgId = 'msg-' + Date.now();

        // Create message bubble with action toolbar
        const botBubble = document.createElement('div');
        botBubble.className = 'chat-message bot-message d-flex gap-2 animate-fade-in w-100';
        botBubble.innerHTML = `
            <div class="msg-avatar">🛡️</div>
            <div class="msg-content p-3 glass-card border-primary border-opacity-25 w-100">
                <div class="msg-text-body" id="${msgId}"></div>
                <div class="msg-actions">
                    <button class="msg-action-btn" onclick="speakText(this.closest('.msg-content').querySelector('.msg-text-body').innerText, this)">
                        <i class="bi bi-volume-up"></i> Listen
                    </button>
                    <button class="msg-action-btn" onclick="copyMessageText(this)">
                        <i class="bi bi-clipboard"></i> Copy
                    </button>
                    <button class="msg-action-btn" onclick="this.innerHTML='<i class=\\'bi bi-hand-thumbs-up-fill text-success\\'></i>'">
                        <i class="bi bi-hand-thumbs-up"></i>
                    </button>
                </div>
            </div>
        `;
        container.appendChild(botBubble);

        // ChatGPT-style streaming typewriter animation
        const targetEl = document.getElementById(msgId);
        targetEl.innerHTML = formattedReply;

        // Auto-read voice if enabled
        const autoSpeak = document.getElementById('voiceAutoSpeak');
        if (autoSpeak && autoSpeak.checked) {
            const listenBtn = botBubble.querySelector('.msg-action-btn');
            speakText(targetEl.innerText, listenBtn);
        }

    } catch (err) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        container.innerHTML += `
            <div class="chat-message bot-message d-flex gap-2 animate-fade-in">
                <div class="msg-avatar">🛡️</div>
                <div class="msg-content p-3 glass-card border-danger text-danger">
                    Error contacting AI service. Please check your connection.
                </div>
            </div>
        `;
    } finally {
        if (sendBtn) sendBtn.disabled = false;
        container.scrollTop = container.scrollHeight;
        input.focus();
    }
}

// Quick Prompt Sender
function sendQuickPrompt(promptText) {
    const input = document.getElementById('chatInput');
    if (input) {
        input.value = promptText;
        document.getElementById('chatForm').dispatchEvent(new Event('submit', { cancelable: true }));
    }
}

// New Chat Session
function newChatSession() {
    stopSpeech();
    clearChat();
    const input = document.getElementById('chatInput');
    if (input) input.focus();
}

// Clear Chat Function
function clearChat() {
    stopSpeech();
    const container = document.getElementById('chatMessages');
    if (container) {
        container.innerHTML = `
            <div class="chat-message bot-message d-flex gap-3 animate-fade-in">
                <div class="msg-avatar">🛡️</div>
                <div class="msg-content p-3 glass-card border-primary border-opacity-25 w-100">
                    <p class="mb-2 fw-semibold text-info"><i class="bi bi-stars me-1"></i>New conversation started!</p>
                    <p class="mb-0 text-secondary small">Ask any question or click the microphone to speak with CreditRisk AI.</p>
                </div>
            </div>
        `;
    }
}

// Keyboard shortcut (Ctrl+K for New Chat)
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        const chatForm = document.getElementById('chatForm');
        if (chatForm) {
            e.preventDefault();
            newChatSession();
        }
    }
});

// ── Floating Chat Widget Toggle & Submission ───────────────────
function toggleFloatingChat() {
    const popup = document.getElementById('aiChatPopup');
    const closedIcon = document.querySelector('.chat-icon-closed');
    const openIcon = document.querySelector('.chat-icon-open');

    if (!popup) return;

    if (popup.classList.contains('d-none')) {
        popup.classList.remove('d-none');
        if (closedIcon) closedIcon.classList.add('d-none');
        if (openIcon) openIcon.classList.remove('d-none');
        const input = document.getElementById('popupChatInput');
        if (input) setTimeout(() => input.focus(), 150);
    } else {
        popup.classList.add('d-none');
        if (closedIcon) closedIcon.classList.remove('d-none');
        if (openIcon) openIcon.classList.add('d-none');
    }
}

async function handlePopupChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('popupChatInput');
    const container = document.getElementById('popupChatMessages');
    if (!input || !container) return;

    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    // Append user bubble
    container.innerHTML += `
        <div class="chat-message user-message d-flex gap-2">
            <div class="msg-content p-2 px-3 small">
                ${msg.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
            </div>
        </div>
    `;

    // Append typing indicator
    const typingId = 'popup-typing-' + Date.now();
    container.innerHTML += `
        <div id="${typingId}" class="chat-message bot-message d-flex gap-2">
            <div class="msg-avatar small">🛡️</div>
            <div class="msg-content p-2 px-3 glass-card small">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    container.scrollTop = container.scrollHeight;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();

        const raw = data.reply || "No response received.";
        const formatted = formatChatMarkdown(raw);
        container.innerHTML += `
            <div class="chat-message bot-message d-flex gap-2">
                <div class="msg-avatar small">🛡️</div>
                <div class="msg-content p-2 px-3 glass-card small border-primary border-opacity-25 w-100">
                    <div class="popup-msg-text">${formatted}</div>
                    <div class="msg-actions mt-1 pt-1">
                        <button class="msg-action-btn py-0" style="font-size:0.7rem;" onclick="speakText(this.closest('.msg-content').querySelector('.popup-msg-text').innerText, this)">
                            <i class="bi bi-volume-up"></i> Listen
                        </button>
                    </div>
                </div>
            </div>
        `;
    } catch (err) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        container.innerHTML += `
            <div class="chat-message bot-message d-flex gap-2">
                <div class="msg-avatar small">🛡️</div>
                <div class="msg-content p-2 px-3 glass-card small text-danger">
                    Error connecting to AI service.
                </div>
            </div>
        `;
    } finally {
        container.scrollTop = container.scrollHeight;
    }
}
