/**
 * api.js
 * Arfal Malik Gibran | 24782005 | TRI 4 A
 */

const BASE_URL = 'http://103.151.63.71:8008';

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const headers = { 'Content-Type': 'application/json' };

    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const config = { method: method, headers: headers };

    if (bodyData && method !== 'GET') {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);

        // ✅ TAMBAHAN LAB 15 — Interceptor 401
        if (response.status === 401) {
            alert('Sesi Anda telah habis atau Anda belum login.');
            localStorage.clear();
            window.location.hash = '#login';
            return null;
        }

        return response;
    } catch (error) {
        console.error('[API] Network error:', error);
        throw error;
    }
}

function isLoggedIn() {
    return !!localStorage.getItem('access_token');
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}