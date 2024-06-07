"""A module containing all Robot agents."""

import os
from ctypes import cast, py_object
from .integrations.openai import Agent, tool, Sequence, BaseTool
from .integrations.qdrant_db import Vector_DB

class Robot():
    """An agent model with an integrated memory agent using a vector database."""

    def __init__(self, memory_vector_db : Vector_DB, system_prompt : str, openai_api_key : str | None = None, openai_model : str = "gpt-3.5-turbo", temperature : float = 0.7, additional_tools : Sequence[BaseTool] = [], debug : bool = False) -> None:
        """An agent model with an integrated memory agent using a vector database.
        
        Arguments:

            `memory_vector_db`: The vector database to use for memory.
            `system_promt`: The system promt for the main agent.
            `openai_api_key`: The openai API key, leave as `None` to use the enviorment variable `OPENAI_API_KEY`.
            `openai_model`: The LLM model the main agent uses.
            `temperature`: The temperature value for the LLM, needs to be between `0` and `1` inclusive.
            `additional_tools`: The additional tools the agent can use, besides those for memory.
            `debug`: Weather or not the agent should print a log to the console.
                
        Examples:

        .. code-block:: python
            from rhythm.robot import Robot, Vector_DB, tool

            @tool
            def add_numbers(number1 : float, number2 : float) -> float:
                \"\"\"A tool to add two numbers, gives back the result.\"\"\"
                return number1 + number2
            
            system_prompt = \"\"\"You are a bot that adds two numbers and then needs to remember what was calculated for the future.
            Your memories should include the entire calculation, not just the answer.
            After adding the current calculation provide an overwiev of all previously done calculations.
            Your memories should follow the sceme: 'Calculation: x + y = z'.\"\"\"

            memory_db = Vector_DB(db_name=\"example\")
            robot = Robot(memory_vector_DB=memory_db, system_prompt=system_prompt, additional_tools=[add_numbers])"""

        openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")

        tools = [self.__add_to_memory, self.__get_from_memory]
        for tool in additional_tools:
            tools.append(tool)
        
        self.__memory_db = memory_vector_db
        self.__memory_db_id = id(self.__memory_db)

        memory_system_promt = f"""Your 'memory_db_id' = '{str(self.__memory_db_id)}'\n
        You are responsible for managing the Memory.
        Only use information that is provied to you! Don't make something up!
        When recalling memories, give back all the relevant information for the requested subject and leave out the unimportant parts."""

        self.__memory_agent = Agent(openai_api_key=openai_api_key, openai_model = "gpt-3.5-turbo", temperature = 0.15, tools = [self.__query_memory], system_prompt = memory_system_promt, max_iterations = 2, debug=debug)
        self.__memory_agent_id = id(self.__memory_agent)
        self.__main_agent = Agent(openai_api_key=openai_api_key, openai_model=openai_model, temperature=temperature, tools=tools, system_prompt="Your 'memory_db_id' = '" + str(self.__memory_db_id) + "'\nYour 'memory_agent_id' = '" + str(self.__memory_agent_id) + "'\n\n" + system_prompt, max_iterations=None, debug=debug)

    @tool
    def __add_to_memory(memory_db_id : int, memory : str) -> str:
        """Use this tool when you need to remember something in the future.
        Your memory should follow the following format:
        'Broad Topic' : '<broad_topic>'; 'Sub Topic' : '<sub_topic>'; 'Memory' : '<memory>'
        Replace the placeholders <> with the corosponding values."""

        cast(memory_db_id, py_object).value.add_to_db(memory)
        return "You will remember this from now on, simply look for the topic in your memory."

    @tool
    def __get_from_memory(memory_agent_id : int, query : str) -> str:
        """Use this tool when you need to remember about a topic.
        You can provide a broad or sub topic as the query."""

        return cast(memory_agent_id, py_object).value.execute(f"Recall everything in the memory about:\n{query}")


    @tool
    def __query_memory(memory_db_id : int, query : str) -> str:
        """Use this tool to look into your memory.
        The query should be the broad subject you want to recall about."""

        report = "You found the following in your memory:\n\n"
        for result in cast(memory_db_id, py_object).value.get_from_db(query, 10, 0.75):
            report += result + "\n"
        return report
    
    
    def execute(self, prompt : str) -> str:
        """Execute the agent with the given prompt as user input.
        
        Arguments:

            `prompt`: The prompt for the agent as user input.
                
        Returns: 
        
            The agent output after fully executing."""
        
        return self.__main_agent.execute(prompt=prompt)
