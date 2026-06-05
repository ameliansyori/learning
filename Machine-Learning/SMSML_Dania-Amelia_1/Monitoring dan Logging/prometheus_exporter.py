import time
import random
from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter, Histogram, Gauge

app = Flask(__name__)

# Mendaftarkan 5 Metriks Berbeda untuk syarat SKILLED
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
REQUEST_LATENCY = Histogram('api_model_latency_seconds', 'Latensi API Model dalam Detik')
CPU_USAGE = Gauge('system_cpu_usage', 'Penggunaan CPU dalam Persen')
RAM_USAGE = Gauge('system_ram_usage', 'Penggunaan RAM dalam Megabyte')
MODEL_ERROR_COUNT = Counter('model_prediction_errors_total', 'Total Eror pada Prediksi Model')

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    # Simulasi pembacaan sistem monitoring
    CPU_USAGE.set(random.uniform(20.0, 80.0))
    RAM_USAGE.set(random.uniform(100.0, 500.0))
    
    try:
        data = request.get_json()
        time.sleep(random.uniform(0.01, 0.2)) # Simulasi latensi
        
        if not data:
            raise ValueError("Data kosong")
            
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
        return jsonify({"status": "success", "prediction": 1})
        
    except Exception as e:
        MODEL_ERROR_COUNT.inc()
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5002)
