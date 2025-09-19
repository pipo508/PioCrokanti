// src/services/api.js

import axios from 'axios';

// Creamos una instancia de Axios con una configuración base.
const api = axios.create({
  // Asegúrate de que esta sea la URL donde corre tu backend de Flask.
  // Por defecto, Flask corre en el puerto 5000.
  baseURL: 'http://127.0.0.1:5000/api', 
});

export default api;