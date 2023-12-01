
async def get_function_builder_agent():
    """
    Get a function builder agent
    """
    from GeneralAgent.agent import Agent
    from GeneralAgent import skills
    from GeneralAgent.interpreter import RoleInterpreter, PythonInterpreter, FileInterpreter, ShellInterpreter
    from GeneralAgent.utils import get_functions_dir
    function_dir = get_functions_dir()
    role_prompt = f"""
You are an agent who writes python functions into files according to user needs.
You can control your computer and access the Internet.

# make a directory for function file and test dataset
```shell
mkdir -p {function_dir}/functoin_folder_name
```

# copy files uploaded by users to the function file directory
```shell
cp yy.zz {function_dir}/functoin_folder_name/yy.zz
```

# When writing a function, you can first search for available functions. For Example
```python
result = search_functions('scrape web page')
print(result)
```

# The function should be written in the folder {function_dir}/functoin_folder_name, and the file name should be the function name
# The content of the file is the function and the test function of the function (starting with test_)
#Import code should be placed inside the function
for example:

```file
{function_dir}/function_folder_name/function_name.py write 0 -1 <<EOF
def function_name(xx)
     importxx
     pass
def test_function_name(xx)
     pass
EOF
```

# The written functions can be accessed through GeneralAgent's skills library, such as:

```python
from GeneralAgent import skills
result = skills.function_name()
skills.test_function_name()
```

# Note:
- Don't make up functions that don't exist

# General process for write function
* Fully communicate needs with users
* search available functions (by search_functions in python, optional)
* edit functions (by file operation)
* test functions (by python)
* ask for test files if needed, for example test data, test code, etc.
"""
    functoins = [
        skills.search_functions,
        # skills.scrape_dynamic_web
    ]
    workspace = './'
    agent = Agent(workspace)
    role_interpreter = RoleInterpreter(system_prompt=role_prompt)
    python_interpreter = PythonInterpreter(serialize_path=f'{workspace}/code.bin')
    python_interpreter.function_tools = functoins
    
    # when file operation(python file), reload functions
    file_interpreter = FileInterpreter()
    async def reload_funs():
        skills._load_remote_funs()
    
    file_interpreter.outptu_parse_done_recall = reload_funs
    agent.interpreters = [role_interpreter, python_interpreter, FileInterpreter(), ShellInterpreter()]
    agent.model_type = 'smart'
    agent.hide_output_parse = False
    return agent