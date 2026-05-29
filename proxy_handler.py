import litellm
from litellm.integrations.custom_logger import CustomLogger
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

'''
$env:GROQ_API_KEY = "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"
An automated, anonymous midpoint negotiation module for ODR.
'''

class ODRProxyHandler(CustomLogger):
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    # This hook runs BEFORE the data leaves your server
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        # The 'data' dict contains your 'messages'
        if "messages" in data:
            original_text = data["messages"][-1]["content"]

            # 1. Analyze for PII
            results = self.analyzer.analyze(text=original_text, language='en', entities=["PERSON"])

            # 2. Tokenize
            operators = {"PERSON": OperatorConfig("replace", {"new_value": "{{USER_NAME}}"})}
            anonymized = self.anonymizer.anonymize(text=original_text, analyzer_results=results, operators=operators)

            # 3. Swap the content in the request data
            data["messages"][-1]["content"] = anonymized.text
            print(f"DEBUG: Masked prompt: {anonymized.text}")

        return data


# Important: Create the instance that LiteLLM will use
proxy_handler_instance = ODRProxyHandler()
