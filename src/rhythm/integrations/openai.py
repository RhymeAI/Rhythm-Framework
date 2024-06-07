"""A module containing all OpenAI API integrations."""

import os
import base64
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool
from typing import Sequence
from typing_extensions import Literal
from langchain.agents import AgentExecutor, tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

class Agent():
    """An agent model with tools."""
    
    def __init__(self, openai_model : str, temperature : float, tools : Sequence[BaseTool], system_prompt: str, max_iterations : int | None, debug : bool, openai_api_key : str | None = None) -> None:
        """An agent model with tools.
        
        Arguments:

            `openai_model`: The LLM model the agent uses.
            `temperature`: The temperature value for the LLM, needs to be between `0` and `1` inclusive.
            `tools`: The tools the agent can use.
            `system_promt`: The system promt for the main agent.
            `max_iterations`: The maximum number of steps the agent can take.
            `debug`: Weather or not the agent should print a log to the console.
            `openai_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.
                
        Examples:

        .. code-block:: python
            from rhythm.integrations import Agent, tool

            @tool
            def add_numbers(number1 : float, number2 : float) -> float:
                \"\"\"A tool to add two numbers, gives back the result.\"\"\"
                return number1 + number2
            
            system_prompt = \"\"\"You are a bot that adds two numbers and gives back the result.\"\"\"

            agent = agent(openai_model="gpt-3.5-turbo", temperature=0.7, tools=[add_numbers], system_prompt=system_prompt, max_iterations=None, debug=False)"""

        openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")

        llm = ChatOpenAI(model=openai_model, temperature=temperature, api_key=openai_api_key)
        llm_with_tools = llm.bind(functions = [format_tool_to_openai_function (t) for t in tools])
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name = "agent_scratchpad"),
            ]
        )
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x ["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )
        self.__agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=max_iterations, verbose=debug)

    def execute(self, prompt : str) -> str:
        """Execute the agent with the given prompt as user input.
        
        Arguments:

            `prompt`: The prompt for the agent as user input.
                
        Returns: 
        
            The agent output after fully executing."""

        return self.__agent_executor.invoke({"input": prompt }).get("output")

class Image_Generator():
    """An interface with the image generator from openai."""

    def __init__(self, openai_model : str, openai_api_key : str | None = None) -> None:
        """An interface with the image generator from openai.

        Arguments:

            `openai_model`: The generator model to use.
            `openai_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.
                
        Examples:

        .. code-block:: python
            from rhythm.integrations import Image_Generator

            generator = Image_Generator(openai_model="dall-e-2")"""

        openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")

        self.__client = OpenAI(api_key=openai_api_key)
        self.__model = openai_model

    def create_image(self, prompt : str, size : Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], quality : Literal["standard", "hd"], file : str) -> None:
        """Create an image file based on the given prompt.
        
        Arguments:

            `prompt`: The prompt for the image generator.
            `size`: The size of the image, needs to be one of: `'56x256'`, `'512x512'`, `'1024x1024'`, `'1792x1024'`, `'1024x1792'`.
            `quality`: The quality of the image, needs to be one of: `'standard'`, `'hd'`.
            `file`: The file path to save the image to."""

        response = self.__client.images.generate(
        model=self.__model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
        response_format="b64_json",
        )

        img_data = str.encode(response.data[0].b64_json)
        with open(file, "wb") as writer:
            writer.write(base64.decodebytes(img_data))
