/**
 * app.js
 * Arfal Malik Gibran | 24782005 | TRI 4 A
 */

function updateNavbar() {
    const navMenus = document.getElementById('nav-menus');
    if (!navMenus) return;

    if (isLoggedIn()) {
        const username = localStorage.getItem('username') || 'Warga';
        navMenus.innerHTML = `
            <span class="navbar-text text-white opacity-75 small me-2 d-none d-md-inline">
                <i class="bi bi-person-circle me-1"></i>${username}
            </span>
            <button onclick="logout()" class="btn btn-sm btn-danger d-flex align-items-center gap-1">
                <i class="bi bi-box-arrow-right"></i>
                <span class="d-none d-md-inline">Keluar</span>
            </button>`;
    } else {
        navMenus.innerHTML = `
            <a href="#login" class="btn btn-sm btn-outline-light d-flex align-items-center gap-1">
                <i class="bi bi-box-arrow-in-right"></i>
                <span>Masuk</span>
            </a>`;
    }
}

document.addEventListener('DOMContentLoaded', () => { updateNavbar(); });