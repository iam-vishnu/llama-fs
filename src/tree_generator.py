#!/usr/local/bin/python3.10

from groq import Groq
import json
import ollama
import os

FILE_PROMPT = """
You will be provided with list of source files and a summary of their contents. For each file, propose a new path and filename, using a directory structure that optimally organizes the files using known conventions and best practices.
Follow good naming conventions. Here are a few guidelines
- Think about your files : What related files are you working with?
- Identify metadata (for example, date, sample, experiment) : What information is needed to easily locate a specific file?
- Abbreviate or encode metadata
- Use versioning : Are you maintaining different versions of the same file?
- Think about how you will search for your files : What comes first?
- Deliberately separate metadata elements : Avoid spaces or special characters in your file names
If the file is already named well or matches a known convention, set the destination path to the same as the source path.

Dont give any explanations. Your response must be a JSON object with the following schema: 
```json
{
    "files": [
        {
            "src_path": "original file path",
            "dst_path": "new file path under proposed directory structure with proposed file name"
        }
    ]
}
```
""".strip()


def create_file_tree(summaries: list):
    # client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    client = ollama.Client()
    # chat_completion = client.chat.completions.create(
    chat_completion = client.chat(
        messages=[
            {"role": "system", "content": FILE_PROMPT},
            {"role": "user", "content": json.dumps(summaries)},
        ],
        model="llama3",
        # response_format={"type": "json_object"},  # Uncomment if needed
        # temperature=0,
    )
    # print(chat_completion["message"]["content"])
    a = chat_completion["message"]["content"]
    print(json.loads(a)['files'])
    print("Printing print(a['files'])")
    # a = dict(a)
    # print(a["files"])
    file_tree = json.loads(a)['files']
    # print(type(a))
    # print(list(a['files']))
    # file_tree = json.loads(chat_completion.choices[0].message.content)["files"]
    return file_tree
