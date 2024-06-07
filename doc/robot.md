# Robot (Class)

An agent model with an integrated memory agent using a vector database.

## Initialization

#### Arguments

> `memory_vector_db`: The vector database to use for memory.  
> `system_promt`: The system promt for the main agent.  
> `openai_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.  
> `openai_model`: The LLM model the main agent uses.  
> `temperature`: The temperature value for the LLM, needs to be between `0` and `1` inclusive.  
> `additional_tools`: The additional tools the agent can use, besides those for memory.  
> `debug`: Weather or not the agent should print a log to the console.

#### Examples

```python
from rhythm.robot import Robot, Vector_DB, tool

@tool
def add_numbers(number1 : float, number2 : float) -> float:
    """A tool to add two numbers, gives back the result."""
    return number1 + number2

system_prompt = """You are a bot that adds two numbers and then needs to remember what  was calculated for the future.
Your memories should include the entire calculation, not just the answer.
After adding the current calculation provide an overwiev of all previously done calculations.
Your memories should follow the sceme: 'Calculation: x + y = z'."""

memory_db = Vector_DB(db_name="example")
robot = Robot(memory_vector_DB=memory_db, system_prompt=system_prompt, additional_tools=[add_numbers])
```

## Methods

### execute

Execute the agent with the given prompt as user input.

#### Arguments:

> `prompt`: The prompt for the agent as user input.

#### Returns:

The agent output after fully executing.

#### Examples

```python
robot.execute("What's 1 + 2 ? And what have you calculated before?")
```
