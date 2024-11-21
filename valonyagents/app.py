import streamlit as st
import asyncio
import yaml
from pathlib import Path
from components.chat import ChatInterface
from components.visualizations import VisualizationManager
from crew import SupportAnalysisCrew

import sys
#sys.modules['sqlite3'] = __import__('pysqlite3')


class SupportAnalysisApp:
    def __init__(self):
        self.chat_interface = ChatInterface()
        self.visualization_manager = VisualizationManager()
        self.crew_manager = None
        self.load_configurations()
        
    def load_configurations(self):
        """Load YAML configurations"""
        config_path = Path(__file__).parent / "config"
        
        with open(config_path / "agents.yaml") as f:
            self.agents_config = yaml.safe_load(f)
            
        with open(config_path / "tasks.yaml") as f:
            self.tasks_config = yaml.safe_load(f)
    
    def initialize_crew(self):
        """Initialize CrewAI manager"""
        if not self.crew_manager:
            self.crew_manager = SupportAnalysisCrew()
    
    def run(self):
        """Run the Streamlit app"""
        st.set_page_config(
            page_title="Support Data Analysis",
            page_icon="📊",
            layout="wide"
        )
        
        # Initialize CrewAI
        self.initialize_crew()
        
        # Create main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Render chat interface
            self.chat_interface.render(self.crew_manager)
        
        with col2:
            # Render visualizations if data is available
            if hasattr(st.session_state, 'chart_data'):
                self.visualization_manager.render_visualization(
                    st.session_state.chart_data
                )

def main():
    """Main entry point for the Streamlit app"""
    app = SupportAnalysisApp()
    app.run()

if __name__ == "__main__":
    main()