"""
Configuration management for the LLM Go Pipeline.
"""

import os

class Config:
    """Configuration class for the LLM Go Pipeline."""
    
    # Default prompt for Go code generation
    DEFAULT_GO_GENERATION_PROMPT = """
You have an assignment to create a Go program.

Your task: $assignment

Requirements:
1. Create a main.go file in the /app directory
2. Write clean, well-commented Go code
3. Make the program interactive - it should accept user input and respond
4. Include proper error handling
5. Build the code to ensure it compiles successfully
6. Use go mod init if needed to create a proper Go module

The program should be designed to interact with users through stdin/stdout.
Make it engaging and demonstrate the functionality clearly.

Ensure the program will come to a natural conclusion and exit after a few exchanges (up to 20)

Always build the code with 'go build' to ensure it works before finishing.
Return the container with the working Go program.
""".strip()

    # Default prompt for program interaction
    DEFAULT_INTERACTION_PROMPT = """
You are a human user running a Go program. Your task is: $task

The program is in the $program container in the /app directory.

Steps to follow:
1. First, explore what's in the /app directory to understand the program structure
2. Look at the main.go file to understand what the program does
3. Build the program if it's not already built (go build)
4. Run the program once and interact with it naturally as a human user would
5. Document the interaction in a reliable, accurate 'as-it-happened' log
""".strip()

    @classmethod
    def get_go_generation_prompt(cls) -> str:
        """
        Get the Go code generation prompt from environment or use default.
        
        Returns:
            The prompt string for Go code generation
        """
        return os.getenv("GO_GENERATION_PROMPT", cls.DEFAULT_GO_GENERATION_PROMPT)
    
    @classmethod
    def get_interaction_prompt(cls) -> str:
        """
        Get the program interaction prompt from environment or use default.
        
        Returns:
            The prompt string for program interaction
        """
        return os.getenv("INTERACTION_PROMPT", cls.DEFAULT_INTERACTION_PROMPT)
    


# Global config instance
config = Config() 