from crewai import Crew, Task, Process
from agents import (
    create_strategy_coordinator,
    create_market_researcher,
    create_outreach_specialist,
    create_content_creator,
    create_lead_qualifier
)
import yaml

class IncrementumCrew:
    def __init__(self):
        # Kreiraj sve agente
        self.strategy_coordinator = create_strategy_coordinator()
        self.market_researcher = create_market_researcher()
        self.outreach_specialist = create_outreach_specialist()
        self.content_creator = create_content_creator()
        self.lead_qualifier = create_lead_qualifier()
        
        # Load task configs
        with open('config/tasks.yaml', 'r') as f:
            self.task_configs = yaml.safe_load(f)
    
    def create_expansion_plan(self, market, industry):
        """
        Koordinirani workflow za kreiranje expansion plana
        """
        # Task 1: Market Research
        research_task = Task(
            description=self.task_configs['market_research_task']['description'].format(
                market=market,
                industry=industry
            ),
            expected_output=self.task_configs['market_research_task']['expected_output'],
            agent=self.market_researcher
        )
        
        # Task 2: Strategy Coordinator syntetizira plan
        strategy_task = Task(
            description=f"Based on market research, create comprehensive expansion strategy for {industry} company entering {market}",
            expected_output="Detailed expansion plan with timeline, budget estimates, and key actions",
            agent=self.strategy_coordinator,
            context=[research_task]  # Koristi research rezultate
        )
        
        # Kreiraj Crew
        crew = Crew(
            agents=[self.market_researcher, self.strategy_coordinator],
            tasks=[research_task, strategy_task],
            process=Process.sequential,  # Sequential execution
            verbose=2
        )
        
        # Pokreni workflow
        result = crew.kickoff()
        return result
    
    def draft_outreach(self, target_persona, market, context=""):
        """
        Kreira personalized outreach message
        """
        outreach_task = Task(
            description=self.task_configs['outreach_task']['description'].format(
                target_persona=target_persona,
                market=market
            ) + f"\n\nAdditional context: {context}",
            expected_output=self.task_configs['outreach_task']['expected_output'],
            agent=self.outreach_specialist
        )
        
        crew = Crew(
            agents=[self.outreach_specialist],
            tasks=[outreach_task],
            verbose=2
        )
        
        return crew.kickoff()
    
    def create_content(self, content_type, topic, market):
        """
        Kreira content
        """
        content_task = Task(
            description=self.task_configs['content_creation_task']['description'].format(
                content_type=content_type,
                topic=topic,
                market=market
            ),
            expected_output=self.task_configs['content_creation_task']['expected_output'],
            agent=self.content_creator
        )
        
        crew = Crew(
            agents=[self.content_creator],
            tasks=[content_task],
            verbose=2
        )
        
        return crew.kickoff()
    
    def qualify_lead(self, lead_info):
        """
        Kvalificira lead
        """
        qualify_task = Task(
            description=self.task_configs['lead_qualification_task']['description'].format(
                lead_info=lead_info
            ),
            expected_output=self.task_configs['lead_qualification_task']['expected_output'],
            agent=self.lead_qualifier
        )
        
        crew = Crew(
            agents=[self.lead_qualifier],
            tasks=[qualify_task],
            verbose=2
        )
        
        return crew.kickoff()