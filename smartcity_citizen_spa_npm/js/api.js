/**
 * api.js
 * Arfal Malik Gibran | 24782005 | TRI 4 A
 */

const BASE_URL = 'http://127.0.0.1:8000';

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