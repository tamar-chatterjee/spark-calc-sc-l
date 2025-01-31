from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

machine_options = {
    
    "8 Cores | 32GB RAM | NVIDIA A10": 0.69,
    "16 Cores | 32GB RAM | AMD EPYC 7R13": 0.33,
    "16 Cores | 64GB RAM | NVIDIA A10": 0.95,
    "32 Cores | 64GB RAM | AMD EPYC 7R13": 0.69,
    "32 Cores | 128GB RAM | NVIDIA A10": 1.29,
    "64 Cores | 128GB RAM | AMD EPYC 7R13": 1.35,
}

@app.route('/')
def index():
    default_machine = "Starter Kit 1 | 4 Cores | 16GB RAM | NVIDIA T4 16 GB VRAM"
    return render_template('index.html', machine_options=machine_options, default_machine=default_machine)

@app.route('/calculate', methods=['POST'])
def calculate():
    num_devs = int(request.form['num_devs'])
    on_prem_cost_per_dev = float(request.form['on_prem_cost_per_dev'])
    annual_maint_costs = float(request.form['annual_maint_costs'])
    frames = int(request.form['frames'])
    minutes_per_frame = float(request.form['minutes_per_frame'])
    smart_compute_nodes = int(request.form['smart_compute_nodes'])
    spark_prostation = request.form['spark_prostation']

    print(f"Received Data:")
    print(f" - num_devs: {num_devs}")
    print(f" - on_prem_cost_per_dev: {on_prem_cost_per_dev}")
    print(f" - annual_maint_costs: {annual_maint_costs}")
    print(f" - frames: {frames}")
    print(f" - minutes_per_frame: {minutes_per_frame}")
    print(f" - smart_compute_nodes: {smart_compute_nodes}")
    print(f" - spark_prostation: {spark_prostation}")

    compute_hours = (frames * minutes_per_frame) / 60
    on_prem_time = compute_hours / num_devs
    total_on_prem_cost = (on_prem_cost_per_dev * num_devs) + annual_maint_costs
    print(f"Total On-Prem Cost: {total_on_prem_cost}")

    machine_cost_per_hour = machine_options[spark_prostation]
    machine_cost_per_hour *= 0.35
    spark_time = compute_hours / smart_compute_nodes
    spark_cost = smart_compute_nodes * spark_time * machine_cost_per_hour

    time_on_prem_display = f"{on_prem_time:.2f} hours"
    if on_prem_time > 72:
        days = int(on_prem_time // 24)
        time_on_prem_display += f" [ {days} days ]"

    return jsonify({
        'on_prem_cost': total_on_prem_cost,
        'time_on_prem': time_on_prem_display,
        'cloud_cost': spark_cost,
        'time_spark': spark_time
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)