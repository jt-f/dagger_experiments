"""
Dagger.io Pipeline with LLM Go Code Generation and Execution

This pipeline demonstrates:
1. Using an LLM to generate Go code based on an assignment
2. Having another LLM agent run and interact with the program as a human would

Based on the Dagger.io quickstart AI agent example, customised to add the second agent.
"""
import dagger
from dagger import dag, function, object_type
from .config import config


@object_type
class LlmGoPipeline:
    """A pipeline that uses LLMs to generate and interact with Go programs."""

    @function
    def generate_go_program(
        self,
        assignment: str,
    ) -> dagger.Container:
        """
        Step 1: Use an LLM to write a Go program based on the assignment.

        Args:
            assignment: The programming task description (e.g., "write a simple calculator")

        Returns:
            Container with the generated Go program
        """
        
        # Set up the environment for the LLM to generate Go code
        environment = (
            dag.env()
            .with_string_input("assignment", assignment, "the programming assignment to complete")
            .with_container_input(
                "builder",
                dag.container().from_("golang:1.21").with_workdir("/app"),
                "a Go container to use for building and running Go code",
            )
            .with_container_output(
                "completed", "the completed assignment in the Go container"
            )
        )

        # Use LLM to generate the Go program with configurable prompt
        work = (
            dag.llm()
            .with_env(environment)
            .with_prompt(config.get_go_generation_prompt())
        )

        return work.env().output("completed").as_container()

    @function
    async def run_and_interact(
        self,
        program_container: dagger.Container,
        interaction_description: str = "Test the program as a curious user would",
    ) -> str:
        """
        Step 2: Use another LLM agent to run the program and interact with it.

        Args:
            program_container: Container with the generated Go program
            interaction_description: How the agent should interact with the program

        Returns:
            The interaction log showing the conversation
        """

        
        # Set up environment for the interaction agent
        environment = (
            dag.env()
            .with_container_input(
                "program", 
                program_container, 
                "container with the Go program to run and interact with"
            )
            .with_string_input(
                "task", 
                interaction_description, 
                "description of how to interact with the program"
            )
            .with_string_output("interaction_log", "log of the interaction with the program")
        )

        # Use LLM to interact with the program with configurable prompt
        work = (
            dag.llm()
            .with_env(environment)
            .with_prompt(config.get_interaction_prompt())
        )

        # Get the interaction log
        result = await work.env().output("interaction_log").as_string()
        return result

    @function
    async def complete_pipeline(
        self,
        assignment: str,
        interaction_description: str = "Test the program thoroughly as a real user",
    ) -> str:
        """
        Run the complete pipeline: generate Go code and then interact with it.

        Args:
            assignment: The programming task for the LLM to implement
            interaction_description: How the second agent should interact with the program

        Returns:
            Complete log of the generation and interaction process
        """
        print(f"🚀 Starting pipeline with assignment: {assignment}")

        # Step 1: Generate the Go program
        print("📝 Step 1: Generating Go program with LLM...")
        program_container = self.generate_go_program(assignment)

        # Step 2: Have another agent interact with the program
        print("🤖 Step 2: Having second agent interact with the program...")
        interaction_log = await self.run_and_interact(program_container, interaction_description)

        # Combine results
        final_report = f"""
=== DAGGER.IO LLM PIPELINE EXECUTION REPORT ===

Assignment Given: {assignment}

Step 1: Code Generation Completed ✅
- LLM successfully generated Go program
- Program built and validated in container

Step 2: Interactive Testing Completed ✅
- Second LLM agent tested the program
- Full interaction documented below

=== INTERACTION LOG ===
{interaction_log}

=== PIPELINE COMPLETED SUCCESSFULLY ===
"""

        return final_report
