
async def main(chat_history, input, file_path, output_callback, file_callback, send_ui):
    from GeneralAgent import skills
    from GeneralAgent.tools import Tools
    from GeneralAgent.interpreter import RoleInterpreter, AsyncPythonInterpreter
    from GeneralAgent.agent import Agent
    workspace = './'
    role_interpreter = RoleInterpreter()
    role_interpreter.system_prompt_template = """
Now: {{now}}
You a python expert.
You can use predefined functions in Python code to create and send UI elements to the user.
Please note that you should only use known Python functions in your code.
Please do the job immediately without asking for permission.
"""
    tools = Tools([
        skills.create_ui,
        ])
    import_code = """
from GeneralAgent import skills
create_ui = skills.create_ui
"""
    # libs = skills.get_current_env_python_libs()
    libs = ''
    python_interpreter = AsyncPythonInterpreter(serialize_path=f'{workspace}/code.bin', libs=libs, import_code=import_code, tools=tools)
    python_interpreter.async_tools = [send_ui]
    output_interpreters = [role_interpreter, python_interpreter]
    agent = Agent(workspace, output_interpreters=output_interpreters, model_type='smart')
    await agent.run(input, output_callback=output_callback)