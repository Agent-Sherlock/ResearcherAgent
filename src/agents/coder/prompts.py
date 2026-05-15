from src.shared.utils.general_utils import clean_docstring

task_instruction = clean_docstring("""
You are an expert developer. Your task is to implement a solution based on the provided idea.
Problem Statement:
{problem_statement}
Candidate Idea to Implement:
{candidate_idea}
Current Code Context:
{current_code}
Instructions:
1. Write the code to implement the candidate idea.
2. You MUST edit the existing file at {target_file_path} using the str_replace command. Do not create a new file:
    {target_file_path}

Keep in mind to act on behalf of these guidelines:
{improvement_scope}
As the code will later be evaluated by a verifier. 
""")
