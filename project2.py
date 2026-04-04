# ==============================
# ELITE SEARCH ENGINE (SMART STYLE UI + ANIMATIONS)
# ==============================

import os
import re
import math
from flask import Flask, render_template_string, request, jsonify
from collections import defaultdict, Counter

app = Flask(__name__)

# -----------------------------
# SEARCH ENGINE CORE
# -----------------------------
class SearchEngine:
    def __init__(self):
        self.documents = {}
        self.index = defaultdict(set)
        self.freq = {}
        self.N = 0

    def tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    def add_document(self, name, text):
        self.documents[name] = text
        words = self.tokenize(text)
        self.freq[name] = Counter(words)
        for word in set(words):
            self.index[word].add(name)
        self.N = len(self.documents)

    def tf_idf(self, word, doc):
        tf = self.freq[doc][word]
        df = len(self.index[word]) if word in self.index else 1
        return tf * math.log((self.N + 1) / (df + 1))

    def search(self, query):
        words = self.tokenize(query)
        scores = defaultdict(float)
        for word in words:
            for doc in self.index.get(word, []):
                scores[doc] += self.tf_idf(word, doc)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def snippet(self, doc, query, length=150):
        text = self.documents[doc]
        idx = text.lower().find(query.lower())
        start = max(0, idx - length//2) if idx != -1 else 0
        snippet = text[start:start+length]
        for word in query.split():
            snippet = re.sub(f"(?i)({word})", r"<mark>\\1</mark>", snippet)
        return snippet + "..."

engine = SearchEngine()
UPLOAD_FOLDER = "/tmp/documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
for file in os.listdir("documents"):
    if file.endswith(".txt"):
        with open(os.path.join("documents", file), 'r', encoding='utf-8') as f:
            engine.add_document(file, f.read())

# -----------------------------
# SMART-STYLE UI
# -----------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Elite Search</title>
<style>
body {
  font-family: Arial;
  margin:0;
  transition:0.4s;
  background: linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)), url('https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1920&q=100') no-repeat center center fixed;
  background-size: cover;
  color:white;
}

.light {
  background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)),
              url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1920&q=100') no-repeat center center fixed;
  background-size: cover;
  color:Black;
}

.container {
  text-align:center;
  margin-top:120px;
  padding:40px;
  width:60%;
  margin-left:auto;
  margin-right:auto;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(15px);
  border-radius:25px;
  box-shadow:0 8px 30px rgba(0,0,0,0.4);
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from {opacity:0; transform:translateY(20px);} 
  to {opacity:1; transform:translateY(0);} 
}

.search-box {
  width:70%;
  margin:auto;
  display:flex;
  align-items:center;
  background:white;
  border-radius:50px;
  padding:12px 25px;
  box-shadow:0 6px 25px rgba(0,0,0,0.25);
  transition:0.2s;
}

.search-box:hover {
  box-shadow:0 8px 25px rgba(0,0,0.8,0.8);
}

.search-box input {
  border:none;
  outline:none;
  flex:1;
  font-size:12px;
}


button {
  margin-top:30px;
  padding:10px 20px;
  border:none;
  border-radius:20px;
  cursor:pointer;
  background:#2563eb;
  color:white;
  transition:0.3s;
}

.button-box:hover{
  box-shadow:0 8px 25px rgba(0,0,0,0.8);
}

.result {
  width:80%;
  margin:20px auto;
  text-align:left;
  background: rgba(255,255,255,0.9);
  color:black;
  padding:20px;
  border-radius:15px;
  box-shadow:0 6px 20px rgba(0,0,0,0.2);
  animation: fadeIn 0.5s ease-in-out;
}

mark { background:yellow; }

#loader {
  display:none;
  margin-top:20px;
}

.loader {
  border:6px solid #f3f3f3;
  border-top:6px solid #3498db;
  border-radius:50%;
  width:40px;
  height:40px;
  animation: spin 1s linear infinite;
  margin:auto;
}

@keyframes spin {
  0% { transform: rotate(0deg);} 
  100% { transform: rotate(360deg);} 
}

.upload {
  margin-top:30px;
  padding:30px;
  border-radius:20px;
  background: linear-gradient(135deg, rgba(59,130,246,0.9), rgba(147,51,234,0.9));
  color:white;
  box-shadow:0 10px 30px rgba(0,0,0,0.3);
  transition:0.3s;
}

.upload:hover {
  transform: scale(1.02);
  box-shadow:0 15px 40px rgba(0,0,0,0.4);
}

.toggle {
  position:absolute;
  top:10px;
  right:20px;
}
.custom-file {
  display:inline-block;
  padding:12px 20px;
  background:white;
  color:#2563eb;
  border-radius:25px;
  cursor:pointer;
  font-weight:bold;
  transition:0.3s;
}

.custom-file:hover {
  background:#e0e7ff;
  transform: scale(1.05);
}

</style>
<script>
async function search(){
 let q = document.getElementById('q').value;
 document.getElementById('loader').style.display='block';
 let res = await fetch(`/search?q=${q}`);
 let data = await res.json();
 document.getElementById('loader').style.display='none';
 let div = document.getElementById('results');
 div.innerHTML='';
 data.forEach(r=>{
   div.innerHTML += `<div class='result'><b>${r.doc}</b><br>${r.snippet}</div>`;
 });
}

async function upload(){
 let fileInput = document.getElementById('file');
 let formData = new FormData();
 formData.append('file', fileInput.files[0]);
 await fetch('/upload', { method:'POST', body:formData });
 alert('Uploaded!');
}

function toggleTheme(){ document.body.classList.toggle('light'); }
</script>
</head>
<body>
<button class="toggle" onclick="toggleTheme()">🌙</button>
<div class="container">
<h1>Elite Search</h1>
<div class="search-box">
<input id="q" placeholder="Search anything...">
</div>
<button onclick="search()">Search</button>
<div id="loader"><div class="loader"></div></div>

<div class="upload">
  <h3>Upload Your Documents</h3>
  <p>Drag & drop or select a file to index instantly</p>
  
  <label for="file" class="custom-file">
    📁 Choose File
  </label>
  <input type="file" id="file" hidden>
  
  <br><br>
  <button onclick="upload()">Upload Now</button>
</div>

<div id="results"></div>
</div>
</body>
</html>
"""

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/search")
def search():
 q = request.args.get("q", "")
 results = engine.search(q)
 return jsonify([{"doc": d, "snippet": engine.snippet(d, q)} for d, s in results])

@app.route("/upload", methods=["POST"])
def upload():
 file = request.files['file']
 text = file.read().decode('utf-8')
 engine.add_document(file.filename, text)
 return "OK"

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
 app.run()
