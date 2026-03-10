from crewai import Agent
import yaml

def create_content_creator():
    with open('config/agents.yaml', 'r') as f:
        config = yaml.safe_load(f)['content_creator']
    
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False
    )