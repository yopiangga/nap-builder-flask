from flask import Flask, jsonify
import pandas as pd

import src.extract_document as extract_document

app = Flask(__name__)

# Route API
@app.route('/', methods=['GET'])
def get_data():
    path = [
    "./temp/Financial-Statement-Full-Year-2020.pdf",
    "./temp/Financial-Statement-Full-Year-2021.pdf",
    "./temp/FINAL-FS-UT-Tbk-31-December-2022.pdf",

    "./temp/FS-UNTR-0322.pdf",
    "./temp/FS-UNTR-0323.pdf"
]
    e = extract_document.ExtractDocument(path)
    e.upload()
    # df = e.get_genai_extract("aset_lancar")
    [a, b, c, d, ee]= e.main()

    df = pd.concat([a, b, c, d, ee])

    return jsonify(df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)