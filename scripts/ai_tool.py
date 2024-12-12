import os
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class ai_tool:
    def __init__(self, model="gpt-4o-mini", temperature=0.2):
        """
        Initialize the SmartAnalysisAgent with model configuration and validate OpenAI API key.
        """
        self._load_and_validate_api_key()
        self.llm = ChatOpenAI(model=model, temperature=temperature)

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
                tables = json.dumps(inputs["tables"]['1. PROJECT DATA'])
                llm_input = {
                "prompt": inputs["prompt"]["prompt"],
                "tables": tables,
                "commercial_registration": "\n\n"+ inputs["commercial_registration"],
                "industrial_licence": "\n\n"+ inputs["industrial_licence"]
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
                llm_input = {
                "prompt": inputs["prompt"]["prompt"],
                "tables": "\n\n".join(inputs["tables"]),
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
                llm_input = {
                "prompt": inputs["prompt"]["prompt"],
                "tables": json.dumps(inputs["tables"]),
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

        # Use the LLM to perform the analysis
        chain = prompt | self.llm
        result = chain.invoke(input=llm_input)

        return result.content