from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Display pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/models')
def models():
    return render_template('models.html')

@app.route('/clustering')
def clustering():
    return render_template('clustering.html')

@app.route('/aws')
def aws():
    return render_template('aws.html')

# Route for executing models
@app.route('/run-model', methods=['POST'])
def run_model():
    data = request.json
    model_name = data.get('model')

    # Placeholder functions for model execution
    def run_andy_model():
        # Replace with the actual logic or script execution for Andy's model
        return "Results from Andy's model"

    def run_mason_model():
        # Replace with the actual logic or script execution for Mason's model
        return "Results from Mason's model"

    def run_nick_model():
        # Replace with the actual logic or script execution for Nick's model
        return "Results from Nick's model"

    # Execute the appropriate model based on the request
    if model_name == 'Andy':
        results = run_andy_model()
    elif model_name == 'Mason':
        results = run_mason_model()
    elif model_name == 'Nick':
        results = run_nick_model()
    else:
        return jsonify({'error': 'Invalid model selected'}), 400

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True)
