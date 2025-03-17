import spacy
import re
from pathlib import Path
import yaml
from config import logger

nlp = spacy.load("en_core_web_sm")

class DataProcessor:
    def __init__(self):
        yaml_path = Path(__file__).parent / 'agents.yaml'
        with open(yaml_path, 'r') as file:
            self.agents = yaml.safe_load(file)

    def translate_prompt_to_input_data(self, prompt: str, arguments: dict = {}) -> dict:
        input_data = {"response_type": "markdown"}
        doc = nlp(prompt)
        
        # Identify agent_type
        agent_type = arguments.get("tracking_key") if arguments.get("tracking_key") in self.agents else self._identify_agent_type(prompt)
        if not agent_type:
            logger.warning("Agent type not found in prompt: %s", prompt)
            return input_data
            
        input_data["agent_type"] = agent_type
        agent_fields = {field["id"]: field for field in self.agents[agent_type].get("fields", [])}
        
        # Extract fields
        extracted_fields = self._extract_fields(doc, prompt, agent_type)
        input_data.update(self._map_fields(extracted_fields, agent_fields))
        
        logger.info("Mapped input data: %s", input_data)
        return input_data

    def _identify_agent_type(self, prompt: str) -> str | None:
        agent_keys = {
            re.sub(r"[^a-zA-Z ]", "", key.lower().replace("_", " ")).strip(): key
            for key in self.agents
        }
        prompt_lower = prompt.lower()
        for normalized_key, actual_agent in agent_keys.items():
            if normalized_key in prompt_lower:
                return actual_agent
        return None

    def _extract_fields(self, doc, prompt: str, agent_type: str) -> dict:
        extracted_fields = {}
        
        # NER extraction
        for ent in doc.ents:
            key = ent.label_.lower().replace(" ", "_")
            extracted_fields[key] = ent.text.strip('"')
            
        # Dependency parsing
        for token in doc:
            if token.dep_ in {"attr", "amod", "compound"} and token.head.dep_ == "ROOT":
                key = token.text.lower().replace(" ", "_")
                extracted_fields[key] = token.head.text
                
        # Extract field value after agent name
        agent_name = self.agents[agent_type]["name"].lower()
        if agent_name in prompt.lower():
            field_value = prompt[prompt.lower().index(agent_name) + len(agent_name):].strip()
            if field_value:
                extracted_fields["customer_purchase_data"] = field_value
                
        return extracted_fields

    def _map_fields(self, extracted_fields: dict, agent_fields: dict) -> dict:
        result = {}
        for field_id in agent_fields:
            for key, value in extracted_fields.items():
                if field_id in key:
                    result[field_id] = value
            if field_id not in result:
                result[field_id] = agent_fields[field_id].get("placeholder", "Unknown")
        return result