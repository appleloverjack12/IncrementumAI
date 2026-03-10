from crewai import Agent
import yaml

def create_outreach_specialist():
    with open('config/agents.yaml', 'r') as f:
        config = yaml.safe_load(f)['outreach_specialist']
    
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False
    )