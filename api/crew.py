"""
SmartBasket CrewAI Crew Module
Orchestrates agents and tasks into a functional crew for product recommendations.
This is the KICKOFF code that assembles and runs the entire CrewAI pipeline.
"""

from crewai import Crew, Process
from agents import create_all_agents
from tasks import (
    create_analyze_needs_task,
    create_recommend_products_task,
    create_budget_analysis_task,
    create_compatibility_check_task
)
from products import get_catalog_string


def create_smart_basket_crew(customer_query: str, llm=None):
    """
    Creates and configures the SmartBasket shopping recommendation crew.
    
    The crew consists of 3 agents working in a sequential process:
    1. Product Recommender → Analyzes needs & recommends products
    2. Budget Analyst → Evaluates cost-effectiveness
    3. Compatibility Checker → Ensures products work together
    
    Args:
        customer_query: The user's natural language shopping query
        llm: Optional LLM instance to use for all agents
    
    Returns:
        Configured Crew instance ready for kickoff
    """
    # Get product catalog as formatted string
    catalog_str = get_catalog_string()
    
    # Create all agents
    agents = create_all_agents(llm=llm)
    recommender = agents["product_recommender"]
    budget = agents["budget_analyst"]
    compatibility = agents["compatibility_checker"]
    
    # Create tasks in sequential order with context chaining
    task1_analyze = create_analyze_needs_task(
        agent=recommender,
        customer_query=customer_query,
        product_catalog_str=catalog_str
    )
    
    task2_recommend = create_recommend_products_task(
        agent=recommender,
        product_catalog_str=catalog_str,
        context_tasks=[task1_analyze]
    )
    
    task3_budget = create_budget_analysis_task(
        agent=budget,
        customer_query=customer_query,
        product_catalog_str=catalog_str,
        context_tasks=[task1_analyze, task2_recommend]
    )
    
    task4_compatibility = create_compatibility_check_task(
        agent=compatibility,
        product_catalog_str=catalog_str,
        context_tasks=[task2_recommend, task3_budget]
    )
    
    # Assemble the crew
    crew = Crew(
        agents=[recommender, budget, compatibility],
        tasks=[task1_analyze, task2_recommend, task3_budget, task4_compatibility],
        process=Process.sequential,  # Tasks execute one after another
        verbose=True
    )
    
    return crew


def kickoff_crew(customer_query: str, llm=None):
    """
    Main entry point: Creates the crew and kicks off the recommendation process.
    
    Args:
        customer_query: Natural language query from the user
        llm: Optional LLM instance
    
    Returns:
        CrewOutput with the final recommendation
    """
    crew = create_smart_basket_crew(customer_query, llm=llm)
    result = crew.kickoff()
    return result


# --- Direct execution for testing ---
if __name__ == "__main__":
    print("=" * 60)
    print("SmartBasket CrewAI - Test Run")
    print("=" * 60)
    
    test_query = "I need a setup for video editing and casual gaming. Budget around $30000"
    print(f"\nCustomer Query: {test_query}\n")
    
    result = kickoff_crew(test_query)
    
    print("\n" + "=" * 60)
    print("FINAL CREW OUTPUT:")
    print("=" * 60)
    print(result)
