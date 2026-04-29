"""
SmartBasket CrewAI Agents Module
Defines the three specialized agents for the shopping recommendation crew.
"""

import yaml
import os
from crewai import Agent

# Load agent configurations from YAML
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")

def load_agent_config():
    """Load agent configurations from the YAML config file"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_product_recommender(llm=None):
    """
    Creates the Product Recommender agent.
    This agent analyzes customer queries and recommends suitable products.
    """
    config = load_agent_config()
    cfg = config['product_recommender']
    
    return Agent(
        role=cfg['role'],
        goal=cfg['goal'],
        backstory=cfg['backstory'],
        verbose=cfg.get('verbose', True),
        allow_delegation=cfg.get('allow_delegation', True),
        llm=llm
    )


def create_budget_analyst(llm=None):
    """
    Creates the Budget Analyst agent.
    This agent evaluates cost-effectiveness and suggests optimal bundles.
    """
    config = load_agent_config()
    cfg = config['budget_analyst']
    
    return Agent(
        role=cfg['role'],
        goal=cfg['goal'],
        backstory=cfg['backstory'],
        verbose=cfg.get('verbose', True),
        allow_delegation=cfg.get('allow_delegation', False),
        llm=llm
    )


def create_compatibility_checker(llm=None):
    """
    Creates the Compatibility Checker agent.
    This agent verifies product compatibility and identifies potential issues.
    """
    config = load_agent_config()
    cfg = config['compatibility_checker']
    
    return Agent(
        role=cfg['role'],
        goal=cfg['goal'],
        backstory=cfg['backstory'],
        verbose=cfg.get('verbose', True),
        allow_delegation=cfg.get('allow_delegation', False),
        llm=llm
    )


def create_all_agents(llm=None):
    """Create and return all three agents as a dictionary"""
    return {
        "product_recommender": create_product_recommender(llm),
        "budget_analyst": create_budget_analyst(llm),
        "compatibility_checker": create_compatibility_checker(llm),
    }
