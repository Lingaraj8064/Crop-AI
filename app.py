from flask import Flask, render_template, request
from markupsafe import Markup
from model import predict_image
import utils   # corrected: "u ls" → "utils"
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                logger.warning("No file part in the request")
                return render_template('index.html', error="No file selected")
            
            file = request.files['file']
            
            if file.filename == '':
                logger.warning("No file selected")
                return render_template('index.html', error="No file selected")
            
            # Read and predict
            img = file.read()
            prediction = predict_image(img)   # fixed spelling
            logger.info(f"Prediction: {prediction}")
            
            # Check if prediction exists in the dictionary
            if prediction not in utils.disease_dic:
                logger.error(f"Prediction '{prediction}' not found in disease dictionary")
                return render_template('index.html', error="Unknown prediction result")
            
            result = Markup(utils.disease_dic[prediction])
            return render_template('display.html', result=result)
        
        except Exception as e:   # fixed spelling
            logger.error(f"Error during prediction: {str(e)}", exc_info=True)
            return render_template('index.html', error="An error occurred during processing")
    
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
