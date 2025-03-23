import google.generativeai as genai
import json
import pandas as pd
import os
from googlesearch import search
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class ExtractDocument():
    def __init__(self, path):
        self.path = path
        self.online_path = []
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def upload(self):
        res_path = []
        for p in self.path:
            res = genai.upload_file(path=p)
            res_path.append(res)
        self.online_path = res_path

    def get_online_path(self):
        return self.online_path

    def get_promt(self, section):
        p1 = """
            You are business analyst asisstant of bank for review financing corporate.

            Performance keuangan audited PT United Tractors Tbk (Konsolidasi) Desember 2020, Desember 2021, Desember 2022.
        
            In Financial statement Document, use left section only for extracting data. 
            The language is Bahasa.
        
            Make schema data for 'aset lancar'. 
            List all data include sub list.
            Give only 'title' and 'value_year_2020', 'value_year_2021', 'value_year_2022'.
            Value must be integer with real number without formating.
        
            Return only json value schema, 1 dimension array.

            example :
            [
                {
                    title: str,
                    value_year_2020: int,
                    value_year_2021: int,
                    value_year_2022: int
                }
            ]
        """

        p2 = """
            You are business analyst asisstant of bank for review financing corporate.
        
            Performance keuangan audited PT United Tractors Tbk (Konsolidasi) Desember 2020, Desember 2021, Desember 2022.
        
            Make schema data for 'aset tidak lancar'. 
            List all data include sub list.
            Give only 'title' and 'value_year_2020', 'value_year_2021', 'value_year_2022'.
            Value must be integer with real number without formating.
        
            Return only json value schema, 1 dimension array.

            example :
            [
                {
                    title: str,
                    value_year_2020: int,
                    value_year_2021: int,
                    value_year_2022: int
                }
            ]
        """

        p3 = """
            You are business analyst asisstant of bank for review financing corporate.

            Performance keuangan audited PT United Tractors Tbk (Konsolidasi) Desember 2020, Desember 2021, Desember 2022.
        
            Make schema data for 'liabilitas jangka pendek'. 
            List all data include sub list.
            Give only 'title' and 'value_year_2020', 'value_year_2021', 'value_year_2022'.
            Value must be integer with real number without formating.
            
            Return only json value schema, 1 dimension array.

            example :
            [
                {
                    title: str,
                    value_year_2020: int,
                    value_year_2021: int,
                    value_year_2022: int
                }
            ]
        """

        p4 = """
            You are business analyst asisstant of bank for review financing corporate.

            Performance keuangan audited PT United Tractors Tbk (Konsolidasi) Desember 2020, Desember 2021, Desember 2022..
        
            Make schema data for 'liabilitas jangka panjang'. 
            List all data include sub list.
            Give only 'title' and 'value_year_2020', 'value_year_2021', 'value_year_2022'.
            Value must be integer with real number without formating.
        
            Return only json value schema, 1 dimension array.

            example :
            [
                {
                    title: str,
                    value_year_2020: int,
                    value_year_2021: int,
                    value_year_2022: int
                }
            ]
        """

        p5 = """
            You are business analyst asisstant of bank for review financing corporate.

            Performance keuangan audited PT United Tractors Tbk (Konsolidasi) Desember 2020, Desember 2021, Desember 2022..
        
            Make schema data for 'ekuitas'. 
            List all data include sub list.
            Give only 'title' and 'value_year_2020', 'value_year_2021', 'value_year_2022'.
            Value must be integer with real number without formating.
        
            Return only json value schema, 1 dimension array.

            example :
            [
                {
                    title: str,
                    value_year_2020: int,
                    value_year_2021: int,
                    value_year_2022: int
                }
            ]
        """

        if section == "aset_lancar":
            return p1
        elif section == "aset_tidak_lancar":
            return p2
        elif section == "liabilitas_jangka_pendek":
            return p3
        elif section == "liabilitas_jangka_panjang":
            return p4
        elif section == "ekuitas":
            return p5
        else:
            return ""
    
    def get_genai_extract(self, section):
        promt = self.get_promt(section)
        response = self.model.generate_content(self.online_path + [promt])

        json_string = response.text
        clean_json_string = json_string.strip("```json\n").strip("```")
        json_data = json.loads(clean_json_string)
        df_json = pd.DataFrame(json_data)

        return df_json[["title", "value_year_2020", "value_year_2021", "value_year_2022"]]

    def get_summ(self, df_json):
        df_summ = df_json.copy()
        df_summ["akumulasi"] = df_summ.apply(lambda x: x["value_year_2020"] + x["value_year_2021"] + x["value_year_2022"], axis=1)
        
        df_summ = df_summ.sort_values(by="akumulasi", ascending=False)

        df_largest = df_summ.nlargest(3, 'akumulasi')
        df_sisa = df_summ[~df_summ.index.isin(df_largest.index)]
        
        df_with_other = df_largest.copy()
        df_with_other.drop(columns=["akumulasi"], inplace=True)
        s1, s2, s3 = [df_sisa["value_year_2020"].sum(), df_sisa["value_year_2021"].sum(), df_sisa["value_year_2022"].sum()]
        
        df_s = pd.DataFrame(columns=["title", "value_year_2020", "value_year_2021", "value_year_2022"])
        df_s["title"] = ["Lainnya"]
        df_s["value_year_2020"] = [s1]
        df_s["value_year_2021"] = [s2]
        df_s["value_year_2022"] = [s3]
        
        df_with_other = pd.concat([df_with_other, df_s])
        
        df_temp = pd.DataFrame(columns=["title", "value_year_2020", "value_year_2021", "value_year_2022"])
        df_temp["title"] = ["Total"]
        t1, t2, t3 = [df_with_other["value_year_2020"].sum(), df_with_other["value_year_2021"].sum(), df_with_other["value_year_2022"].sum()]
        df_temp["value_year_2020"] = [t1]
        df_temp["value_year_2021"] = [t2]
        df_temp["value_year_2022"] = [t3]
        
        df_with_other = pd.concat([df_with_other, df_temp])
        
        return df_with_other
    
    def get_descriptive_analyst(self, data, link):
        promt = """
           Jelaskan data laporan keuangan dari UNTR berikut ini
            Data: 
            {0}
            
            Gunakan data dari referensi berita untuk menjelaskan data yang ada, jika tidak ada maka gunakan laporan keuangan sebagai penjelasan mengapa hal itu terjadi.
        

            """.format(data, link)

        promt = promt + \
            """
            Return json data only.
            
            return schema:
            [
                {
                    title: str,
                    description: str,
                    reference: str
                }
            ]
            """

        response = self.model.generate_content(self.online_path + link + [promt])
        return response 

    def news_reference(self):
        link = []
        for j in search("UNTR Financial News 2020 - 2022", sleep_interval=2, num_results=20):
            link.append(j)
        return link
    
    def main(self):
        aset_lancar = self.get_genai_extract("aset_lancar")
        aset_tidak_lancar = self.get_genai_extract("aset_tidak_lancar")
        liabilitas_jangka_pendek = self.get_genai_extract("liabilitas_jangka_pendek")
        liabilitas_jangka_panjang = self.get_genai_extract("liabilitas_jangka_panjang")
        ekuitas = self.get_genai_extract("ekuitas")

        aset_lancar_summ = self.get_summ(aset_lancar)
        aset_tidak_lancar_summ = self.get_summ(aset_tidak_lancar)
        liabilitas_jangka_pendek_summ = self.get_summ(liabilitas_jangka_pendek)
        liabilitas_jangka_panjang_summ = self.get_summ(liabilitas_jangka_panjang)
        ekuitas_summ = self.get_summ(ekuitas)

        df_data = pd.concat([
            aset_lancar, aset_tidak_lancar,
            liabilitas_jangka_panjang, liabilitas_jangka_pendek,
            ekuitas
        ])

        links = self.news_reference()

        descriptive = self.get_descriptive_analyst(str(df_data.to_dict(orient='records')), links)
        json_string = descriptive.text
        clean_json_string = json_string.strip("```json\n").strip("```")
        json_data = json.loads(clean_json_string)
        df_descriptive = pd.DataFrame(json_data)

        return [aset_lancar_summ, aset_tidak_lancar_summ, liabilitas_jangka_panjang_summ, liabilitas_jangka_pendek_summ, ekuitas_summ, df_descriptive]
            