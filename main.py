# Importaciones para la creación de una API

# FastAPI: Framework web moderno y rápido para crear APIs con Python
# HTTPException: Para manejar y lanzar excepciones HTTP personalizadas
from fastapi import FastAPI, HTTPException

# HTMLResponse: Para devolver respuestas en formato HTML
# JSONResponse: Para devolver respuestas en formato JSON
from fastapi.responses import HTMLResponse, JSONResponse

# pandas: Biblioteca para manipulación y análisis de datos estructurados
import pandas as pd

# nltk: Biblioteca de procesamiento de lenguaje natural (NLP)
import nltk

# word_tokenize: Función para dividir texto en palabras individuales (tokenización)
from nltk.tokenize import word_tokenize

# wordnet: Base de datos léxica para obtener sinónimos, antónimos y relaciones semánticas
from nltk.corpus import wordnet

# Configuración de la ruta donde NLTK buscará los datos descargados
nltk.data.path.append('C:/Users/jhonm/AppData/Roaming/nltk_data')

# Descarga de paquetes necesarios de NLTK solo si no están ya descargados
try:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    # Descargar punkt_tab si no existe
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"⚠️ Advertencia NLTK: {e}")

# ========================================
# ETAPA 5: INICIALIZACIÓN DE LA API
# ========================================

# Crear la instancia de FastAPI con las especificaciones solicitadas
app = FastAPI(
    title="mi aplicacion de peliculas",
    version="1.0.0",
    description="API para consultar y analizar contenido de Netflix usando procesamiento de lenguaje natural"
)

# ========================================
# ETAPA 4: CARGA DEL DATASET
# ========================================

# Variable global para el dataset
dataset_netflix = None

def cargar_dataset():
    """
    Carga el archivo netflix_titles.csv con pandas
    Retorna: DataFrame con los datos de Netflix
    """
    try:
        df = pd.read_csv('DataSet/netflix_titles.csv')
        print(f"✅ Dataset cargado exitosamente: {len(df)} registros")
        return df
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo netflix_titles.csv")
        return None
    except Exception as e:
        print(f"❌ Error al cargar el dataset: {e}")
        return None

def identificar_columnas(df):
    """
    Identifica y describe las columnas del dataset
    Parámetros: df - DataFrame de Netflix
    """
    if df is None:
        return
    
    print("\n" + "="*50)
    print("🔍 ANÁLISIS DE COLUMNAS")
    print("="*50)
    
    columnas_info = {
        'show_id': 'ID único del show',
        'type': 'Tipo de contenido (Movie/TV Show)',
        'title': 'Título del contenido',
        'director': 'Director(es) del contenido',
        'cast': 'Reparto principal',
        'country': 'País(es) de producción',
        'date_added': 'Fecha de agregado a Netflix',
        'release_year': 'Año de lanzamiento',
        'rating': 'Clasificación por edad',
        'duration': 'Duración del contenido',
        'listed_in': 'Géneros/categorías',
        'description': 'Descripción del contenido'
    }
    
    for col, desc in columnas_info.items():
        if col in df.columns:
            valores_unicos = df[col].nunique()
            print(f"📌 {col}: {desc}")
            print(f"   - Valores únicos: {valores_unicos}")
            if valores_unicos <= 10:
                print(f"   - Valores: {list(df[col].unique())}")
            print()

# Evento de inicio para cargar el dataset
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la API
    Carga el dataset de Netflix
    """
    global dataset_netflix
    print("🚀 Iniciando carga del dataset...")
    dataset_netflix = cargar_dataset()
    if dataset_netflix is not None:
        print(f"✅ Dataset listo con {len(dataset_netflix)} registros")
    else:
        print("❌ Error: No se pudo cargar el dataset")

print("✅ API FastAPI inicializada correctamente")
print(f"📱 Título: mi aplicacion de peliculas")
print(f"🔢 Versión: 1.0.0")

# ========================================
# ETAPA 6: RUTAS DE LA API
# ========================================

@app.get("/", response_class=HTMLResponse)
def ruta_inicial():
    """
    Ruta inicial: Interfaz del chatbot para buscar películas por descripción
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot - Mi Aplicación de Películas</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background: #141414;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            
            .container {
                background: #141414;
                width: 100%;
                overflow-x: hidden;
            }
            
            .navbar {
                background: linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, transparent 100%);
                position: fixed;
                top: 0;
                width: 100%;
                padding: 20px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                z-index: 100;
            }
            
            .navbar-logo {
                color: #e50914;
                font-size: 2em;
                font-weight: bold;
                text-decoration: none;
            }
            
            .search-box {
                background: rgba(0,0,0,0.75);
                border: 1px solid #333;
                color: white;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 1em;
                width: 300px;
            }
            
            .hero-section {
                position: relative;
                height: 80vh;
                background: linear-gradient(to bottom, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 100%);
                display: flex;
                align-items: center;
                padding: 60px;
                margin-top: 70px;
            }
            
            .hero-content {
                max-width: 40%;
                color: white;
                z-index: 10;
            }
            
            .hero-title {
                font-size: 4em;
                font-weight: bold;
                margin-bottom: 20px;
                text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
            }
            
            .hero-meta {
                display: flex;
                gap: 20px;
                align-items: center;
                margin-bottom: 20px;
                font-size: 1.1em;
            }
            
            .hero-meta span {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .hero-description {
                font-size: 1.2em;
                line-height: 1.6;
                margin-bottom: 30px;
                color: #e5e5e5;
            }
            
            .hero-buttons {
                display: flex;
                gap: 15px;
            }
            
            .btn {
                padding: 12px 35px;
                border: none;
                border-radius: 4px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-play {
                background: white;
                color: black;
            }
            
            .btn-play:hover {
                background: #e5e5e5;
            }
            
            .btn-info {
                background: rgba(109, 109, 110, 0.7);
                color: white;
            }
            
            .btn-info:hover {
                background: rgba(109, 109, 110, 0.4);
            }
            
            .header {
                background: transparent;
                padding: 0;
                text-align: left;
                border: none;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .content-section {
                padding: 40px 60px;
            }
            
            .section-title {
                color: white;
                font-size: 1.8em;
                margin-bottom: 20px;
                font-weight: bold;
            }
            
            .content-row {
                margin-bottom: 50px;
            }
            
            .items-container {
                display: flex;
                gap: 15px;
                overflow-x: auto;
                padding: 10px 0;
                scroll-behavior: smooth;
            }
            
            .items-container::-webkit-scrollbar {
                height: 8px;
            }
            
            .items-container::-webkit-scrollbar-track {
                background: #141414;
            }
            
            .items-container::-webkit-scrollbar-thumb {
                background: #e50914;
                border-radius: 10px;
            }
            
            .movie-item {
                min-width: 300px;
                background: #1a1a1a;
                border-radius: 4px;
                overflow: hidden;
                cursor: pointer;
                transition: all 0.3s;
                position: relative;
            }
            
            .movie-item:hover {
                transform: scale(1.05);
                z-index: 10;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }
            
            .movie-item-cover {
                width: 100%;
                height: 200px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 3em;
            }
            
            .movie-item-info {
                padding: 15px;
                color: #e5e5e5;
            }
            
            .movie-item-title {
                font-size: 1.1em;
                font-weight: bold;
                margin-bottom: 8px;
                color: white;
            }
            
            .movie-item-meta {
                font-size: 0.9em;
                color: #808080;
            }
            
            .message {
                margin-bottom: 20px;
                animation: fadeIn 0.3s ease-in;
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .bot-message {
                background: #2d2d2d;
                color: #e5e5e5;
                padding: 15px 20px;
                border-radius: 15px;
                max-width: 80%;
                margin-left: 0;
                border-left: 4px solid #e50914;
            }
            
            .user-message {
                background: #e50914;
                color: white;
                padding: 15px 20px;
                border-radius: 15px;
                max-width: 80%;
                margin-left: auto;
                margin-right: 0;
                font-weight: bold;
            }
            
            .input-container {
                padding: 30px 60px;
                background: #141414;
                border-top: 1px solid #333;
            }
            
            input[type="text"] {
                background: rgba(0,0,0,0.75);
                color: white;
                border: 1px solid #333;
            }
            
            .search-results {
                background: rgba(0,0,0,0.9);
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .input-group {
                display: flex;
                gap: 10px;
            }
            
            input[type="text"] {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #ddd;
                border-radius: 30px;
                font-size: 1em;
                outline: none;
                transition: border-color 0.3s;
            }
            
            input[type="text"]:focus {
                border-color: #e50914;
            }
            
            button {
                padding: 15px 40px;
                background: #e50914;
                color: white;
                border: none;
                border-radius: 30px;
                font-size: 1em;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                font-weight: bold;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(229, 9, 20, 0.5);
                background: #b20710;
            }
            
            button:active {
                transform: translateY(0);
            }
            
            .results {
                margin-top: 20px;
                padding: 20px;
                background: #141414;
                border-radius: 10px;
                border: 1px solid #3d3d3d;
            }
            
            .movie-card {
                background: #2d2d2d;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 8px;
                border: 1px solid #3d3d3d;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
            }
            
            .movie-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(229, 9, 20, 0.3);
                border-color: #e50914;
            }
            
            .movie-title {
                font-size: 1.5em;
                font-weight: bold;
                color: #e50914;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .movie-description {
                color: #b0b0b0;
                line-height: 1.6;
                margin-bottom: 12px;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }
            
            .read-more {
                color: #e50914;
                cursor: pointer;
                font-weight: bold;
                font-size: 0.9em;
            }
            
            .movie-info {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                font-size: 0.85em;
                color: #808080;
                margin-top: 10px;
            }
            
            .movie-info span {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .loading {
                text-align: center;
                padding: 20px;
                color: #e50914;
                font-size: 1.2em;
            }
            
            .error {
                background: #3d1a1a;
                color: #ff4444;
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #ff4444;
            }
            
            .welcome-message {
                text-align: center;
                color: #808080;
                padding: 30px;
            }
            
            .welcome-message h2 {
                color: #e50914;
                margin-bottom: 15px;
            }
            
            .examples {
                margin-top: 20px;
                padding: 15px;
                background: #2d2d2d;
                border-radius: 10px;
                border-left: 4px solid #e50914;
            }
            
            .examples h3 {
                color: #e50914;
                margin-bottom: 10px;
            }
            
            .example-keywords {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
            }
            
            .example-keyword {
                background: rgba(255,255,255,0.1);
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                transition: all 0.2s;
                border: 1px solid #333;
                color: white;
            }
            
            .example-keyword:hover {
                background: #e50914;
                color: white;
                border-color: #e50914;
            }
            
            /* Modal Netflix Style */
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.9);
                overflow-y: auto;
            }
            
            .modal-content {
                background: linear-gradient(180deg, #141414 0%, #1a1a1a 100%);
                margin: 50px auto;
                padding: 0;
                max-width: 800px;
                border-radius: 10px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                position: relative;
                border: 2px solid #3d3d3d;
            }
            
            .modal-header {
                background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
                padding: 30px 40px;
                border-radius: 10px 10px 0 0;
            }
            
            .modal-header h2 {
                color: white;
                margin: 0;
                font-size: 2em;
            }
            
            .close {
                position: absolute;
                right: 20px;
                top: 20px;
                color: white;
                font-size: 35px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.3s;
            }
            
            .close:hover {
                transform: rotate(90deg);
            }
            
            .modal-body {
                padding: 40px;
                color: #e5e5e5;
            }
            
            .modal-synopsis {
                font-size: 1.1em;
                line-height: 1.8;
                margin-bottom: 30px;
                color: #d0d0d0;
            }
            
            .modal-info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .modal-info-item {
                background: #2d2d2d;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #e50914;
            }
            
            .modal-info-label {
                color: #808080;
                font-size: 0.9em;
                margin-bottom: 5px;
            }
            
            .modal-info-value {
                color: white;
                font-size: 1.1em;
                font-weight: bold;
            }
            
            .modal-footer {
                padding: 20px 40px;
                background: #1a1a1a;
                border-radius: 0 0 10px 10px;
                border-top: 1px solid #3d3d3d;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="navbar">
                <div class="navbar-logo">NETFLIX</div>
                <input type="text" class="search-box" id="userInput" placeholder="Buscar películas..." onkeypress="if(event.key==='Enter') enviarMensaje(event)">
            </div>
            
            <div class="hero-section" id="heroSection">
                <div class="hero-content">
                    <h1 class="hero-title">🎬 Encuentra tu próximo show favorito</h1>
                    <div class="hero-meta">
                        <span>⭐ 5.0</span>
                        <span>📅 2024</span>
                        <span>🎭 Netflix Bot</span>
                    </div>
                    <p class="hero-description">
                        Describe el tipo de película que te gustaría ver y te ayudaré a encontrarla. 
                        Usa palabras clave como "acción", "romance", "terror" o cualquier género que te interese.
                    </p>
                    <div class="hero-buttons">
                        <button class="btn btn-play" onclick="empezarBusqueda()">▶ Buscar Ahora</button>
                        <button class="btn btn-info" onclick="scrollToCategorias()">ℹ️ Ver Categorías</button>
                    </div>
                </div>
            </div>
            
            <div class="content-section" id="categoriasSection">
                <h2 class="section-title">Explorar por Categorías</h2>
                <div class="content-row">
                    <div class="example-keywords">
                        <span class="example-keyword" onclick="buscar('action adventure hero')">Superhéroes</span>
                        <span class="example-keyword" onclick="buscar('romantic comedy love')">Romance</span>
                        <span class="example-keyword" onclick="buscar('crime drama mystery')">Crimen</span>
                        <span class="example-keyword" onclick="buscar('horror scary monster')">Terror</span>
                        <span class="example-keyword" onclick="buscar('sci-fi space future')">Sci-Fi</span>
                        <span class="example-keyword" onclick="buscar('family children animation')">Familia</span>
                        <span class="example-keyword" onclick="buscar('comedy fun humor')">Comedia</span>
                        <span class="example-keyword" onclick="buscar('documentary real life')">Documentales</span>
                    </div>
                </div>
            </div>
            
            <div id="results"></div>
            
            </div>
        
        <script>
            function enviarMensaje(event) {
                event.preventDefault();
                const input = document.getElementById('userInput');
                const busqueda = input.value.trim();
                
                if (!busqueda) {
                    alert('Por favor, escribe algo para buscar');
                    return;
                }
                
                // Mostrar carga
                mostrarCarga();
                
                // Hacer la petición a la API
                fetch(`/peliculas/descripcion/${encodeURIComponent(busqueda)}`)
                    .then(response => {
                        if (!response.ok) {
                            return response.json().then(err => {
                                throw new Error(err.detail || 'Error en la búsqueda');
                            });
                        }
                        return response.json();
                    })
                    .then(data => {
                        mostrarResultados(busqueda, data.peliculas, data.total);
                    })
                    .catch(error => {
                        mostrarError(error.message);
                    });
                
                // Limpiar el input
                input.value = '';
                
                // Scroll a los resultados
                document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
            }
            
            function agregarMensajeUsuario(mensaje) {
                // Ya no usamos mensajes de usuario en el nuevo diseño
            }
            
            function mostrarCarga() {
                const results = document.getElementById('results');
                results.innerHTML = '<div class="loading">🔍 Buscando películas...</div>';
            }
            
            function mostrarResultados(busqueda, peliculas, total) {
                const results = document.getElementById('results');
                
                if (peliculas.length === 0) {
                    results.innerHTML = '<div class="error">No se encontraron películas con esa descripción</div>';
                    return;
                }
                
                peliculasActuales = peliculas;
                
                let html = `<div class="content-section"><h2 class="section-title">Resultados de tu búsqueda (${total} encontradas)</h2><div class="content-row"><div class="items-container">`;
                
                peliculas.forEach((pelicula, index) => {
                    const emoji = pelicula.type === 'Movie' ? '🎬' : '📺';
                    const tipoTexto = pelicula.type === 'Movie' ? 'Película' : (pelicula.type === 'TV Show' ? 'Serie' : pelicula.type || 'N/A');
                    html += `
                        <div class="movie-item" onclick="verDetalle(${index})">
                            <div class="movie-item-cover">${emoji}</div>
                            <div class="movie-item-info">
                                <div class="movie-item-title">${pelicula.title || 'Sin título'}</div>
                                <div class="movie-item-meta">${tipoTexto} • ${pelicula.rating || 'N/A'} • ${pelicula.release_year || 'N/A'}</div>
                            </div>
                        </div>
                    `;
                });
                
                html += '</div></div></div>';
                results.innerHTML = html;
                
                // Scroll a los resultados
                results.scrollIntoView({ behavior: 'smooth' });
            }
            
            function buscar(keywords) {
                const input = document.getElementById('userInput');
                input.value = keywords;
                enviarMensaje(new Event('submit'));
            }
            
            function empezarBusqueda() {
                const input = document.getElementById('userInput');
                input.focus();
                scrollToCategorias();
            }
            
            function scrollToCategorias() {
                document.getElementById('categoriasSection').scrollIntoView({ behavior: 'smooth' });
            }
            
            function mostrarError(mensaje) {
                const results = document.getElementById('results');
                results.innerHTML = `<div class="error">❌ Error: ${mensaje}</div>`;
            }
            
            let peliculasActuales = [];
            
            function verDetalle(index) {
                const pelicula = peliculasActuales[index];
                
                const modal = document.createElement('div');
                modal.className = 'modal';
                modal.innerHTML = `
                    <div class="modal-content">
                        <div class="modal-header">
                            <span class="close" onclick="cerrarModal()">&times;</span>
                            <h2>${pelicula.title || 'Sin título'}</h2>
                        </div>
                        <div class="modal-body">
                            <div class="modal-synopsis">
                                <h3>📖 Sinopsis</h3>
                                <p>${pelicula.description || 'Sin descripción disponible'}</p>
                            </div>
                            <div class="modal-info-grid">
                                <div class="modal-info-item">
                                    <div class="modal-info-label">🎭 Tipo</div>
                                    <div class="modal-info-value">${pelicula.type === 'Movie' ? 'Película' : (pelicula.type === 'TV Show' ? 'Serie de TV' : pelicula.type || 'N/A')}</div>
                                </div>
                                <div class="modal-info-item">
                                    <div class="modal-info-label">⭐ Clasificación</div>
                                    <div class="modal-info-value">${pelicula.rating || 'N/A'}</div>
                                </div>
                                <div class="modal-info-item">
                                    <div class="modal-info-label">📅 Año</div>
                                    <div class="modal-info-value">${pelicula.release_year || 'N/A'}</div>
                                </div>
                                <div class="modal-info-item">
                                    <div class="modal-info-label">⏱️ Duración</div>
                                    <div class="modal-info-value">${pelicula.duration || 'N/A'}</div>
                                </div>
                                <div class="modal-info-item">
                                    <div class="modal-info-label">🌍 País</div>
                                    <div class="modal-info-value">${pelicula.country || 'N/A'}</div>
                                </div>
                                <div class="modal-info-item">
                                    <div class="modal-info-label">🎬 Director</div>
                                    <div class="modal-info-value">${pelicula.director || 'N/A'}</div>
                                </div>
                            </div>
                            ${pelicula.cast ? `
                            <div class="modal-info-item" style="grid-column: 1 / -1;">
                                <div class="modal-info-label">👥 Reparto</div>
                                <div class="modal-info-value">${pelicula.cast}</div>
                            </div>
                            ` : ''}
                            ${pelicula.listed_in ? `
                            <div class="modal-info-item" style="grid-column: 1 / -1;">
                                <div class="modal-info-label">🏷️ Categorías</div>
                                <div class="modal-info-value">${pelicula.listed_in}</div>
                            </div>
                            ` : ''}
                        </div>
                        <div class="modal-footer">
                            <button onclick="cerrarModal()" style="width: 100%;">Cerrar</button>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                modal.style.display = 'block';
            }
            
            function cerrarModal() {
                const modal = document.querySelector('.modal');
                if (modal) {
                    modal.style.display = 'none';
                    modal.remove();
                }
            }
            
            // Cerrar modal al hacer clic fuera de él
            window.onclick = function(event) {
                const modal = document.querySelector('.modal');
                if (event.target == modal) {
                    cerrarModal();
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/peliculas", response_class=JSONResponse)
def lista_peliculas():
    """
    Ruta para obtener la lista de todas las películas disponibles en el dataset
    """
    if dataset_netflix is None:
        raise HTTPException(status_code=500, detail="No se pudo cargar el dataset")
    
    try:
        # Crear una copia del dataset y reemplazar todos los valores nulos
        df_clean = dataset_netflix.copy()
        
        # Reemplazar NaN, NaT y None por cadenas vacías en todas las columnas
        for col in df_clean.columns:
            df_clean[col] = df_clean[col].replace([None, 'None', float('nan'), 'nan'], "")
        
        # Convertir a lista de diccionarios
        peliculas = df_clean.to_dict(orient='records')
        
        # Retornar solo los primeros 100 resultados para evitar tiempos de carga
        return JSONResponse(content={
            "total": len(dataset_netflix),
            "total_en_respuesta": len(peliculas[:100]),
            "mensaje": "Mostrando primeros 100 resultados",
            "peliculas": peliculas[:100]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener películas: {str(e)}")

@app.get("/peliculas/{id}", response_class=JSONResponse)
def pelicula_por_id(id: str):
    """
    Ruta para obtener una película específica según su ID
    Parámetros: id - ID de la película a buscar
    """
    if dataset_netflix is None:
        raise HTTPException(status_code=500, detail="No se pudo cargar el dataset")
    
    try:
        # Buscar la película por su ID en la columna 'show_id'
        pelicula = dataset_netflix[dataset_netflix['show_id'] == id]
        
        if pelicula.empty:
            raise HTTPException(status_code=404, detail=f"No se encontró película con ID: {id}")
        
        # Convertir a diccionario reemplazando valores NaN por None
        pelicula_dict = pelicula.fillna("").to_dict(orient='records')[0]
        
        return JSONResponse(content=pelicula_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar película: {str(e)}")

@app.get("/peliculas/categoria/{categoria}", response_class=JSONResponse)
def peliculas_por_categoria(categoria: str):
    """
    Ruta para obtener lista de películas según la categoría solicitada por el usuario
    Parámetros: categoria - Categoría a filtrar (por ejemplo: "Dramas", "Comedies", etc.)
    """
    if dataset_netflix is None:
        raise HTTPException(status_code=500, detail="No se pudo cargar el dataset")
    
    try:
        # Buscar películas cuya columna 'listed_in' contenga la categoría especificada
        peliculas = dataset_netflix[
            dataset_netflix['listed_in'].str.contains(categoria, case=False, na=False)
        ]
        
        if peliculas.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron películas en la categoría: {categoria}"
            )
        
        # Convertir a lista de diccionarios reemplazando valores NaN por None
        peliculas_list = peliculas.fillna("").to_dict(orient='records')
        
        return JSONResponse(content={
            "categoria": categoria,
            "total": len(peliculas_list),
            "peliculas": peliculas_list
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar por categoría: {str(e)}")

# ========================================
# ETAPA 7: RUTA DEL CHATBOT - FILTRO POR DESCRIPCIÓN
# ========================================

# Importar stopwords para filtrar palabras comunes
from nltk.corpus import stopwords

# Obtener lista de stopwords en inglés
try:
    stop_words = set(stopwords.words('english'))
except:
    stop_words = set()

def limpiar_y_tokenizar(texto):
    """
    Limpia y tokeniza un texto eliminando stopwords
    Parámetros: texto - Texto a limpiar y tokenizar
    Retorna: Lista de palabras tokenizadas y limpiadas
    """
    if texto is None or pd.isna(texto):
        return []
    
    # Tokenizar el texto
    tokens = word_tokenize(str(texto).lower())
    
    # Filtrar stopwords y solo mantener palabras alfanuméricas
    palabras_limpias = [palabra for palabra in tokens 
                       if palabra.isalnum() and palabra not in stop_words]
    
    return palabras_limpias

def buscar_peliculas_por_descripcion(descripcion_usuario, dataset):
    """
    Busca películas que contengan palabras clave de la descripción del usuario
    Parámetros: 
        descripcion_usuario - Descripción o palabras clave del usuario
        dataset - DataFrame con las películas
    Retorna: Lista de películas que coinciden
    """
    # Tokenizar y limpiar la descripción del usuario
    palabras_usuario = limpiar_y_tokenizar(descripcion_usuario)
    
    if not palabras_usuario:
        return pd.DataFrame()
    
    # Buscar películas cuyas descripciones contengan las palabras del usuario
    peliculas_encontradas = []
    
    for idx, row in dataset.iterrows():
        descripcion = row.get('description', '')
        if pd.isna(descripcion):
            continue
        
        # Tokenizar la descripción de la película
        palabras_descripcion = limpiar_y_tokenizar(descripcion)
        
        # Contar cuántas palabras del usuario aparecen en la descripción
        palabras_coincidentes = set(palabras_usuario) & set(palabras_descripcion)
        
        if palabras_coincidentes:
            peliculas_encontradas.append({
                'indice': idx,
                'coincidencias': len(palabras_coincidentes),
                'palabras_clave': list(palabras_coincidentes)
            })
    
    # Ordenar por número de coincidencias (las que más coincidencias tienen primero)
    peliculas_encontradas.sort(key=lambda x: x['coincidencias'], reverse=True)
    
    # Obtener los índices de las películas encontradas
    indices = [p['indice'] for p in peliculas_encontradas]
    
    # Retornar las películas ordenadas por relevancia
    peliculas_resultado = dataset.loc[indices].copy()
    
    # Agregar información de relevancia
    for i, idx in enumerate(indices):
        if idx in peliculas_resultado.index:
            peliculas_resultado.at[idx, '_relevancia'] = peliculas_encontradas[i]['coincidencias']
            peliculas_resultado.at[idx, '_palabras_clave'] = ', '.join(peliculas_encontradas[i]['palabras_clave'])
    
    return peliculas_resultado

@app.get("/peliculas/descripcion/{descripcion}", response_class=JSONResponse)
def peliculas_por_descripcion(descripcion: str):
    """
    Ruta del chatbot para obtener lista de películas que coinciden con la descripción del usuario
    Parámetros: descripcion - Descripción o palabras clave que el usuario busca
    Ejemplo: /peliculas/descripcion/action adventure hero
    """
    if dataset_netflix is None:
        raise HTTPException(status_code=500, detail="No se pudo cargar el dataset")
    
    try:
        # Buscar películas que coinciden con la descripción
        peliculas = buscar_peliculas_por_descripcion(descripcion, dataset_netflix)
        
        if peliculas.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron películas que coincidan con: {descripcion}"
            )
        
        # Limpiar valores NaN antes de convertir a diccionario
        peliculas_limpias = peliculas.fillna("").to_dict(orient='records')
        
        # Limpiar las columnas temporales de relevancia
        for pelicula in peliculas_limpias:
            if '_relevancia' in pelicula:
                relevancia = pelicula.pop('_relevancia', 0)
            if '_palabras_clave' in pelicula:
                palabras_clave = pelicula.pop('_palabras_clave', '')
        
        return JSONResponse(content={
            "busqueda": descripcion,
            "total": len(peliculas_limpias),
            "peliculas": peliculas_limpias[:50]  # Limitar a 50 resultados
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar por descripción: {str(e)}")

print("✅ Rutas de la API creadas exitosamente")
print("✅ Ruta del chatbot (filtro por descripción) creada")
