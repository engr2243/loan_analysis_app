## Main Functions
import os
import json
from utils.utility import load_js
from scripts.document_ext import Data_extractor
from scripts.ai_tool import ai_tool

cwd = os.getcwd()

class analyse:
    def __init__(self, cr_name, il_name):
        self.cr_name = cr_name
        self.il_name = il_name
        self.registration_tables = None
        self.industrial_licence = None
        self.market_data = None
        self.prompts = None
        self.ai_agent = ai_tool()
        self.get_results = self.go()

    def load_rdata(self):
        # Assuming load_js and Data_extractor are defined elsewhere
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "prompts.json")
        self.prompts = load_js(file_path)
        data = Data_extractor().get(self.cr_name, self.il_name)
        self.registration_tables = data['registration_tables']
        self.industrial_licence = data["industrial_licence"]
        self.market_data = data["market_data"]

    
    def go(self):
        print("Extracting Data")
        self.load_rdata()

        compile_prompt = """Analyse the below requests in all jsons and categorize them under Market Responses,
        Technical Responses and Credit Responses as headings. The answer must start addressing the user e.g;
        'Here is the complete breakdown of analysis of your Commercial Loan Application' Make sure to format the output with bullets and numbers.
        Make sure to not include any additional comments with the response."""

        ai_agent = self.ai_agent
        rt = self.registration_tables
        il = self.industrial_licence
        md = self.market_data

        all_results = []
        for prompt in self.prompts:
            inputs = {
            "prompt": prompt,
            "tables": rt,
            "industrial_licence": il,
            "market_data": json.dumps(md, indent=4)
            }    
        
            analysis_result = ai_agent.analyse(inputs)
            all_results.append(analysis_result['text'])
        
        # Compile Final Results
        inputs = {
        "compile_prompt": compile_prompt,
        "input_payload": json.dumps(all_results, indent=4)
        }    
    
        final_result = ai_agent.analyse(inputs)
        return final_result["text"]