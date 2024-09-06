import axios, { AxiosInstance } from 'axios';
import { setToken } from './utils/AxiosInstance';

function isLoggedIn(): boolean {
    const token = localStorage.getItem('token');
    if (token !== null && token !== undefined) setToken(token);
    return token !== null && token !== undefined;
}

const backendUrl = `http://127.0.0.1:5000`; // Replace with your actual backend URL

const axiosInstance: AxiosInstance = axios.create({
    baseURL: backendUrl,
    headers: {
        'Content-Type': 'application/json' // Optional: Set any default headers
    }
});

export { axiosInstance, isLoggedIn };

