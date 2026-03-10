from crewai import Agent
import yaml

def create_strategy_coordinator():
    with open('config/agents.yaml', 'r') as f:
        config = yaml.safe_load(f)['strategy_coordinator']
    
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=True,
        max_iter=15
    )