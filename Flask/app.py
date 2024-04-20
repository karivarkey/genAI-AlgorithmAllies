from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Enable auto-reload in development
app.config['TEMPLATES_FOLDER'] = '/home/karivarkey/code/genAI-AlgorithmAllies/Flask/static'  # Set the template folder path
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)