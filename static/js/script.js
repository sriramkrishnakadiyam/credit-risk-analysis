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

// Dedicated full-page chat handler
async function handleChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const container = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('chatSendBtn');

    if (!input || !container) return;
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';

    // Append user message
    container.innerHTML += `
        <div class="chat-message user-message d-flex gap-2 animate-fade-in">
            <div class="msg-avatar text-light"><i class="bi bi-person-fill"></i></div>
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

        const formattedReply = formatChatMarkdown(data.reply || data.error || "No response received.");
        container.innerHTML += `
            <div class="chat-message bot-message d-flex gap-2 animate-fade-in">
                <div class="msg-avatar">🛡️</div>
                <div class="msg-content p-3 glass-card border-primary border-opacity-25">
                    ${formattedReply}
                </div>
            </div>
        `;
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

// Clear Chat Function
function clearChat() {
    const container = document.getElementById('chatMessages');
    if (container) {
        container.innerHTML = `
            <div class="chat-message bot-message d-flex gap-3 animate-fade-in">
                <div class="msg-avatar">🛡️</div>
                <div class="msg-content p-3 glass-card border-primary border-opacity-25">
                    <p class="mb-2 fw-semibold text-info">Chat cleared! How can I assist you with credit risk classification?</p>
                    <p class="mb-0 text-secondary small">Ask about loan eligibility, Logistic Regression metrics (75% accuracy, 80% recall), or input features.</p>
                </div>
            </div>
        `;
    }
}

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

        const formatted = formatChatMarkdown(data.reply || "No response received.");
        container.innerHTML += `
            <div class="chat-message bot-message d-flex gap-2">
                <div class="msg-avatar small">🛡️</div>
                <div class="msg-content p-2 px-3 glass-card small border-primary border-opacity-25">
                    ${formatted}
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
