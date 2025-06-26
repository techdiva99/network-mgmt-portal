# tasks/__init__.py
"""
Tasks package for CrewAI workflows
"""
from .data_tasks import DataProcessingTasks
from .analysis_tasks import OptimizationAnalysisTasks
from .intelligence_tasks import CompetitiveIntelligenceTasks
from .reporting_tasks import ExecutiveReportingTasks

__all__ = [
    'DataProcessingTasks',
    'OptimizationAnalysisTasks',
    'CompetitiveIntelligenceTasks', 
    'ExecutiveReportingTasks'
]

