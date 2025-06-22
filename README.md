# Dagger Experiments

Joe's experiments with Dagger!

## Overview

Dagger pipelines that demonstrate different use cases and workflows.

## Prerequisites

- [Dagger CLI](https://docs.dagger.io/install) installed on your system
- Docker running locally

## Getting Started

### Initialize Dagger

```bash
dagger develop
```

### Configure your environment

Set your API key as an environment variable.

Copy from example:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key (can be GEMINI or OPENAI too).

Test it is working:

```bash
dagger -c "llm | model"
```

The output should be something like:

```bash
▶ connect 0.7s
▶ detect module: . 1.3s
▶ load module: /mnt/c/Users/joefo/test/dagger_experiments 8.5s

▶ Missing.model: String! 0.1s

claude-3-5-sonnet-latest

Setup tracing at https://dagger.cloud/traces/setup. To hide set DAGGER_NO_NAG=1
```

## Available Pipelines

### Go-coder with execution test

An example of a pipeline that uses a LLM to generate Go code
...and then plays with / tests it.

#### Customize Prompts

To customize the prompts used by the LLM, edit the `config.py` file:

```bash
# Edit the configuration file in the agent directory
.dagger/src/llm_go_pipeline/config.py
```

You can modify:
- `DEFAULT_GO_GENERATION_PROMPT`: How the LLM generates Go code
- `DEFAULT_INTERACTION_PROMPT`: How the LLM interacts with the generated program

You can also modify other prompts in the main.py file, such as the final report format.

#### Run the pipeline

Start the shell:

```bash
cd <same directory as your .env file>
dagger
```

Run the pipeline:

```bash
# Customise the instruction however you want
complete-pipeline "make a guessing game with user interaction"
```

⚠️ You might need to run a few times with different assignments to get a good output :)

### Expected output

The output should be something like:

```bash
=== DAGGER.IO LLM PIPELINE EXECUTION REPORT ===

Assignment Given: make a guessing game with user interaction

Step 1: Code Generation Completed ✅
- LLM successfully generated Go program
- Program built and validated in container

Step 2: Interactive Testing Completed ✅
- Second LLM agent tested the program
- Full interaction documented below

=== INTERACTION LOG ===
Program Testing Session Log

Initial Exploration:
1. Examined the program structure in /app directory:
   - Found main.go, go.mod, and game directory
2. Reviewed main.go source code:
   - Confirmed it's a number guessing game
   - Number range: 1-100
   - Maximum attempts: 10
   - Provides feedback (too high/too low)

Building:
1. Attempted to run ./game (failed - not built)
2. Successfully built program with: go build -o game

Game Testing Session:
1. Game started with welcome message and instructions
2. My guessing strategy:
   - Started with 50 (middle of range)
   - Got "Too high" -> number is < 50
   - Tried 75 -> "Too high"
   - Tried 63 -> "Too high"
   - Tried 57 -> "Too high"
   - Tried 53 -> "Too high"
   - Tried 51 -> "Too high"
   - Tried 52 -> "Too high"

Program Behavior Analysis:
1. Core functionality:
   - Random number generation works
   - Input processing works correctly
   - Feedback system works (too high/too low responses)
   - Attempt counting works
   - Clear user interface with good instructions

2. User Experience:
   - Clear welcome message
   - Good feedback after each guess
   - Shows attempt count clearly
   - Maintains good spacing for readability

3. Input Handling:
   - Accepts numeric input correctly
   - Properly processes each guess
   - Program responds appropriately to input

The program functions as intended, providing an engaging number guessing game experience with clear feedback and proper game mechanics.

=== PIPELINE COMPLETED SUCCESSFULLY ===
```

## Configuration

### Required Configuration

- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`: Your LLM API key

### Customizing Prompts

The prompts used by the LLM can be customized by editing the `config.py` file:

```python
# In .dagger/src/llm_go_pipeline/config.py

DEFAULT_GO_GENERATION_PROMPT = """
Your custom prompt for Go code generation here...
"""

DEFAULT_INTERACTION_PROMPT = """
Your custom prompt for program interaction here...
"""
```

### Default Prompts

The pipeline uses sensible defaults:

- **Go Generation**: Instructs the LLM to create interactive, well-commented Go programs
- **Interaction**: Guides the LLM to test programs naturally as a human user would

### Example Custom Prompts

```python
# Make the LLM focus on specific aspects of speed and execution
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
Focus on speed and efficiency of execution

Ensure the program will come to a natural conclusion and exit after a few exchanges (up to 20)

Always build the code with 'go build' to ensure it works before finishing.
Return the container with the working Go program.
""".strip()

# Change the interaction style
DEFAULT_INTERACTION_PROMPT = """
You are a human user testing a Go program. Your task is: $task

The program is in the $program container in the /app directory.

Steps to follow:
1. First, explore what's in the /app directory to understand the program structure
2. Look at the main.go file to understand what the program does
3. Build the program if it's not already built (go build)
4. Run the program and interact with it naturally as a human user would
5. Try different inputs to test various features
6. Provide thoughtful responses that a real user might give
7. Continue the interaction for several exchanges to thoroughly test the program
8. Document the entire interaction experience

Be curious, ask questions, try edge cases, and provide realistic human responses.
Create an engaging conversation that demonstrates the program's capabilities.

Save the complete interaction log (including your inputs and the program's outputs) 
as a detailed report.

Use the tools available to run commands, provide input, and capture output.
""".strip()
```
