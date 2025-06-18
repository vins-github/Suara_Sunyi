STYLE = """
<style>
/* Global font & background */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f9fafc;
    color: #222;
}

/* Headings */
h1, h2, h3, h4 {
    color: #2c3e50;
    font-weight: 700;
}

/* Custom blur-style record button */
.record-button {
    backdrop-filter: blur(8px);
    background-color: rgba(255, 255, 255, 0.06);
    color: #2c3e50;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s ease;
}
.record-button:hover {
    background-color: rgba(200, 200, 255, 0.1);
}

/* Unduh Rekaman */
.download-button {
    display: inline-block;
    background-color: #34495e;
    color: white;
    padding: 0.7rem 1.4rem;
    border-radius: 10px;
    text-decoration: none;
    font-size: 1rem;
    transition: 0.3s ease;
}
.download-button:hover {
    background-color: #2c3e50;
}

/* Emotion card */
.emotion-card {
    background: linear-gradient(to right, #e4ecf7, #ffffff);
    border-left: 6px solid #6c9bcf;
    padding: 1.2rem;
    border-radius: 12px;
    margin-top: 2rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

/* Transkripsi box */
.transcript-box {
    background-color: #f0f4f8;
    padding: 1rem;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    color: #333;
    overflow-x: auto;
    box-shadow: inset 0 0 3px rgba(0,0,0,0.1);
}
</style>
"""
