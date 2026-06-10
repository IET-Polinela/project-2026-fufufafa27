/**
 * auth.js
 * Arfal Malik Gibran | 24782005 | TRI 4 A
 */

function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.replaceWith(loginForm.cloneNode(true));
    const freshForm = document.getElementById('loginForm');

    freshForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Wajib: cegah reload & bocor password ke URL

        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;

        if (!username || !password) {
            showLoginAlert('Username dan password tidak boleh kosong.', 'warning');
            return;
        }

        const submitBtn = freshForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Masuk...`;

        try {
            const response = await requestAPI('/api/token/', 'POST', {
                username: username,
                password: password,
            });

            if (response.status === 200) {
                const data = await response.json();

                // Simpan token ke localStorage
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                localStorage.setItem('username', username);

                showLoginAlert('Login berhasil! Mengalihkan ke Dashboard...', 'success');

                setTimeout(() => {
                    window.location.hash = '#dashboard';
                }, 800);

            } else if (response.status === 401) {
                showLoginAlert('Username atau password salah.', 'danger');
            } else {
                showLoginAlert('Login gagal. Coba lagi.', 'danger');
            }

        } catch (error) {
            showLoginAlert('Tidak dapat terhubung ke server. Pastikan backend berjalan di port 8000.', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

function showLoginAlert(message, type = 'info') {
    const alertContainer = document.getElementById('loginAlertContainer');
    if (!alertContainer) return;
    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show py-2 mb-0 mt-3" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>`;
}

function logout() {
    clearTokens();
    localStorage.removeItem('username');
    window.location.hash = '#login';
}