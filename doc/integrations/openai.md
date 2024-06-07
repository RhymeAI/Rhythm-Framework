# Agent (Class)

An agent model with tools.

## Initialization

#### Arguments

> `openai_model`: The LLM model the agent uses.  
> `temperature`: The temperature value for the LLM, needs to be between `0` and `1` inclusive.  
> `tools`: The tools the agent can use.  
> `system_promt`: The system promt for the main agent.  
> `max_iterations`: The maximum number of steps the agent can take.  
> `debug`: Weather or not the agent should print a log to the console.  
> `openai_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.

#### Examples

```python
from rhythm.integrations import Agent, tool

@tool
def add_numbers(number1 : float, number2 : float) -> float:
    """A tool to add two numbers, gives back the result."""
    return number1 + number2

system_prompt = """You are a bot that adds two numbers and gives back the result."""

agent = agent(openai_model="gpt-3.5-turbo", temperature=0.7, tools=[add_numbers], system_prompt=system_prompt, max_iterations=None, debug=False)
```

## Methods

### execute

Execute the agent with the given prompt as user input.

#### Arguments

> `prompt`: The prompt for the agent as user input.

#### Returns:

The agent output after fully executing.

#### Examples

```python
agent.execute("What's 1 + 2 ?")
```

# Image_Generator (Class)

An interface with the image generator from openai.

## Initialization

#### Arguments

> `openai_model`: The generator model to use.  
> `openai_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.

#### Examples

```python
from rhythm.integrations import Image_Generator

generator = Image_Generator(openai_model="dall-e-2")
```

## Methods

### create_image

Create an image file based on the given prompt.

#### Arguments

> `prompt`: The prompt for the image generator.  
> `size`: The size of the image, needs to be one of: `'56x256'`, `'512x512'`, `'1024x1024'`, `'1792x1024'`, `'1024x1792'`.  
> `quality`: The quality of the image, needs to be one of: `'standard'`, `'hd'`.  
> `file`: The file path to save the image to.

#### Examples

```python
generator.create_image(prompt="Draw a dragon.", size="512x512", quality="standard", file="./example_image.png")
```
