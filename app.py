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

ANALYZER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabric Comfort Analyzer</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background: #f7fafd;
            min-height: 100vh;
            font-family: 'Montserrat', Arial, sans-serif;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .main-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 2px 16px #0001;
            padding: 2.2rem 1.5rem 1.5rem 1.5rem;
            max-width: 50%;
            width: 100%;
        }
        .main-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #2563eb;
            margin-bottom: 1.2rem;
            text-align: center;
        }
        .input-form {
            display: flex;
            flex-direction: column;
            gap: 1.1rem;
            margin-bottom: 1.5rem;
        }
        .input-label {
            font-size: 1.02rem;
            color: #2563eb;
            font-weight: 600;
            margin-bottom: 0.3rem;
            text-align: left;
        }
        .form-control {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .input-field, .input-select {
            width: 100%;
            min-width: 0;
            box-sizing: border-box;
            padding: 0.7rem 1rem;
            border-radius: 8px;
            border: 1.5px solid #e0eafc;
            font-size: 1.05rem;
            background: #f7fafd;
            transition: border 0.2s;
        }
        .input-field:focus, .input-select:focus {
            border: 1.5px solid #2563eb;
            outline: none;
        }
        .checkbox-row {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.5rem;
        }
        .analyze-btn {
            background: #2563eb;
            color: #fff;
            font-size: 1.12rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 0;
            margin-top: 0.5rem;
            cursor: pointer;
            transition: background 0.2s;
            width: 100%;
        }
        .analyze-btn:hover {
            background: #1746a0;
        }
        .result-section {
            margin-top: 2.2rem;
            text-align: left;
        }
        .donut-charts-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin: 1.5rem 0 1.5rem 0;
            flex-wrap: wrap;
            gap: 1.2rem;
            padding: 0 1rem 0 1rem
        }
        .donut-chart-container {
            width: 110px;
            text-align: center;
        }
        .donut-label {
            font-size: 1.02rem;
            font-weight: 600;
            color: #2563eb;
            margin-top: 0.5rem;
        }
        .donut-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #222;
            margin-top: 0.2rem;
        }
        .result-details {
            font-size: 0.98rem;
            color: #555;
            background: #f7fafd;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1.1rem;
        }
        .export-btn {
            background: #2563eb;
            color: #fff;
            font-size: 1.02rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.7rem 1.5rem;
            margin-top: 1.1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        .export-btn:hover {
            background: #1746a0;
        }
        .footer {
            color: #b2bec3;
            font-size: 0.95rem;
            text-align: center;
            margin-top: 2.2rem;
        }
        @media (max-width: 700px) {
            .main-card { padding: 1rem; max-width: 100vw; }
            .donut-charts-row { flex-direction: column; align-items: center; gap: 1.5rem; }
            .donut-chart-container { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="main-title">Fabric Comfort Analyzer</div>
        <form id="comfortForm" class="input-form">
            <div class="form-control">
                <label for="gsm" class="input-label">GSM (g/m²)</label>
                <input type="number" class="input-field" id="gsm" name="gsm" min="50" max="500" value="150" required placeholder="50-500">
            </div>
            <div class="form-control">
                <label for="fiberType" class="input-label">Fiber Type</label>
                <select class="input-select" id="fiberType" name="fiberType" required>
                    {% for fiber in fibers %}
                    <option value="{{ fiber }}">{{ fiber }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-control">
                <label for="weaveType" class="input-label">Weave Type</label>
                <select class="input-select" id="weaveType" name="weaveType" required>
                    {% for weave in weaves %}
                    <option value="{{ weave }}">{{ weave }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="checkbox-row">
                <input class="form-check-input" type="checkbox" id="softeningFinish" name="softeningFinish" style="accent-color:#2563eb;">
                <label class="form-check-label" for="softeningFinish" style="color:#444;font-size:1.01rem;">Softening Finish</label>
            </div>
            <button type="submit" class="analyze-btn">Analyze</button>
        </form>
        <div id="resultSection" class="result-section" style="display:none;">
            <div class="donut-charts-row">
                <div class="donut-chart-container">
                    <canvas id="donutPhysical"></canvas>
                    <div class="donut-label">Physical</div>
                    <div class="donut-value" id="valPhysical"></div>
                </div>
                <div class="donut-chart-container">
                    <canvas id="donutSensory"></canvas>
                    <div class="donut-label">Sensory</div>
                    <div class="donut-value" id="valSensory"></div>
                </div>
                <div class="donut-chart-container">
                    <canvas id="donutMechanical"></canvas>
                    <div class="donut-label">Mechanical</div>
                    <div class="donut-value" id="valMechanical"></div>
                </div>
                <div class="donut-chart-container">
                    <canvas id="donutPsychological"></canvas>
                    <div class="donut-label">Psychological</div>
                    <div class="donut-value" id="valPsychological"></div>
                </div>
            </div>
            <div id="resultDetails" class="result-details" style="display:none;"></div>
            <button id="exportBtn" class="export-btn" style="display:none;">Download Report</button>
        </div>
        <div class="footer">© 2024 Fabric Analyzer</div>
    </div>
    <script>
    let donutCharts = {};
    let lastResultText = '';
    document.getElementById('comfortForm').addEventListener('submit', function(e) {
        e.preventDefault();
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
                alert(data.error);
                return;
            }
            document.getElementById('resultSection').style.display = 'block';
            // Donut charts for each category
            const breakdown = data.category_breakdown;
            const chartData = [
                { id: 'donutPhysical', val: breakdown.Physical, color: '#2563eb', label: 'Physical', valId: 'valPhysical' },
                { id: 'donutSensory', val: breakdown.Sensory, color: '#38a1f9', label: 'Sensory', valId: 'valSensory' },
                { id: 'donutMechanical', val: breakdown.Mechanical, color: '#fda085', label: 'Mechanical', valId: 'valMechanical' },
                { id: 'donutPsychological', val: breakdown.Psychological, color: '#b388ff', label: 'Psychological', valId: 'valPsychological' }
            ];
            chartData.forEach(cd => {
                if (donutCharts[cd.id]) donutCharts[cd.id].destroy();
                const ctx = document.getElementById(cd.id).getContext('2d');
                donutCharts[cd.id] = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: [cd.label, ''],
                        datasets: [{
                            data: [cd.val, 100-cd.val],
                            backgroundColor: [cd.color, '#e0eafc'],
                            borderWidth: 2,
                            borderColor: '#fff',
                        }]
                    },
                    options: {
                        cutout: '70%',
                        plugins: {
                            legend: { display: false },
                            tooltip: { enabled: false }
                        }
                    }
                });
                document.getElementById(cd.valId).textContent = cd.val.toFixed(1) + '%';
            });
            // Details
            let details = `<b>Fiber:</b> ${data.fiber_type} | <b>Weave:</b> ${data.weave_type} | <b>GSM:</b> ${data.gsm}<br>`;
            details += `<b>Softening Finish:</b> ${data.softening_finish ? 'Yes' : 'No'}<br><br>`;
            details += `<b>Analysis:</b><br><pre style='font-size:1em;'>${data.detailed_analysis}</pre>`;
            details += `<b>Suggestions:</b><br>`;
            if (data.suggestions.length > 0) {
                details += `<ol style='margin:0 0 0 1.2em;'>`;
                for (const s of data.suggestions) {
                    details += `<li>${s}</li>`;
                }
                details += `</ol>`;
            } else {
                details += `<span>- Fabric properties are well-balanced for comfort</span>`;
            }
            lastResultText = details.replace(/<[^>]+>/g, '');
            document.getElementById('resultDetails').innerHTML = details;
            document.getElementById('resultDetails').style.display = 'block';
            document.getElementById('exportBtn').style.display = 'inline-block';
        })
        .catch(err => {
            alert('Error during analysis.');
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