from crewai import Agent, Crew, Process, Task
from crewai_tools import FileReadTool, SerperDevTool
import asyncio
import yaml
from pathlib import Path

class SupportAnalysisCrew:
    def __init__(self):
        self.load_config()
        self.csv_tool = FileReadTool(file_path='./support_tickets_data.csv')
        self.setup_agents()
        self.setup_tasks()

    def load_config(self):
        config_path = Path(__file__).parent / "config"
        with open(config_path / "agents.yaml") as f:
            self.agents_config = yaml.safe_load(f)
        with open(config_path / "tasks.yaml") as f:
            self.tasks_config = yaml.safe_load(f)

    def setup_agents(self):
        self.suggestion_agent = Agent(
            role="Suggestion Engine",
            goal="Generate actionable suggestions",
            backstory="You analyze support tickets and provide solutions",
            tools=[self.csv_tool]
        )
        
        self.reporting_agent = Agent(
            role="Report Generator",
            goal="Create comprehensive reports",
            backstory="You transform data into insights",
            tools=[self.csv_tool]
        )
        
        self.chart_agent = Agent(
            role="Visualization Expert",
            goal="Create data visualizations",
            backstory="You create compelling visual insights",
            allow_delegation=False
        )

    def setup_tasks(self):
        self.tasks = [
            Task(
                description="Generate suggestions for support tickets",
                agent=self.suggestion_agent
            ),
            Task(
                description="Create data visualizations",
                agent=self.chart_agent
            ),
            Task(
                description="Compile final report",
                agent=self.reporting_agent
            )
        ]

    def get_crew(self) -> Crew:
        return Crew(
            agents=[self.suggestion_agent, self.reporting_agent, self.chart_agent],
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    async def process_async(self, inputs: dict) -> str:
        crew = self.get_crew()
        result = await crew.kickoff(inputs=inputs)
        yield result.raw

    def process(self, inputs: dict) -> str:
        crew = self.get_crew()
        result = crew.kickoff(inputs=inputs)
        return result.raw