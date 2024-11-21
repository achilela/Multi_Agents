import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List

class VisualizationManager:
    @staticmethod
    def create_issue_distribution_chart(data: Dict[str, int]):
        """Create a pie chart showing issue distribution"""
        fig = go.Figure(data=[go.Pie(
            labels=list(data.keys()),
            values=list(data.values()),
            hole=.3
        )])
        fig.update_layout(title="Issue Distribution")
        return fig

    @staticmethod
    def create_priority_breakdown(data: Dict[str, int]):
        """Create a bar chart showing priority levels"""
        fig = go.Figure(data=[go.Bar(
            x=list(data.keys()),
            y=list(data.values())
        )])
        fig.update_layout(title="Priority Level Breakdown")
        return fig

    @staticmethod
    def create_resolution_time_trend(data: List[Dict[str, any]]):
        """Create a line chart showing resolution time trends"""
        df = pd.DataFrame(data)
        fig = px.line(df, x='date', y='resolution_time',
                     title='Average Resolution Time Trend')
        return fig

    @staticmethod
    def create_satisfaction_trend(data: List[Dict[str, any]]):
        """Create a line chart showing satisfaction trends"""
        df = pd.DataFrame(data)
        fig = px.line(df, x='date', y='satisfaction',
                     title='Customer Satisfaction Trend')
        return fig

    def render_visualization(self, chart_data: Dict[str, any]):
        """Render visualization in Streamlit"""
        st.subheader("Support Data Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'issue_distribution' in chart_data:
                st.plotly_chart(
                    self.create_issue_distribution_chart(
                        chart_data['issue_distribution']
                    ),
                    use_container_width=True
                )
            
            if 'resolution_time_trend' in chart_data:
                st.plotly_chart(
                    self.create_resolution_time_trend(
                        chart_data['resolution_time_trend']
                    ),
                    use_container_width=True
                )

        with col2:
            if 'priority_breakdown' in chart_data:
                st.plotly_chart(
                    self.create_priority_breakdown(
                        chart_data['priority_breakdown']
                    ),
                    use_container_width=True
                )
            
            if 'satisfaction_trend' in chart_data:
                st.plotly_chart(
                    self.create_satisfaction_trend(
                        chart_data['satisfaction_trend']
                    ),
                    use_container_width=True
                )