/**
 * app.js — Lab 12
 * Arfal Malik Gibran | 24782005 | TRI 4 A
 */

// =====================================================================
// STATE GLOBAL
// =====================================================================
let currentTab = 'my_reports';
let currentPage = 1;
let editingReportId = null; // null = buat baru, ada id = edit draft

// =====================================================================
// STATUS CONFIG
// =====================================================================
const STATUS_CONFIG = {
    'DRAFT':       { label: 'Draft',        color: 'secondary', progress: 10,  icon: 'bi-pencil' },
    'REPORTED':    { label: 'Dilaporkan',   color: 'info',      progress: 30,  icon: 'bi-flag' },
    'VERIFIED':    { label: 'Diverifikasi', color: 'primary',   progress: 55,  icon: 'bi-patch-check' },
    'IN_PROGRESS': { label: 'Diproses',     color: 'warning',   progress: 75,  icon: 'bi-gear' },
    'RESOLVED':    { label: 'Selesai',      color: 'success',   progress: 100, icon: 'bi-check-circle' },
};

// =====================================================================
// NAVBAR
// =====================================================================
function updateNavbar() {
    const navMenus = document.getElementById('nav-menus');
    if (!navMenus) return;
    if (isLoggedIn()) {
        const username = localStorage.getItem('username') || 'Warga';
        navMenus.innerHTML = `
            <span class="navbar-text text-white opacity-75 small me-2 d-none d-md-inline">
                <i class="bi bi-person-circle me-1"></i>${username}
            </span>
            <button onclick="openNewReportModal()" class="btn btn-sm btn-warning fw-bold me-1 d-none d-md-flex align-items-center gap-1">
                <i class="bi bi-plus-circle"></i><span>Laporan Baru</span>
            </button>
            <button onclick="logout()" class="btn btn-sm btn-danger d-flex align-items-center gap-1">
                <i class="bi bi-box-arrow-right"></i>
                <span class="d-none d-md-inline">Keluar</span>
            </button>`;
    } else {
        navMenus.innerHTML = `
            <a href="#login" class="btn btn-sm btn-outline-light d-flex align-items-center gap-1">
                <i class="bi bi-box-arrow-in-right"></i><span>Masuk</span>
            </a>`;
    }
}

// =====================================================================
// LOAD DASHBOARD DATA
// =====================================================================
async function loadDashboardData(tab = currentTab, page = currentPage) {
    currentTab = tab;
    currentPage = page;

    const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');

    if (response && response.status === 200) {
        const data = await response.json();

        const reports    = data.results ?? [];
        const totalCount = data.count ?? 0;
        const totalPages = Math.ceil(totalCount / 10);

        renderList(reports, tab);
        renderPagination(totalPages, page, tab);
        loadSummaryStats();
    } else {
        const listContainer = document.getElementById('listContainer');
        if (listContainer) {
            listContainer.innerHTML = `
                <div class="col-12 text-center text-muted p-5">
                    <i class="bi bi-exclamation-triangle fs-1"></i>
                    <p>Gagal memuat data laporan.</p>
                </div>`;
        }
        const paginationContainer = document.getElementById('paginationContainer');
        if (paginationContainer) paginationContainer.innerHTML = '';
    }
}

// =====================================================================
// RENDER LIST — Kartu + Progress Bar
// =====================================================================
function renderList(reports, tab) {
    const listContainer = document.getElementById('listContainer');
    if (!listContainer) return;

    if (reports.length === 0) {
        listContainer.innerHTML = `
            <div class="col-12 text-center text-muted py-5">
                <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                <p class="mb-0">Belum ada laporan di sini.</p>
                ${tab === 'my_reports' ? `<button onclick="openNewReportModal()" class="btn btn-primary btn-sm mt-3"><i class="bi bi-plus me-1"></i>Buat Laporan Pertama</button>` : ''}
            </div>`;
        return;
    }

    listContainer.innerHTML = reports.map(report => {
        const cfg = STATUS_CONFIG[report.status] || STATUS_CONFIG['DRAFT'];
        const isOwner = report.is_owner;
        const reporterName = report.reporter_display || 'Warga Anonim';

        const draftActions = isOwner && report.status === 'DRAFT' ? `
            <div class="d-flex gap-2 mt-2">
                <button class="btn btn-sm btn-outline-primary flex-fill" onclick="editDraft(${report.id})">
                    <i class="bi bi-pencil me-1"></i>Edit Draft
                </button>
                <button class="btn btn-sm btn-primary flex-fill" onclick="submitReport(${report.id})">
                    <i class="bi bi-send me-1"></i>Ajukan
                </button>
            </div>` : '';

        return `
        <div class="card report-card mb-3">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-1">
                    <h6 class="fw-bold mb-0" style="font-size:0.9rem;">${escapeHtml(report.title)}</h6>
                    <span class="badge bg-${cfg.color} status-badge ms-2">
                        <i class="bi ${cfg.icon} me-1"></i>${cfg.label}
                    </span>
                </div>
                <p class="text-muted mb-1" style="font-size:0.78rem;">
                    <i class="bi bi-geo-alt me-1"></i>${escapeHtml(report.location || '-')}
                </p>
                <p class="text-muted mb-2" style="font-size:0.78rem;">
                    <i class="bi bi-person me-1"></i>${escapeHtml(reporterName)}
                    <span class="ms-2"><i class="bi bi-clock me-1"></i>${formatDate(report.updated_at)}</span>
                </p>
                <div class="d-flex align-items-center gap-2">
                    <div class="progress flex-fill">
                        <div class="progress-bar bg-${cfg.color}" role="progressbar"
                            style="width:${cfg.progress}%"
                            aria-valuenow="${cfg.progress}" aria-valuemin="0" aria-valuemax="100">
                        </div>
                    </div>
                    <small class="text-muted" style="font-size:0.7rem;white-space:nowrap;">${cfg.progress}%</small>
                </div>
                ${draftActions}
            </div>
        </div>`;
    }).join('');
}

// =====================================================================
// RENDER PAGINATION
// =====================================================================
function renderPagination(totalPages, currentPage, tab) {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;
    if (totalPages <= 1) { paginationContainer.innerHTML = ''; return; }

    let buttons = '';
    for (let i = 1; i <= totalPages; i++) {
        buttons += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <button class="page-link" onclick="loadDashboardData('${tab}', ${i})">${i}</button>
            </li>`;
    }

    paginationContainer.innerHTML = `
        <nav>
            <ul class="pagination pagination-sm justify-content-center mb-0">
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <button class="page-link" onclick="loadDashboardData('${tab}', ${currentPage - 1})">
                        <i class="bi bi-chevron-left"></i>
                    </button>
                </li>
                ${buttons}
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <button class="page-link" onclick="loadDashboardData('${tab}', ${currentPage + 1})">
                        <i class="bi bi-chevron-right"></i>
                    </button>
                </li>
            </ul>
        </nav>`;
}

// =====================================================================
// LOAD SUMMARY STATS — Rekap sidebar
// =====================================================================
async function loadSummaryStats() {
    const response = await requestAPI('/api/report/?tab=my_reports&page_size=1000', 'GET');
    if (!response || response.status !== 200) return;

    const data = await response.json();
    const all  = data.results ?? [];

    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    set('statTotal',   all.length);
    set('statDraft',   all.filter(r => r.status === 'DRAFT').length);
    set('statProcess', all.filter(r => ['REPORTED','VERIFIED','IN_PROGRESS'].includes(r.status)).length);
    set('statDone',    all.filter(r => r.status === 'RESOLVED').length);
}

// =====================================================================
// SWITCH TAB
// =====================================================================
function switchTab(tab) {
    currentPage = 1;
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    loadDashboardData(tab, 1);
}

// =====================================================================
// MODAL — Buat laporan baru
// =====================================================================
function openNewReportModal() {
    editingReportId = null;
    const form = document.getElementById('reportForm');
    if (form) form.reset();
    document.getElementById('reportModalLabel').innerHTML =
        '<i class="bi bi-pencil-square me-2"></i>Buat Laporan Baru';
    document.getElementById('reportAlertContainer').innerHTML = '';
    const modal = new bootstrap.Modal(document.getElementById('reportModal'));
    modal.show();
    setupModalButtons();
}

// =====================================================================
// EDIT DRAFT
// =====================================================================
async function editDraft(id) {
    const response = await requestAPI(`/api/report/${id}/`, 'GET');
    if (!response || response.status !== 200) { alert('Gagal mengambil data laporan.'); return; }
    const report = await response.json();

    document.getElementById('reportTitle').value       = report.title || '';
    document.getElementById('reportCategory').value    = report.category || 'other';
    document.getElementById('reportLocation').value    = report.location || '';
    document.getElementById('reportDescription').value = report.description || '';
    document.getElementById('reportAlertContainer').innerHTML = '';

    editingReportId = id;
    document.getElementById('reportModalLabel').innerHTML =
        `<i class="bi bi-pencil me-2"></i>Edit Draft #${id}`;

    const modal = new bootstrap.Modal(document.getElementById('reportModal'));
    modal.show();
    setupModalButtons();
}

// =====================================================================
// SUBMIT REPORT (dari tombol Ajukan di kartu)
// =====================================================================
async function submitReport(id) {
    const response = await requestAPI(`/api/report/${id}/`, 'PATCH', { status: 'REPORTED' });
    if (response && response.status === 200) loadDashboardData();
}

// =====================================================================
// SETUP TOMBOL MODAL
// =====================================================================
function setupModalButtons() {
    const btnDraft  = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');
    const newDraft  = btnDraft.cloneNode(true);
    const newSubmit = btnSubmit.cloneNode(true);
    btnDraft.replaceWith(newDraft);
    btnSubmit.replaceWith(newSubmit);

    async function getFormData(status) {
        const title       = document.getElementById('reportTitle').value.trim();
        const category    = document.getElementById('reportCategory').value;
        const location    = document.getElementById('reportLocation').value.trim();
        const description = document.getElementById('reportDescription').value.trim();
        if (!title) { showReportAlert('Judul tidak boleh kosong.', 'warning'); return null; }
        return { title, category, location, description, status };
    }

    async function sendForm(status) {
        const payload  = await getFormData(status);
        if (!payload) return;
        const isEdit   = editingReportId !== null;
        const method   = isEdit ? 'PUT' : 'POST';
        const endpoint = isEdit ? `/api/report/${editingReportId}/` : '/api/report/';
        const response = await requestAPI(endpoint, method, payload);
        if (response && (response.status === 201 || response.status === 200)) {
            bootstrap.Modal.getInstance(document.getElementById('reportModal')).hide();
            document.getElementById('reportForm').reset();
            editingReportId = null;
            loadDashboardData();
        } else {
            showReportAlert('Gagal menyimpan. Coba lagi.', 'danger');
        }
    }

    document.getElementById('btnDraft').addEventListener('click',  () => sendForm('DRAFT'));
    document.getElementById('btnSubmit').addEventListener('click', () => sendForm('REPORTED'));
}

// =====================================================================
// HELPERS
// =====================================================================
function showReportAlert(message, type = 'info') {
    const el = document.getElementById('reportAlertContainer');
    if (el) el.innerHTML = `<div class="alert alert-${type} py-2 mb-0 mt-2 small">${message}</div>`;
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

document.addEventListener('DOMContentLoaded', () => { updateNavbar(); });