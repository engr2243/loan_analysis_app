## Main Functions
import os
import json
from utils.utility import load_js
from document_ext import Data_extractor
from ai_tool import ai_tool

cwd = os.getcwd()

class analyse:
    def __init__(self, loan_app_name, cr_name, il_name):
        self.loan_app_name = loan_app_name
        self.cr_name = cr_name
        self.il_name = il_name

        self.loan_app_tables = None
        self.industrial_licence = None
        self.commercial_license = None
        self.market_data = None
        self.prompts = None
        self.ai_agent = ai_tool()
        self.get_results = self.go()

    def load_rdata(self):
        # Assuming load_js and Data_extractor are defined elsewhere
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "prompts.json")
        self.prompts = load_js(file_path)

        data = Data_extractor().get(loan_app_name=self.loan_app_name, cr_name=self.cr_name, il_name=self.il_name)
        self.loan_app_tables = data['loan_app_tables']
        self.industrial_licence = data["industrial_licence"]
        self.commercial_registration = data["commercial_registration"]
        self.market_data = data["market_data"]

    
    def go(self):
        print("Extracting Data")
        self.load_rdata()

        compile_prompt = """You are given a list of Json each having 'Perspective' and 'Response' as keys. Your job is to categorize them under Market Responses,
        Technical Responses and Credit Responses as headings. The answer must start addressing the user e.g;
        'Here is the complete breakdown of analysis of your Commercial Loan Application' Make sure to format the out with numbers under each cateogory."""

        ai_agent = self.ai_agent
        l_appt = self.loan_app_tables
        il = self.industrial_licence
        cr = self.commercial_registration
        md = self.market_data

        print("Data Extraction Completed!")
        
        input = self.prompts
        all_results = []
        for index, prompt in enumerate(input):
            inputs = {
            "prompt": prompt,
            "tables": l_appt,
            "industrial_licence": il,
            "commercial_registration": cr,
            "market_data": json.dumps(md, indent=4)
            }

            analysis_result = ai_agent.analyse(inputs)
            all_results.append(analysis_result)
        
        # Compile Final Results
        inputs = {
        "compile_prompt": compile_prompt,
        "input_payload": json.dumps(all_results, indent=4)
        }    
    
        final_result = ai_agent.analyse(inputs)
        return final_result