/**
 * Credit Risk Classification — Client-side JavaScript
 * Form validation and UI enhancements
 */

document.addEventListener('DOMContentLoaded', () => {
    // ── Bootstrap form validation ──────────────────────────────
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Show loading state on submit button
                const btn = document.getElementById('submitBtn');
                if (btn) {
                    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analysing…';
                    btn.disabled = true;
                }
            }
            form.classList.add('was-validated');
        });
    }

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
