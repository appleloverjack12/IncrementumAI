from crewai import Agent
import yaml
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools.brave_search import brave_search

def create_market_researcher():
    with open('config/agents.yaml', 'r') as f:
        config = yaml.safe_load(f)['market_researcher']
    
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        tools=[brave_search],
        verbose=True,
        allow_delegation=False
    )