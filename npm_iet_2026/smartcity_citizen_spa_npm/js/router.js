/**
 * router.js
 * Arfal Malik Gibran | 24782005 | TRI 4 A
 */

const routes = {

    '#login': `
        <div id="login-page" class="d-flex align-items-center justify-content-center py-5">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-11 col-sm-8 col-md-6 col-lg-4">
                        <div class="card login-card shadow-lg">
                            <div class="card-header text-white text-center">
                                <div class="mb-3"><i class="bi bi-buildings-fill" style="font-size:2.5rem;"></i></div>
                                <h4 class="fw-bold mb-1">Portal Warga</h4>
                                <p class="mb-0 opacity-75 small">Smart City Lampung</p>
                            </div>
                            <div class="card-body p-4">
                                <form id="loginForm" novalidate>
                                    <div class="mb-3">
                                        <label class="form-label fw-semibold small">
                                            <i class="bi bi-person me-1"></i>Username
                                        </label>
                                        <input type="text" id="loginUsername" class="form-control" placeholder="Masukkan username" required>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label fw-semibold small">
                                            <i class="bi bi-key me-1"></i>Password
                                        </label>
                                        <input type="password" id="loginPassword" class="form-control" placeholder="Masukkan password" required>
                                    </div>
                                    <div id="loginAlertContainer"></div>
                                    <div class="d-grid mt-3">
                                        <button type="submit" class="btn btn-primary fw-bold">
                                            <i class="bi bi-box-arrow-in-right me-2"></i>Masuk
                                        </button>
                                    </div>
                                </form>
                            </div>
                            <div class="card-footer bg-light text-center py-3">
                                <small class="text-muted">
                                    <i class="bi bi-shield-lock me-1"></i>Diamankan dengan JWT Authentication
                                </small>
                            </div>
                        </div>
                        <p class="text-center text-white opacity-50 mt-3 small">
                            PIE 1416 · Lab 11 · Arfal Malik Gibran · 24782005
                        </p>
                    </div>
                </div>
            </div>
        </div>`,

    '#dashboard': `
        <div class="row g-0">

            <!-- Kolom Kiri: Sidebar (25%) -->
            <aside class="col-12 col-lg-3 d-none d-lg-block" id="sidebar">
                <div class="pt-3">
                    <div class="px-3 pb-3 mb-2 border-bottom border-secondary">
                        <div class="d-flex align-items-center gap-2">
                            <div class="bg-primary rounded-circle d-flex align-items-center justify-content-center" style="width:40px;height:40px;flex-shrink:0;">
                                <i class="bi bi-person-fill text-white"></i>
                            </div>
                            <div>
                                <div class="fw-semibold text-white small" id="sidebarUsername">Warga</div>
                                <div class="text-success" style="font-size:0.7rem;">
                                    <i class="bi bi-circle-fill me-1" style="font-size:0.5rem;"></i>Online
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="sidebar-heading">Menu Utama</div>
                    <nav class="nav flex-column">
                        <a href="#dashboard" class="nav-link active"><i class="bi bi-speedometer2 me-2"></i>Dashboard</a>
                        <a href="#laporan" class="nav-link"><i class="bi bi-file-earmark-text me-2"></i>Laporan Saya</a>
                        <a href="#buat-laporan" class="nav-link"><i class="bi bi-plus-circle me-2"></i>Buat Laporan</a>
                    </nav>
                    <div class="sidebar-heading mt-2">Lainnya</div>
                    <nav class="nav flex-column">
                        <a href="#profil" class="nav-link"><i class="bi bi-person-circle me-2"></i>Profil Saya</a>
                        <a href="#" class="nav-link text-danger" onclick="logout(); return false;">
                            <i class="bi bi-box-arrow-left me-2"></i>Keluar
                        </a>
                    </nav>
                </div>
            </aside>

            <!-- Kolom Tengah: Konten Utama (50%) -->
            <section class="col-12 col-lg-6 p-3 p-lg-4">
                <div class="d-flex align-items-center justify-content-between mb-4">
                    <div>
                        <h5 class="fw-bold mb-0"><i class="bi bi-hand-wave text-warning me-2"></i>Selamat Datang!</h5>
                        <p class="text-muted small mb-0">Portal Warga Smart City Lampung</p>
                    </div>
                </div>
                <div class="row g-3 mb-4">
                    <div class="col-6">
                        <div class="card stat-card text-center p-3">
                            <div class="stat-icon bg-primary bg-opacity-10 text-primary mx-auto mb-2">
                                <i class="bi bi-file-earmark-check"></i>
                            </div>
                            <div class="fw-bold fs-4">12</div>
                            <div class="text-muted small">Total Laporan</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card stat-card text-center p-3">
                            <div class="stat-icon bg-success bg-opacity-10 text-success mx-auto mb-2">
                                <i class="bi bi-check2-circle"></i>
                            </div>
                            <div class="fw-bold fs-4">5</div>
                            <div class="text-muted small">Selesai</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card stat-card text-center p-3">
                            <div class="stat-icon bg-warning bg-opacity-10 text-warning mx-auto mb-2">
                                <i class="bi bi-clock-history"></i>
                            </div>
                            <div class="fw-bold fs-4">4</div>
                            <div class="text-muted small">Dalam Proses</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card stat-card text-center p-3">
                            <div class="stat-icon bg-danger bg-opacity-10 text-danger mx-auto mb-2">
                                <i class="bi bi-exclamation-circle"></i>
                            </div>
                            <div class="fw-bold fs-4">3</div>
                            <div class="text-muted small">Menunggu</div>
                        </div>
                    </div>
                </div>
                <div class="card border-0 shadow-sm mb-4 text-center">
                    <div class="card-body py-4">
                        <i class="bi bi-inbox fs-1 text-muted mb-2 d-block"></i>
                        <h5 class="mt-2">Selamat Datang!</h5>
                        <p class="text-muted small mb-0">Koneksi API untuk data laporan akan diimplementasikan pada Lab 12.</p>
                    </div>
                </div>
                <div class="d-grid">
                    <a href="#buat-laporan" class="btn btn-primary btn-lg fw-bold">
                        <i class="bi bi-plus-circle-fill me-2"></i>Buat Laporan Baru
                    </a>
                </div>
            </section>

            <!-- Kolom Kanan: Pengumuman (25%) -->
            <aside class="col-12 col-lg-3 d-none d-lg-block p-3">
                <div class="card border-0 shadow-sm sticky-top mb-3" style="top:20px;">
                    <div class="card-header bg-white border-bottom">
                        <h6 class="fw-bold mb-0"><i class="bi bi-info-circle-fill text-primary me-2"></i>Pengumuman</h6>
                    </div>
                    <div class="card-body p-0">
                        <div class="list-group list-group-flush">
                            <div class="list-group-item px-3 py-2">
                                <div class="d-flex align-items-start gap-2">
                                    <i class="bi bi-megaphone-fill text-warning mt-1"></i>
                                    <div>
                                        <div class="small fw-semibold">Pemeliharaan Sistem</div>
                                        <div class="text-muted" style="font-size:0.75rem;">Jadwal maintenance Sabtu 00:00-02:00 WIB</div>
                                    </div>
                                </div>
                            </div>
                            <div class="list-group-item px-3 py-2">
                                <div class="d-flex align-items-start gap-2">
                                    <i class="bi bi-patch-check-fill text-success mt-1"></i>
                                    <div>
                                        <div class="small fw-semibold">Fitur Baru</div>
                                        <div class="text-muted" style="font-size:0.75rem;">Upload foto laporan kini tersedia</div>
                                    </div>
                                </div>
                            </div>
                            <div class="list-group-item px-3 py-2">
                                <div class="d-flex align-items-start gap-2">
                                    <i class="bi bi-calendar-event-fill text-primary mt-1"></i>
                                    <div>
                                        <div class="small fw-semibold">Agenda Kota</div>
                                        <div class="text-muted" style="font-size:0.75rem;">Musrenbang Kelurahan, 15 Juni 2026</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-white border-bottom">
                        <h6 class="fw-bold mb-0"><i class="bi bi-activity text-success me-2"></i>Status Sistem</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="small">API Backend</span>
                            <span class="badge bg-success"><i class="bi bi-circle-fill me-1" style="font-size:0.5rem;"></i>Online</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="small">Database</span>
                            <span class="badge bg-success"><i class="bi bi-circle-fill me-1" style="font-size:0.5rem;"></i>Online</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="small">Auth Service</span>
                            <span class="badge bg-success"><i class="bi bi-circle-fill me-1" style="font-size:0.5rem;"></i>Online</span>
                        </div>
                    </div>
                </div>
            </aside>

        </div>

        <!-- Mobile Bottom Navigation -->
        <nav class="d-lg-none fixed-bottom bg-white border-top shadow-lg">
            <div class="row g-0 text-center">
                <div class="col">
                    <a href="#dashboard" class="d-block py-2 text-primary text-decoration-none">
                        <i class="bi bi-speedometer2 d-block fs-5"></i>
                        <span style="font-size:0.65rem;">Dashboard</span>
                    </a>
                </div>
                <div class="col">
                    <a href="#laporan" class="d-block py-2 text-muted text-decoration-none">
                        <i class="bi bi-file-earmark-text d-block fs-5"></i>
                        <span style="font-size:0.65rem;">Laporan</span>
                    </a>
                </div>
                <div class="col">
                    <a href="#buat-laporan" class="d-block py-2 text-muted text-decoration-none">
                        <i class="bi bi-plus-circle d-block fs-5"></i>
                        <span style="font-size:0.65rem;">Buat</span>
                    </a>
                </div>
                <div class="col">
                    <a href="#profil" class="d-block py-2 text-muted text-decoration-none">
                        <i class="bi bi-person-circle d-block fs-5"></i>
                        <span style="font-size:0.65rem;">Profil</span>
                    </a>
                </div>
            </div>
        </nav>`,
};

// =====================================================================
// ROUTING UTAMA
// =====================================================================
function handleRouting() {
    const hash = window.location.hash || '#login';
    const appContent = document.getElementById('app-content');
    const loggedIn = isLoggedIn();

    if (!loggedIn && hash !== '#login') {
        window.location.hash = '#login';
        return;
    }
    if (loggedIn && hash === '#login') {
        window.location.hash = '#dashboard';
        return;
    }

    appContent.innerHTML = routes[hash] || `
        <div class="d-flex align-items-center justify-content-center" style="min-height:70vh;">
            <div class="text-center">
                <i class="bi bi-exclamation-triangle-fill text-warning" style="font-size:4rem;"></i>
                <h2 class="fw-bold mt-3">404 — Halaman Tidak Ditemukan</h2>
                <a href="#dashboard" class="btn btn-primary mt-2"><i class="bi bi-house me-2"></i>Kembali</a>
            </div>
        </div>`;

    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }

    if (hash === '#dashboard') {
        const usernameEl = document.getElementById('sidebarUsername');
        if (usernameEl) usernameEl.textContent = localStorage.getItem('username') || 'Warga';
        if (typeof updateNavbar === 'function') updateNavbar();
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);