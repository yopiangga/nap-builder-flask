from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

import src.extract_document as extract_document

app = Flask(__name__)
CORS(app)

# Route API
@app.route('/', methods=['GET'])
def get_data():
    try:
        df_table_a = pd.read_csv("./temp/df_table_a.csv", index_col=0)
        df_table_b = pd.read_csv("./temp/df_table_b.csv", index_col=0)
        df_table_c = pd.read_csv("./temp/df_table_c.csv", index_col=0)
        df_table_d = pd.read_csv("./temp/df_table_d.csv", index_col=0)
        df_table_ee = pd.read_csv("./temp/df_table_ee.csv", index_col=0)
        df_descriptive = pd.read_csv("./temp/df_descriptive.csv", index_col=0)

        return jsonify({
            "data": [
                df_table_a.to_dict(orient='records'),
                df_table_b.to_dict(orient='records'),
                df_table_c.to_dict(orient='records'),
                df_table_d.to_dict(orient='records'),
                df_table_ee.to_dict(orient='records'),
            ],
            "descriptive": df_descriptive.to_dict(orient='records')
        })
    except:
        path = [
        "./temp/Financial-Statement-Full-Year-2020.pdf",
        "./temp/Financial-Statement-Full-Year-2021.pdf",
        "./temp/FINAL-FS-UT-Tbk-31-December-2022.pdf",

        "./temp/FS-UNTR-0322.pdf",
        "./temp/FS-UNTR-0323.pdf"
    ]
        e = extract_document.ExtractDocument(path)
        e.upload()

        [a, b, c, d, ee, f]= e.main()

        # df = pd.concat([a, b, c, d, ee])

        a.to_csv("./temp/df_table_a.csv")
        b.to_csv("./temp/df_table_b.csv")
        c.to_csv("./temp/df_table_c.csv")
        d.to_csv("./temp/df_table_d.csv")
        ee.to_csv("./temp/df_table_ee.csv")
        f.to_csv("./temp/df_descriptive.csv")

        return jsonify({
            "data": [
                a.to_dict(orient='records'),
                b.to_dict(orient='records'),
                c.to_dict(orient='records'),
                d.to_dict(orient='records'),
                ee.to_dict(orient='records'),
            ],
            "descriptive": f.to_dict(orient='records')
        })
    

@app.route('/renew', methods=['GET'])
def get_new_data():
    path = [
        "./temp/Financial-Statement-Full-Year-2020.pdf",
        "./temp/Financial-Statement-Full-Year-2021.pdf",
        "./temp/FINAL-FS-UT-Tbk-31-December-2022.pdf",

        "./temp/FS-UNTR-0322.pdf",
        "./temp/FS-UNTR-0323.pdf"
    ]
    e = extract_document.ExtractDocument(path)
    e.upload()

    [a, b, c, d, ee, f]= e.main()

    # df = pd.concat([a, b, c, d, ee])

    a.to_csv("./temp/df_table_a.csv")
    b.to_csv("./temp/df_table_b.csv")
    c.to_csv("./temp/df_table_c.csv")
    d.to_csv("./temp/df_table_d.csv")
    ee.to_csv("./temp/df_table_ee.csv")
    f.to_csv("./temp/df_descriptive.csv")

    return jsonify({
        "data": [
            a.to_dict(orient='records'),
            b.to_dict(orient='records'),
            c.to_dict(orient='records'),
            d.to_dict(orient='records'),
            ee.to_dict(orient='records'),
        ],
        "descriptive": f.to_dict(orient='records')
    })


if __name__ == '__main__':
    app.run(debug=True)