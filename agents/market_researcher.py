from crewai import Agent
import yaml

def create_market_researcher():
    with open('config/agents.yaml', 'r') as f:
        config = yaml.safe_load(f)['market_researcher']
    
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False
    )