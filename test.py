# # Step 1: Define tools and model

# from langchain.tools import tool
# from langchain.chat_models import init_chat_model
# from dotenv import load_dotenv

# load_dotenv()

# model = init_chat_model(
#     "gpt-4.1",
#     temperature=0
# )


# # Define tools
# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply `a` and `b`.

#     Args:
#         a: First int
#         b: Second int
#     """
#     return a * b


# @tool
# def add(a: int, b: int) -> int:
#     """Adds `a` and `b`.

#     Args:
#         a: First int
#         b: Second int
#     """
#     return a + b


# @tool
# def divide(a: int, b: int) -> float:
#     """Divide `a` and `b`.

#     Args:
#         a: First int
#         b: Second int
#     """
#     return a / b


# # Augment the LLM with tools
# tools = [add, multiply, divide]
# tools_by_name = {tool.name: tool for tool in tools}
# model_with_tools = model.bind_tools(tools)

# from langgraph.graph import add_messages
# from langchain.messages import (
#     SystemMessage,
#     HumanMessage,
#     ToolCall,
# )
# from langchain_core.messages import BaseMessage
# from langgraph.func import entrypoint, task


# # Step 2: Define model node

# @task
# def call_llm(messages: list[BaseMessage]):
#     """LLM decides whether to call a tool or not"""
#     return model_with_tools.invoke(
#         [
#             SystemMessage(
#                 content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
#             )
#         ]
#         + messages
#     )


# # Step 3: Define tool node

# @task
# def call_tool(tool_call: ToolCall):
#     """Performs the tool call"""
#     tool = tools_by_name[tool_call["name"]]
#     return tool.invoke(tool_call)


# # Step 4: Define agent

# @entrypoint()
# def agent(messages: list[BaseMessage]):
#     model_response = call_llm(messages).result()

#     while True:
#         if not model_response.tool_calls:
#             break

#         # Execute tools
#         tool_result_futures = [
#             call_tool(tool_call) for tool_call in model_response.tool_calls
#         ]
#         tool_results = [fut.result() for fut in tool_result_futures]
#         messages = add_messages(messages, [model_response, *tool_results])
#         model_response = call_llm(messages).result()

#     messages = add_messages(messages, model_response)
#     return messages

# # Invoke
# messages = [HumanMessage(content="Add 3 and 4.")]
# for chunk in agent.stream(messages, stream_mode="messages"):
#     print(chunk)
#     print("\n")
class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.program_counter = {}
        self.cache = {}

    def get(self, key: int) -> int:
        if key in self.cache.keys():
            self.program_counter[key] += 1 
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if len(self.cache.keys()) < self.capacity:
            self.cache[key] = value
            self.program_counter[key] = 1

        else:
            keys, values = self.program_counter.keys(), self.program_counter.values()
            lru = min(values)
            lru_index = list(values).index(lru)
            self.cache.pop(list(keys)[lru_index])
            self.cache[key] = value

obj = LRUCache(2)
obj.put(1, 1)
obj.put(2, 2)
print(obj.get(1))
print(obj.program_counter)    # return 1
obj.put(3, 3) 
print(obj.cache)       # evicts key 2
print(obj.get(2))    # return -1 (not found)
obj.put(4, 4)
print(obj.cache)       # evicts key 1
print(obj.get(1))    # return -1 (not found)
print(obj.get(3))    # return 3
print(obj.get(4))    # return 4

# items = [1, 1, 2, 3, 2, 4]
# counts = {}

# for item in items:
#     if item in counts:
#         counts[item] += 1
#     else:
#         counts[item] = 1

# print(counts)
# key, values = counts.keys(), counts.values()
# print(min(values))
