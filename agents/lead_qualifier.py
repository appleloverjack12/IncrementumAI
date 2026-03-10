from crewai import Agent
import yaml

def create_lead_qualifier():
    with open('config/agents.yaml', 'r') as f:
        config = yaml.safe_load(f)['lead_qualifier']
    
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False
    )