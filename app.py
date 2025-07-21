# Requirements:
# Flask
# (install with: pip install flask)
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- Core logic (from GX_python_20250720_c20194.py) ---
fiber_data = {
    "Cotton": {"breathability": 0.9, "softness": 0.85, "durability": 0.6, "moisture_regain": 0.8},
    "Polyester": {"breathability": 0.6, "softness": 0.5, "durability": 0.9, "moisture_regain": 0.4},
    "Wool": {"breathability": 0.7, "softness": 0.8, "durability": 0.7, "moisture_regain": 0.9},
    "Cotton-Polyester Blend": {"breathability": 0.75, "softness": 0.7, "durability": 0.8, "moisture_regain": 0.6},
    "Wool-Acrylic Blend": {"breathability": 0.65, "softness": 0.75, "durability": 0.75, "moisture_regain": 0.7},
    "Bamboo": {"breathability": 0.85, "softness": 0.9, "durability": 0.65, "moisture_regain": 0.85},
    "Silk": {"breathability": 0.8, "softness": 0.95, "durability": 0.5, "moisture_regain": 0.75},
    "Linen": {"breathability": 0.95, "softness": 0.6, "durability": 0.7, "moisture_regain": 0.7}
}

weave_data = {
    "Plain": {"stiffness": 0.7, "breathability": 0.8},
    "Twill": {"stiffness": 0.6, "breathability": 0.7},
    "Satin": {"stiffness": 0.5, "breathability": 0.6},
    "Jersey": {"stiffness": 0.4, "breathability": 0.9},
    "Denim": {"stiffness": 0.8, "breathability": 0.5}
}

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome - Fabric Comfort Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            min-height: 100vh;
        }
        .main-card {
            max-width: 600px;
            margin: 60px auto;
            border-radius: 20px;
            box-shadow: 0 4px 32px #0002;
            background: rgba(255,255,255,0.95);
            animation: fadeIn 1.2s;
        }
        .header {
            font-size: 2.3rem;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5rem;
            text-decoration: underline;
            letter-spacing: 1px;
        }
        .header .bi {
            color: #5e72e4;
            font-size: 2.5rem;
            vertical-align: middle;
            margin-right: 10px;
        }
        .footer {
            color: #7f8c8d;
            font-size: 0.9rem;
            text-align: center;
            margin-top: 2rem;
        }
        .btn-primary {
            background: linear-gradient(90deg, #5e72e4 0%, #825ee4 100%);
            border: none;
            font-size: 1.2rem;
            transition: box-shadow 0.2s;
        }
        .btn-primary:hover {
            box-shadow: 0 2px 12px #5e72e455;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: none; }
        }
    </style>
</head>
<body>
    <div class="main-card bg-white p-5">
        <div class="header"><i class="bi bi-patch-check"></i>Welcome to the Fabric Comfort Analyzer</div>
        <p class="lead text-center mb-4">Easily analyze the comfort of various fabric types based on their properties.<br>Click below to get started!</p>
        <div class="d-flex justify-content-center">
            <a href="{{ url_for('analyzer') }}" class="btn btn-primary btn-lg fw-bold">
                <i class="bi bi-arrow-right-circle me-2"></i>Go to Analyzer
            </a>
        </div>
        <div class="footer">© 2024 Fabric Analyzer | v2.0</div>
    </div>
</body>
</html>
'''

ANALYZER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabric Comfort Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            min-height: 100vh;
        }
        .main-card {
            max-width: 800px;
            margin: 40px auto;
            border-radius: 20px;
            box-shadow: 0 4px 32px #0002;
            background: rgba(255,255,255,0.97);
            animation: fadeIn 1.2s;
        }
        .header {
            font-size: 2.3rem;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5rem;
            text-decoration: underline;
            letter-spacing: 1px;
        }
        .header .bi {
            color: #5e72e4;
            font-size: 2.5rem;
            vertical-align: middle;
            margin-right: 10px;
        }
        .footer {
            color: #7f8c8d;
            font-size: 0.9rem;
            text-align: center;
            margin-top: 2rem;
        }
        .progress { height: 6px; }
        .result-box {
            background: linear-gradient(120deg, #f8f9fa 60%, #e0eafc 100%);
            border-radius: 12px;
            padding: 1.2rem;
            border: 1px solid #ddd;
            margin-top: 1.2rem;
            font-family: 'Segoe UI', Arial, sans-serif;
            box-shadow: 0 2px 8px #0001;
            animation: fadeIn 1.2s;
        }
        .btn-primary {
            background: linear-gradient(90deg, #5e72e4 0%, #825ee4 100%);
            border: none;
            font-size: 1.1rem;
            transition: box-shadow 0.2s;
        }
        .btn-primary:hover {
            box-shadow: 0 2px 12px #5e72e455;
        }
        .btn-outline-secondary {
            border-radius: 50px;
            font-weight: 500;
            font-size: 1.05rem;
        }
        label.form-label {
            color: #5e72e4;
            font-weight: 600;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: none; }
        }
    </style>
</head>
<body>
    <div class="main-card bg-white p-4">
        <div class="header"><i class="bi bi-patch-check"></i>Fabric Comfort Analyzer</div>
        <form id="comfortForm">
            <div class="row g-3">
                <div class="col-md-4">
                    <label for="gsm" class="form-label fw-bold">GSM (g/m²)</label>
                    <input type="number" class="form-control" id="gsm" name="gsm" min="50" max="500" value="150" required placeholder="50-500">
                </div>
                <div class="col-md-4">
                    <label for="fiberType" class="form-label fw-bold">Fiber Type</label>
                    <select class="form-select" id="fiberType" name="fiberType" required>
                        {% for fiber in fibers %}
                        <option value="{{ fiber }}">{{ fiber }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="weaveType" class="form-label fw-bold">Weave Type</label>
                    <select class="form-select" id="weaveType" name="weaveType" required>
                        {% for weave in weaves %}
                        <option value="{{ weave }}">{{ weave }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div class="form-check mt-3">
                <input class="form-check-input" type="checkbox" id="softeningFinish" name="softeningFinish">
                <label class="form-check-label" for="softeningFinish">Softening Finish Applied</label>
            </div>
            <button type="submit" class="btn btn-primary w-100 fw-bold mt-4">
                <i class="bi bi-graph-up-arrow me-2"></i>Analyze Comfort
            </button>
        </form>
        <div class="progress mt-3" id="progressBar" style="display:none;">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div>
        </div>
        <div id="result" class="result-box" style="display:none;"></div>
        <div class="d-flex justify-content-between mt-3">
            <a href="{{ url_for('home') }}" class="btn btn-outline-secondary">
                <i class="bi bi-house-door me-1"></i>Back to Home
            </a>
            <button id="exportBtn" class="btn btn-outline-secondary" style="display:none;">
                <i class="bi bi-download me-1"></i>Export Results
            </button>
        </div>
        <div class="footer">© 2024 Fabric Analyzer | v2.0</div>
    </div>
    <script>
    let lastResultText = '';
    document.getElementById('comfortForm').addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('progressBar').style.display = 'block';
        document.getElementById('result').style.display = 'none';
        document.getElementById('exportBtn').style.display = 'none';
        const gsm = document.getElementById('gsm').value;
        const fiberType = document.getElementById('fiberType').value;
        const weaveType = document.getElementById('weaveType').value;
        const softeningFinish = document.getElementById('softeningFinish').checked;
        fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                gsm: parseFloat(gsm),
                fiber_type: fiberType,
                weave_type: weaveType,
                softening_finish: softeningFinish
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerHTML = `<span class="text-danger">${data.error}</span>`;
                document.getElementById('result').style.display = 'block';
                document.getElementById('progressBar').style.display = 'none';
                return;
            }
            let html = `<b>=== FABRIC COMFORT ANALYSIS ===</b><br><br>`;
            html += `Fiber Type: <b>${data.fiber_type}</b> | Weave: <b>${data.weave_type}</b> | GSM: <b>${data.gsm}</b><br>`;
            html += `Softening Finish: <b>${data.softening_finish ? 'Yes' : 'No'}</b><br><br>`;
            html += `<b>Comfort Score:</b> <span class='text-primary fw-bold'>${data.comfort_score.toFixed(2)}/100</span><br>`;
            html += `<b>Category Breakdown:</b><br>`;
            html += `<ul>`;
            for (const [cat, score] of Object.entries(data.category_breakdown)) {
                html += `<li><b>${cat}:</b> ${score.toFixed(1)}%</li>`;
            }
            html += `</ul>`;
            html += `<b>Detailed Analysis:</b><br><pre style='font-size:1em;'>${data.detailed_analysis}</pre>`;
            html += `<b>Suggestions to Improve Comfort:</b><br>`;
            if (data.suggestions.length > 0) {
                html += `<ol>`;
                for (const s of data.suggestions) {
                    html += `<li>${s}</li>`;
                }
                html += `</ol>`;
            } else {
                html += `<span>- Fabric properties are well-balanced for comfort</span>`;
            }
            lastResultText = html.replace(/<[^>]+>/g, '');
            document.getElementById('result').innerHTML = html;
            document.getElementById('result').style.display = 'block';
            document.getElementById('progressBar').style.display = 'none';
            document.getElementById('exportBtn').style.display = 'inline-block';
        })
        .catch(err => {
            document.getElementById('result').innerHTML = '<span class="text-danger">Error during analysis.</span>';
            document.getElementById('result').style.display = 'block';
            document.getElementById('progressBar').style.display = 'none';
        });
    });
    document.getElementById('exportBtn').addEventListener('click', function() {
        const blob = new Blob([lastResultText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'fabric_analysis_report.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
    </script>
</body>
</html>
'''

def analyze_comfort(gsm, fiber_type, weave_type, softening_finish):
    # Validate GSM
    if gsm < 50 or gsm > 500:
        return {"error": "GSM must be between 50 and 500 g/m²"}
    try:
        fiber_props = fiber_data[fiber_type]
        weave_props = weave_data[weave_type]
    except KeyError as e:
        return {"error": f"Missing data for property: {e}"}
    # Physical parameters
    air_permeability = fiber_props["breathability"] * weave_props["breathability"] * (1.1 if softening_finish else 1.0)
    tensile_strength = fiber_props["durability"] * (0.9 if gsm > 200 else 1.0)
    weight_score = 1.0 - (gsm - 50) / 450  # Normalize GSM (50-500) to 0-1
    # Sensory parameters
    softness = fiber_props["softness"] * (1.2 if softening_finish else 1.0)
    stiffness = weave_props["stiffness"] * (0.8 if softening_finish else 1.0)
    smoothness = softness * 0.9  # Correlated with softness
    # Mechanical parameters
    stretchiness = fiber_props["durability"] * 0.8
    elasticity = fiber_props["moisture_regain"] * 0.7
    recovery = elasticity * 0.9
    durability = fiber_props["durability"]
    abrasion_resistance = durability * 0.95
    # Psychological parameters
    psychological = 0.7  # Placeholder
    # Overall comfort score (weighted average)
    weights = {
        "Physical": 0.4,
        "Sensory": 0.3,
        "Mechanical": 0.2,
        "Psychological": 0.1
    }
    physical_score = (air_permeability + tensile_strength + weight_score) / 3
    sensory_score = (softness + (1 - stiffness) + smoothness) / 3
    mechanical_score = (stretchiness + elasticity + recovery + durability + abrasion_resistance) / 5
    overall_score = (
        physical_score * weights["Physical"] +
        sensory_score * weights["Sensory"] +
        mechanical_score * weights["Mechanical"] +
        psychological * weights["Psychological"]
    ) * 100  # Scale to 0-100
    # Generate suggestions
    suggestions = []
    suggestion_priority = {
        "air_permeability": ("Use natural fibers like cotton or bamboo for better breathability", 3),
        "softness": ("Apply softening finishes or use finer yarns to enhance softness", 2),
        "stiffness": ("Choose a satin or jersey weave to reduce stiffness", 1),
        "durability": ("Incorporate synthetic fibers like polyester for improved durability", 2),
        "gsm": ("Reduce GSM to improve comfort for lightweight applications", 3)
    }
    if air_permeability < 0.7:
        suggestions.append(suggestion_priority["air_permeability"])
    if softness < 0.7:
        suggestions.append(suggestion_priority["softness"])
    if stiffness > 0.6:
        suggestions.append(suggestion_priority["stiffness"])
    if durability < 0.7:
        suggestions.append(suggestion_priority["durability"])
    if gsm > 200:
        suggestions.append(suggestion_priority["gsm"])
    # Sort by priority
    suggestions.sort(key=lambda x: x[1], reverse=True)
    suggestions_text = [s[0] for s in suggestions]
    # Category breakdown
    category_breakdown = {
        "Physical": physical_score * 100,
        "Sensory": sensory_score * 100,
        "Mechanical": mechanical_score * 100,
        "Psychological": psychological * 100
    }
    # Detailed analysis text
    detailed = (
        f"Physical Parameters:\n"
        f"  - Air Permeability: {air_permeability:.2f} (Higher = Better)\n"
        f"  - Tensile Strength: {tensile_strength:.2f} (Higher = Better)\n"
        f"  - Weight (GSM) Score: {weight_score:.2f} (Lower GSM = Better)\n\n"
        f"Sensory Parameters:\n"
        f"  - Softness: {softness:.2f} (Higher = Better)\n"
        f"  - Stiffness: {stiffness:.2f} (Lower = Better)\n"
        f"  - Smoothness: {smoothness:.2f} (Higher = Better)\n\n"
        f"Mechanical Parameters:\n"
        f"  - Stretchiness: {stretchiness:.2f} (Higher = Better)\n"
        f"  - Elasticity: {elasticity:.2f} (Higher = Better)\n"
        f"  - Recovery: {recovery:.2f} (Higher = Better)\n"
        f"  - Durability: {durability:.2f} (Higher = Better)\n"
        f"  - Abrasion Resistance: {abrasion_resistance:.2f} (Higher = Better)\n"
    )
    return {
        "fiber_type": fiber_type,
        "weave_type": weave_type,
        "gsm": gsm,
        "softening_finish": softening_finish,
        "comfort_score": overall_score,
        "category_breakdown": category_breakdown,
        "detailed_analysis": detailed,
        "suggestions": suggestions_text
    }

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/analyzer', methods=['GET'])
def analyzer():
    fibers = list(fiber_data.keys())
    weaves = list(weave_data.keys())
    return render_template_string(ANALYZER_TEMPLATE, fibers=fibers, weaves=weaves)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    try:
        gsm = float(data.get('gsm'))
        fiber_type = data.get('fiber_type')
        weave_type = data.get('weave_type')
        softening_finish = bool(data.get('softening_finish'))
    except Exception:
        return jsonify({"error": "Invalid input data."})
    result = analyze_comfort(gsm, fiber_type, weave_type, softening_finish)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5050) 