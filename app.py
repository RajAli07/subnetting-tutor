from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# FRONTEND TEMPLATE (HTML + CSS + JS)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Subnetting Tutor | Decimal & Binary Mapping</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #0f172a; }
        
        .fade-in { animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(15px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        .glass-card {
            background: white;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            border-radius: 16px;
        }
        
        .teacher-notes::-webkit-scrollbar { width: 6px; }
        .teacher-notes::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 8px; }
        .teacher-notes::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 8px; }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4 sm:p-6 py-12">

    <div class="max-w-4xl w-full">
        <div class="text-center mb-8 fade-in" style="animation-delay: 0.1s;">
            <h1 class="text-4xl font-bold tracking-tight text-slate-800 mb-2">Network Subnetting Tutor</h1>
            <p class="text-slate-500 text-base">Enter an IPv4 address to learn deep subnetting architecture with step-by-step mapping.</p>
        </div>

        <div class="glass-card p-6 sm:p-8 mb-6 fade-in" style="animation-delay: 0.2s;">
            <form id="ipForm" class="flex flex-col sm:flex-row gap-4 mb-2">
                <input type="text" id="ipInput" placeholder="e.g., 192.168.1.45" required
                    pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
                    class="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg transition-all"
                    title="Please enter a valid IPv4 address">
                <button type="submit" 
                    class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-lg shadow-sm transition-all flex items-center justify-center gap-2 min-w-[150px]">
                    <span>Analyze IP</span>
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </button>
            </form>
            <p id="errorMsg" class="text-red-500 text-sm hidden mt-2">Invalid IP format. Values must be 0-255.</p>
        </div>

        <div id="resultSection" class="hidden space-y-6">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="glass-card p-5 fade-in" style="animation-delay: 0.3s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Network Class</p>
                    <p id="resClass" class="text-2xl font-bold text-blue-600">Class -</p>
                </div>
                <div class="glass-card p-5 fade-in" style="animation-delay: 0.4s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Default Subnet Mask</p>
                    <p id="resSubnet" class="text-2xl font-bold text-slate-700">-</p>
                </div>
                <div class="glass-card p-5 fade-in" style="animation-delay: 0.5s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">IP Type</p>
                    <p id="resType" class="text-2xl font-bold text-slate-700">-</p>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="glass-card p-5 border-l-4 border-l-indigo-500 fade-in" style="animation-delay: 0.55s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Network ID</p>
                    <p id="resNetID" class="text-xl font-bold text-slate-800">-</p>
                </div>
                <div class="glass-card p-5 border-l-4 border-l-emerald-500 fade-in" style="animation-delay: 0.6s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">First Host ID</p>
                    <p id="resFirstHost" class="text-xl font-bold text-slate-800">-</p>
                </div>
                <div class="glass-card p-5 border-l-4 border-l-amber-500 fade-in" style="animation-delay: 0.65s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Last Host ID</p>
                    <p id="resLastHost" class="text-xl font-bold text-slate-800">-</p>
                </div>
                <div class="glass-card p-5 border-l-4 border-l-rose-500 fade-in" style="animation-delay: 0.7s;">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Broadcast ID</p>
                    <p id="resBroadcast" class="text-xl font-bold text-slate-800">-</p>
                </div>
            </div>

            <div class="glass-card p-6 sm:p-8 fade-in" style="animation-delay: 0.75s;">
                <h2 class="text-lg font-semibold text-slate-800 mb-4 border-b pb-2">Complete 32-Bit Binary Address</h2>
                <div id="resBinary" class="font-mono text-lg sm:text-2xl text-center tracking-widest text-slate-700 bg-slate-50 py-4 rounded-lg border border-slate-100">
                    </div>
            </div>

            <div class="glass-card p-6 sm:p-8 bg-blue-50/40 border-blue-100 fade-in" style="animation-delay: 0.8s;">
                <div class="flex items-center gap-3 mb-4">
                    <div class="bg-blue-100 text-blue-600 p-2 rounded-lg">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                    </div>
                    <h2 class="text-lg font-semibold text-slate-800">Teacher's Slate: Visual Mapping & Logic</h2>
                </div>
                <div id="resExplanation" class="teacher-notes text-slate-600 space-y-6 max-h-[500px] overflow-y-auto pr-2 text-sm leading-relaxed">
                    </div>
            </div>
        </div>
    </div>
<!-- Watermark Footer -->
        <div class="mt-12 mb-4 text-center fade-in" style="animation-delay: 0.85s;">
            <p class="text-sm text-slate-500">
                Developed by <a href="https://rajali01.pythonanywhere.com/" target="_blank" class="font-semibold text-blue-600 hover:text-blue-700 hover:underline transition-all">raaZ© ❤️</a>
                <span class="mx-2 text-slate-300">|</span> 
                <a href="https://rajali01.pythonanywhere.com/" target="_blank" class="font-medium text-slate-500 hover:text-slate-800 transition-all">Portfolio</a>
            </p>
        </div>
    <script>
        document.getElementById('ipForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const ip = document.getElementById('ipInput').value;
            const errorMsg = document.getElementById('errorMsg');
            const resultSection = document.getElementById('resultSection');

            const octets = ip.split('.');
            const isValid = octets.every(num => parseInt(num) >= 0 && parseInt(num) <= 255);
            
            if (!isValid) {
                errorMsg.classList.remove('hidden');
                resultSection.classList.add('hidden');
                return;
            }
            errorMsg.classList.add('hidden');

            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ip: ip })
                });
                
                const data = await response.json();
                if(data.error) throw new Error(data.error);

                // Meta data
                document.getElementById('resClass').textContent = `Class ${data.class}`;
                document.getElementById('resSubnet').textContent = data.subnet;
                document.getElementById('resType').textContent = data.type;
                
                // Boundaries data
                document.getElementById('resNetID').textContent = data.net_id;
                document.getElementById('resFirstHost').textContent = data.first_host;
                document.getElementById('resLastHost').textContent = data.last_host;
                document.getElementById('resBroadcast').textContent = data.broadcast;
                
                // Binary view formatting
                const binaryHTML = data.binary.split('.').map((bin, index) => 
                    `<span class="${index === 0 ? 'text-blue-600 font-bold' : 'text-slate-700'}">${bin}</span>`
                ).join('<span class="text-slate-300">.</span>');
                document.getElementById('resBinary').innerHTML = binaryHTML;

                // Explanation payload
                document.getElementById('resExplanation').innerHTML = data.explanation;

                // Layout transition
                resultSection.classList.remove('hidden');
                
                // Reset standard animations smoothly
                const animatedElements = resultSection.querySelectorAll('.fade-in');
                animatedElements.forEach(el => {
                    el.style.animation = 'none';
                    el.offsetHeight; 
                    el.style.animation = null; 
                });

            } catch (err) {
                alert("Subnet evaluation error: " + err.message);
            }
        });
    </script>
</body>
</html>
"""

# ==========================================
# BACKEND LOGIC (Python Flask API)
# ==========================================

def get_class_boundaries(octets):
    """Calculates Network ID, Hosts, and Broadcast based on traditional class parameters."""
    first = octets[0]
    
    if 1 <= first <= 126:
        net_class = "A"
        subnet = "255.0.0.0"
        itype = "Private" if first == 10 else "Public"
        
        net_id = f"{octets[0]}.0.0.0"
        first_host = f"{octets[0]}.0.0.1"
        last_host = f"{octets[0]}.255.255.254"
        broadcast = f"{octets[0]}.255.255.255"
        
    elif 128 <= first <= 191:
        net_class = "B"
        subnet = "255.255.0.0"
        itype = "Private" if (first == 172 and 16 <= octets[1] <= 31) else "Public"
        
        net_id = f"{octets[0]}.{octets[1]}.0.0"
        first_host = f"{octets[0]}.{octets[1]}.0.0.1" if first_host_is_custom(0) else f"{octets[0]}.{octets[1]}.0.1"
        last_host = f"{octets[0]}.{octets[1]}.255.254"
        broadcast = f"{octets[0]}.{octets[1]}.255.255"
        
    elif 192 <= first <= 223:
        net_class = "C"
        subnet = "255.255.255.0"
        itype = "Private" if (first == 192 and octets[1] == 168) else "Public"
        
        net_id = f"{octets[0]}.{octets[1]}.{octets[2]}.0"
        first_host = f"{octets[0]}.{octets[1]}.{octets[2]}.1"
        last_host = f"{octets[0]}.{octets[1]}.{octets[2]}.254"
        broadcast = f"{octets[0]}.{octets[1]}.{octets[2]}.255"
        
    elif first == 127:
        return "Loopback", "255.0.0.0", "Localhost", "127.0.0.0", "127.0.0.1", "127.255.255.254", "127.255.255.255"
    elif 224 <= first <= 239:
        return "D", "N/A", "Multicast Address", "N/A", "N/A", "N/A", "N/A"
    else:
        return "E", "N/A", "Experimental", "N/A", "N/A", "N/A", "N/A"

    return net_class, subnet, itype, net_id, first_host, last_host, broadcast

def generate_mapped_explanation(octets, net_class, net_id, first_host, last_host, broadcast, subnet_mask):
    """Generates an intuitive, deeply mapped classroom explanation with true step-by-step trace."""
    
    # Helper binary converter
    to_bin = lambda x: format(int(x), '08b')
    
    ip_str = " . ".join(map(str, octets))
    ip_bin = " . ".join([to_bin(x) for x in octets])
    mask_bin = " . ".join([to_bin(x) for x in subnet_mask.split('.')]) if net_class in ['A','B','C'] else ""

    html = f"<div class='space-y-4'>"
    html += f"<p class='text-slate-700 font-medium text-base'>Classroom mein welcome! Chalo aapke IP address <strong>{'.'.join(map(str, octets))}</strong> ko board par breakdown karte hain.</p>"
    
    # Section 1: Decimal to Binary Mapping
    html += f"<div class='bg-white p-4 rounded-xl border border-slate-100 shadow-sm'>"
    html += f"<h4 class='font-bold text-slate-800 text-sm uppercase tracking-wide mb-3 text-blue-600'>Step 1: Complete Address Mapping (Decimal ⟷ Binary)</h4>"
    html += f"<div class='font-mono bg-slate-900 text-slate-200 p-4 rounded-lg space-y-2 text-xs sm:text-sm overflow-x-auto'>"
    html += f"<div>[DECIMAL]: {ip_str}</div>"
    html += f"<div class='text-emerald-400'>[BINARY] : {ip_bin}</div>"
    html += f"</div>"
    html += f"<p class='text-xs text-slate-500 mt-2'>Har ek decimal block (octet) ko exact 8 bits ke standard window mein compute kiya gaya hai.</p>"
    html += f"</div>"

    if net_class not in ['A', 'B', 'C']:
        html += f"<p class='p-3 bg-amber-50 rounded border text-amber-700'>Class {net_class} architectures generally standard end-user host subnetting parameters follow nahi karti hain.</p></div>"
        return html

    # Section 2: Mathematical Calculations
    html += f"<div class='bg-white p-4 rounded-xl border border-slate-100 shadow-sm space-y-4'>"
    html += f"<h4 class='font-bold text-slate-800 text-sm uppercase tracking-wide text-blue-600'>Step 2: Core Subnet Boundaries Ki Calculation</h4>"
    
    # Network ID logic
    html += f"<div class='space-y-1'>"
    html += f"<p class='font-semibold text-slate-800 text-sm'>1. Network ID ({net_id}) kaise bani?</p>"
    html += f"<p class='text-slate-600 text-xs sm:text-sm'>Class {net_class} ke rules ke hisaab se, Network bits ko unchanged rakha jata hai aur saari Host bits ko <strong>0</strong> mein badal diya jata hai:</p>"
    html += f"<div class='font-mono bg-slate-50 p-3 rounded text-xs sm:text-sm text-slate-700 border border-dashed'>"
    html += f"IP Binary: {ip_bin}<br>"
    html += f"Mask Bin : {mask_bin}<br>"
    html += f"<span class='text-indigo-600 font-bold'>Net ID   : {' . '.join([to_bin(x) for x in net_id.split('.')])} ⟶ {net_id}</span>"
    html += f"</div>"
    html += f"</div>"
    
    # First Host logic
    html += f"<div class='space-y-1 mt-4'>"
    html += f"<p class='font-semibold text-slate-800 text-sm'>2. First Host ID ({first_host}) kaise bani?</p>"
    html += f"<p class='text-slate-600 text-xs sm:text-sm'>Network ID kabhi kisi machine ko nahi di ja sakti, isliye valid systems ke liye pehla upyog hone wala address hamesha <strong>Network ID + 1</strong> hota hai:</p>"
    html += f"<div class='font-mono bg-slate-50 p-3 rounded text-xs sm:text-sm text-slate-700 border border-dashed'>"
    html += f"Net ID Binary: {' . '.join([to_bin(x) for x in net_id.split('.')])}<br>"
    html += f"<span class='text-emerald-600 font-bold'>First Host   : {' . '.join([to_bin(x) for x in first_host.split('.')])} ⟶ {first_host}</span>"
    html += f"</div>"
    html += f"</div>"

    # Broadcast ID logic
    html += f"<div class='space-y-1 mt-4'>"
    html += f"<p class='font-semibold text-slate-800 text-sm'>3. Broadcast ID ({broadcast}) kaise bani?</p>"
    html += f"<p class='text-slate-600 text-xs sm:text-sm'>Pure segment mein data sabhi ko ek saath bhejne ke liye, architecture ke mutabik network hissa waise hi chhod kar saari host bits ko binary <strong>1</strong> par configure kar dete hain:</p>"
    html += f"<div class='font-mono bg-slate-50 p-3 rounded text-xs sm:text-sm text-slate-700 border border-dashed'>"
    html += f"IP Binary   : {ip_bin}<br>"
    html += f"<span class='text-rose-600 font-bold'>Broadcast ID: {' . '.join([to_bin(x) for x in broadcast.split('.')])} ⟶ {broadcast}</span>"
    html += f"</div>"
    html += f"</div>"

    # Last Host logic
    html += f"<div class='space-y-1 mt-4'>"
    html += f"<p class='font-semibold text-slate-800 text-sm'>4. Last Host ID ({last_host}) kaise bani?</p>"
    html += f"<p class='text-slate-600 text-xs sm:text-sm'>Kyunki aakhri dynamic configuration Broadcast ke liye reserved hoti hai, usse thik pehla chalne wala single node network ka aakhri live user banta hai <strong>(Broadcast ID - 1)</strong>:</p>"
    html += f"<div class='font-mono bg-slate-50 p-3 rounded text-xs sm:text-sm text-slate-700 border border-dashed'>"
    html += f"Broadcast Bin: {' . '.join([to_bin(x) for x in broadcast.split('.')])}<br>"
    html += f"<span class='text-amber-600 font-bold'>Last Host ID : {' . '.join([to_bin(x) for x in last_host.split('.')])} ⟶ {last_host}</span>"
    html += f"</div>"
    html += f"</div>"

    html += f"</div></div>"
    return html

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    ip = data.get('ip', '')
    
    try:
        octets = [int(x) for x in ip.split('.')]
        if len(octets) != 4 or any(x < 0 or x > 255 for x in octets):
            return jsonify({"error": "Invalid IP Address components"}), 400
            
        binary_octets = [format(x, '08b') for x in octets]
        binary_ip = '.'.join(binary_octets)
        
        # Calculate deep networking architectures
        net_class, subnet, ip_type, net_id, first_host, last_host, broadcast = get_class_boundaries(octets)
        
        # UI Native classroom compiler
        explanation = generate_mapped_explanation(octets, net_class, net_id, first_host, last_host, broadcast, subnet)
        
        return jsonify({
            "class": net_class,
            "subnet": subnet,
            "type": ip_type,
            "binary": binary_ip,
            "net_id": net_id,
            "first_host": first_host,
            "last_host": last_host,
            "broadcast": broadcast,
            "explanation": explanation
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)