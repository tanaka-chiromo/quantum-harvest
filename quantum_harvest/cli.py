"""
Command-line interface for Quantum Harvest.
"""

import argparse
import sys
from quantum_harvest import QuantumHarvestEnv, RandomAgent, GreedyAgent, StrategicAgent, GameVisualizer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Quantum Harvest - AI Strategy Game")
    
    parser.add_argument(
        "--agent1", 
        choices=["random", "greedy", "strategic"], 
        default="random",
        help="Agent type for player 1"
    )
    
    parser.add_argument(
        "--agent2", 
        choices=["random", "greedy", "strategic"], 
        default="greedy",
        help="Agent type for player 2"
    )
    
    parser.add_argument(
        "--episodes", 
        type=int, 
        default=1,
        help="Number of episodes to run"
    )
    
    parser.add_argument(
        "--render", 
        action="store_true",
        help="Render the game visually"
    )
    
    parser.add_argument(
        "--map-size", 
        type=int, 
        default=12,
        help="Size of the game map"
    )
    
    args = parser.parse_args()
    
    # Create agents
    agent_classes = {
        "random": RandomAgent,
        "greedy": GreedyAgent,
        "strategic": StrategicAgent
    }
    
    agent1 = agent_classes[args.agent1](player_id=0)
    agent2 = agent_classes[args.agent2](player_id=1)
    
    # Create environment
    env = QuantumHarvestEnv(map_size=args.map_size)
    
    # Create visualizer if rendering
    visualizer = None
    if args.render:
        visualizer = GameVisualizer()
    
    # Run episodes
    for episode in range(args.episodes):
        print(f"Running episode {episode + 1}/{args.episodes}")
        
        observation = env.reset()
        done = False
        step = 0
        
        while not done and step < 1000:  # Prevent infinite loops
            # Get actions from agents
            action1 = agent1.get_action(observation)
            action2 = agent2.get_action(observation)
            
            # Step environment
            observation, rewards, done, info = env.step([action1, action2])
            
            # Render if requested
            if visualizer:
                visualizer.render(env)
            
            step += 1
            
            if done:
                print(f"Episode {episode + 1} finished in {step} steps")
                print(f"Winner: {info.get('winner', 'Unknown')}")
                print(f"Final scores: {rewards}")
                break
    
    print("All episodes completed!")


if __name__ == "__main__":
    main()
