"""
SmartBasket CrewAI Tasks Module
Defines the tasks that agents will execute in the recommendation pipeline.
"""

import yaml
import os
from crewai import Task

# Load task configurations from YAML
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")

def load_task_config():
    """Load task configurations from the YAML config file"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_analyze_needs_task(agent, customer_query, product_catalog_str):
    """
    Task 1: Analyze the customer's needs from their query.
    The Product Recommender agent parses and structures the request.
    """
    config = load_task_config()
    cfg = config['analyze_needs']
    
    description = cfg['description'].format(
        customer_query=customer_query,
        product_catalog=product_catalog_str
    )
    
    return Task(
        description=description,
        expected_output=cfg['expected_output'],
        agent=agent
    )


def create_recommend_products_task(agent, product_catalog_str, context_tasks=None):
    """
    Task 2: Recommend products based on the needs analysis.
    Generates specific product suggestions with justifications.
    """
    config = load_task_config()
    cfg = config['recommend_products']
    
    description = cfg['description'].format(
        product_catalog=product_catalog_str
    )
    
    task_kwargs = {
        "description": description,
        "expected_output": cfg['expected_output'],
        "agent": agent,
    }
    
    if context_tasks:
        task_kwargs["context"] = context_tasks
    
    return Task(**task_kwargs)


def create_budget_analysis_task(agent, customer_query, product_catalog_str, context_tasks=None):
    """
    Task 3: Analyze the budget implications of suggested products.
    Evaluates total cost and suggests alternatives if needed.
    """
    config = load_task_config()
    cfg = config['analyze_budget']
    
    description = cfg['description'].format(
        customer_query=customer_query,
        product_catalog=product_catalog_str
    )
    
    task_kwargs = {
        "description": description,
        "expected_output": cfg['expected_output'],
        "agent": agent,
    }
    
    if context_tasks:
        task_kwargs["context"] = context_tasks
    
    return Task(**task_kwargs)


def create_compatibility_check_task(agent, product_catalog_str, context_tasks=None):
    """
    Task 4: Verify compatibility between all recommended products.
    Ensures everything works together seamlessly.
    """
    config = load_task_config()
    cfg = config['check_compatibility']
    
    description = cfg['description'].format(
        product_catalog=product_catalog_str
    )
    
    task_kwargs = {
        "description": description,
        "expected_output": cfg['expected_output'],
        "agent": agent,
    }
    
    if context_tasks:
        task_kwargs["context"] = context_tasks
    
    return Task(**task_kwargs)
