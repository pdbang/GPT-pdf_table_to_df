from openai import OpenAI
import json

def get_csv_answer(csv_path, system_prompt, params_properties: dict, model: str = "gpt-3.5-turbo-1106"):
    client = OpenAI()
    
    messages = [{"role": "system", "content": system_prompt}]

    tools = [{
        "type": "function",
        "function":{
        
            "name": "to_csv",
            "description": "Create a csv file from the given parameters",
            "parameters": params_properties
    }
    }
    ]

    with open(csv_path, "r", encoding="utf-8") as f:
        messages.append({"role": "user", "content": f.read()})

    response = client.chat.completions.create(messages=messages,
                                   model=model,
                                   tool_choice={"type": "function", "function": {"name": "to_csv"}},
                                   tools=tools,
                                   temperature=0)
    
    arguments = response.choices[0].message.tool_calls[0].function.arguments
    print(arguments)
    return json.loads(arguments)


def get_cols_and_rows(csv_path: str, system_prompt: str, model: str = "gpt-3.5-turbo-1106") -> (list, list):
    params_properties = {
        "type": "object",
        "properties": {
            "Columns": {
                "type": "string",
                "description": "list of columns names infered from the csv",
            },
            "Rows": {
                "type": "string",
                "description": "list of rows names infered from the csv"
            }
        },
        "required": ["Columns", "Rows"]
    }
    result = get_csv_answer(csv_path, system_prompt, params_properties, model)
    return result["Rows"], result["Columns"]

def get_csv_with_cols(csv_path: str, system_prompt: str, rows: list, cols: list, model: str = "gpt-3.5-turbo-1106"):
    params_properties = {
        "type": "object",
        "properties": {
            f"{row} ## {col}": {
                "type": "string"
            } for row in rows for col in cols
        },
        "required": []
    }
    return get_csv_answer(csv_path, system_prompt, params_properties, model)