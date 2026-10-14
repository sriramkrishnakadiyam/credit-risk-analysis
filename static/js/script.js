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
