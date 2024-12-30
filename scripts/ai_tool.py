import os
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import initialize_agent, AgentType

class ai_tool:
    def __init__(self, model="gpt-4o", temperature=0):
        """
        Initialize the SmartAnalysisAgent with model configuration and validate OpenAI API key.
        """
        self._load_and_validate_api_key()
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.math_agent = initialize_agent(
            tools=[PythonREPLTool()],
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            # handle_parse_errors=True,
            verbose=True
        )

    @staticmethod
    def _load_and_validate_api_key():
        """
        Load and validate the OpenAI API key from the .env file.
        """
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it in your .env file.")
        os.environ["OPENAI_API_KEY"] = api_key

    def analyse(self, inputs: dict):
        """
        Run an LLM-based analysis on tables provided in markdown format.
        
        Args:
            inputs (dict): A dictionary containing:
                - "tables": List of tables in markdown format as strings.
                - "analysis_guidelines": Guidelines for the analysis.
                - "output_guidelines": Guidelines for the output formatting.

        Returns:
            str: Analysis result from the LLM.
        """
        # Validate input keys
        step_1_keys = {"tables", "prompt", "industrial_licence", "commercial_registration", "market_data"}
        step_2_keys = {"compile_prompt", "input_payload"}

        if step_1_keys.issubset(inputs.keys()):
            if inputs["prompt"]["task_number"]=="2":
                # Combine inputs into a structured prompt
                prompt_template = """
                {prompt}

                **Tables of loan application**:
                {tables}

                **Commercial Registration**:
                {commercial_registration}

                **Industrial License**:
                {industrial_licence}
                """
                prompt_input = ["tables", "prompt", "industrial_licence", "commercial_registration"]
                if isinstance(inputs["tables"], dict):
                    tables = json.dumps(inputs["tables"]['1. PROJECT DATA'])
                else:
                    tables = inputs["tables"]

                llm_input = {
                "prompt": inputs["prompt"]["prompt"],
                "tables": tables,
                "commercial_registration": "\n\n"+ inputs["commercial_registration"],
                "industrial_licence": "\n\n"+ inputs["industrial_licence"]
                }

            elif inputs["prompt"]["task_number"]=="4":
                    # Combine inputs into a structured prompt
                    prompt_template = """
                    {prompt}

                    **Tables of loan application**:
                    {tables}
                    """
                    prompt_input = ["tables", "prompt"]
                    if isinstance(inputs["tables"], dict):
                        tables = json.dumps({x:y for x,y in inputs["tables"].items() if x in ['1. PROJECT DATA', '2. MARKETING INFORMATION', "3. TECHNICAL INFORMATION"]})
                    else:
                         tables = inputs["tables"]
                    llm_input = {
                    "prompt": inputs["prompt"]["prompt"],
                    "tables": tables
                    }

            elif inputs["prompt"]["task_number"]=="5":
                    # Combine inputs into a structured prompt
                    prompt_template = """
                    {prompt}

                    **Tables of loan application**:
                    {tables}
                    """
                    prompt_input = ["tables", "prompt"]
                    if isinstance(inputs["tables"], dict):
                        tables = json.dumps({x:y for x,y in inputs["tables"].items() if x in ['2. MARKETING INFORMATION']})
                    else:
                         tables = inputs["tables"]
                    llm_input = {
                    "prompt": inputs["prompt"]["prompt"],
                    "tables": tables,
                    }

            elif inputs["prompt"]["task_number"]=="6":
                # Combine inputs into a structured prompt
                prompt_template = """
                {prompt}

                **Tables**:
                {tables}

                **Market Data**:
                {market_data}
                """
                prompt_input = ["tables", "prompt", "market_data"]
                if isinstance(inputs["tables"], dict):
                    tables = json.dumps({x:y for x,y in inputs["tables"].items() if x in ['1. PROJECT DATA', '2. MARKETING INFORMATION', "3. TECHNICAL INFORMATION"]})
                else:
                     tables = inputs["tables"]
                llm_input = {
                "prompt": inputs["prompt"]["prompt"],
                "tables": tables,
                "market_data": "\n\n"+ inputs["market_data"]
                }
                
            else:
                # Combine inputs into a structured prompt
                prompt_template = """
                {prompt}

                **Tables**:
                {tables}
                """
                prompt_input = ["tables", "prompt"]
                if isinstance(inputs["tables"], dict):
                     tables = json.dumps(inputs["tables"])
                else:
                     tables = inputs["tables"]
                
                llm_input = {
                "prompt": inputs["prompt"]["prompt"],
                "tables": tables,
                }

        elif step_2_keys.issubset(inputs.keys()):
                # Combine inputs into a structured prompt
                prompt_template = """
                {prompt}

                **Input Payload**:
                {input_payload}
                """
                prompt_input = ["input_payload", "prompt"]
                llm_input = {
                "prompt": inputs["compile_prompt"],
                "input_payload": "\n\n".join(inputs["input_payload"]),
                }

        elif not step_1_keys.issubset(inputs.keys()):
            raise ValueError(f"Input dictionary must contain keys: {step_1_keys}")
        else:
            raise ValueError(f"Input dictionary must contain keys: {step_1_keys}")
        
        prompt = PromptTemplate(
            input_variables=prompt_input,
            template=prompt_template.strip()
        )
        
        if "prompt" in inputs.keys() and inputs["prompt"]["task_number"]=="6":
             prompt_formatted = prompt.format(prompt=llm_input["prompt"],
                                               tables=llm_input["tables"],
                                                 market_data=llm_input["market_data"])
             response = self.math_agent.run({"input": prompt_formatted, "chat_history": []})
             return response
        else:
            chain = prompt | self.llm
            result = chain.invoke(input=llm_input)
            return result.content