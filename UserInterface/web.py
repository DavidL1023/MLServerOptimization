from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle form submission
        algorithm = request.form.get('algorithm')
        # Perform specified algorithm and output results
        result = "Algorithm Results"

        return render_template('web.html', result=result)

    return render_template('web.html')

if __name__ == '__main__':
    app.run()
