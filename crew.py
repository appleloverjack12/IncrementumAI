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
            context=[research_task]
        )
        
        # Kreiraj Crew
        crew = Crew(
            agents=[self.market_researcher, self.strategy_coordinator],
            tasks=[research_task, strategy_task],
            process=Process.sequential,
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
    
    def full_expansion_workflow(self, market, industry, company_description=""):
        """
        Complete expansion workflow - all agents collaborate
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
        
        # Task 2: Strategy Plan
        strategy_task = Task(
            description=f"Based on market research, create comprehensive expansion strategy for {industry} company entering {market}. {company_description}",
            expected_output="Detailed expansion plan with timeline, budget estimates, and key actions",
            agent=self.strategy_coordinator,
            context=[research_task]
        )
        
        # Task 3: Content Creation
        content_task = Task(
            description=f"Create blog post about '{industry} expansion opportunities in {market}' based on the market research and strategy.",
            expected_output="SEO-optimized blog post with market insights",
            agent=self.content_creator,
            context=[research_task, strategy_task]
        )
        
        # Task 4: Outreach Template
        outreach_task = Task(
            description=f"Draft outreach email template for {industry} decision-makers in {market}, highlighting the expansion opportunities identified in the research.",
            expected_output="Personalized outreach email template",
            agent=self.outreach_specialist,
            context=[research_task, strategy_task]
        )
        
        # Task 5: ICP Definition
        icp_task = Task(
            description=f"Based on market research, define the Ideal Customer Profile for {industry} companies expanding to {market}. Include BANT criteria.",
            expected_output="Detailed ICP with qualification criteria",
            agent=self.lead_qualifier,
            context=[research_task, strategy_task]
        )
        
        # Create crew with all agents
        crew = Crew(
            agents=[
                self.market_researcher,
                self.strategy_coordinator,
                self.content_creator,
                self.outreach_specialist,
                self.lead_qualifier
            ],
            tasks=[research_task, strategy_task, content_task, outreach_task, icp_task],
            process=Process.sequential,
            verbose=2
        )
        
        # Execute workflow
        result = crew.kickoff()
        
        # Parse results
        return {
            "research": str(research_task.output) if hasattr(research_task, 'output') else "Research completed",
            "strategy": str(strategy_task.output) if hasattr(strategy_task, 'output') else "Strategy created",
            "content": str(content_task.output) if hasattr(content_task, 'output') else "Content created",
            "outreach": str(outreach_task.output) if hasattr(outreach_task, 'output') else "Outreach template created",
            "icp": str(icp_task.output) if hasattr(icp_task, 'output') else "ICP defined",
            "full_result": str(result)
        }