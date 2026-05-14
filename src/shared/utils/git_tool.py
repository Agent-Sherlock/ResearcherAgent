import subprocess
import os

def _run_git_command(command: list[str], cwd: str = None) -> dict:
    # Execute a git command and return a structured dictionary
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {
            "success": False, 
            "error": e.stderr.strip() if e.stderr else e.stdout.strip(), 
            "command": " ".join(command)
        }
    except Exception as e:
        return {
            "success": False, 
            "error": str(e), 
            "command": " ".join(command)
        }

def write_to_file(file_path: str, content: str) -> dict:
    # Overrides the entire content of a file, creating directories if needed
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return {
            "success": True, 
            "message": f"Successfully wrote {len(content)} characters to {file_path}"
        }
    except Exception as e:
        return {
            "success": False, 
            "error": str(e)
        }

def git_create_repo(repo_path: str) -> dict:
    # Check if the repository already exists
    if os.path.exists(os.path.join(repo_path, ".git")):
        return {"success": True, "message": f"Repository already exists at {repo_path}"}
        
    # Ensure the target directory exists before initializing
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        
    init_res = _run_git_command(["git", "init"], cwd=repo_path)
    if not init_res["success"]:
        return init_res
    
    # Create an initial empty commit so branches can be created normally
    commit_res = _run_git_command(["git", "commit", "--allow-empty", "-m", "Initial commit"], cwd=repo_path)
    if not commit_res["success"]:
        return commit_res
        
    return {"success": True, "message": f"Successfully initialized repository at {repo_path}"}

def git_create_branch(repo_path: str, branch_name: str) -> dict:
    # Check if the branch already exists
    check_res = _run_git_command(["git", "branch", "--list", branch_name], cwd=repo_path)
    if check_res["success"] and check_res["output"].strip():
        return {"success": True, "message": f"Branch '{branch_name}' already exists"}

    # Create a new branch from the current HEAD
    res = _run_git_command(["git", "branch", branch_name], cwd=repo_path)
    if not res["success"]:
        return res
        
    return {"success": True, "message": f"Successfully created branch '{branch_name}'"}

def git_commit_to_branch(repo_path: str, branch_name: str, commit_message: str, files_to_add: str = ".") -> dict:
    # Switch to the target branch
    checkout_res = _run_git_command(["git", "checkout", branch_name], cwd=repo_path)
    if not checkout_res["success"]:
        return checkout_res
        
    # Stage the specified files
    add_res = _run_git_command(["git", "add", files_to_add], cwd=repo_path)
    if not add_res["success"]:
        return add_res
        
    # Check if there are any changes to commit using git status
    status_res = _run_git_command(["git", "status", "--porcelain"], cwd=repo_path)
    if status_res["success"] and not status_res["output"].strip():
        return {"success": True, "message": f"No changes to commit on '{branch_name}'"}
        
    # Commit the staged changes
    commit_res = _run_git_command(["git", "commit", "-m", commit_message], cwd=repo_path)
    if not commit_res["success"]:
         return commit_res
         
    return {"success": True, "message": f"Successfully committed to '{branch_name}'"}

def git_get_history(repo_path: str, branch_name: str, max_commits: int = 50) -> dict:
    # Retrieve only the commit hashes for a specific branch as a list
    command = [
        "git", 
        "log", 
        branch_name,
        f"-{max_commits}", 
        "--format=%h"  # %h for short hash, use %H for full long hash
    ]
    
    res = _run_git_command(command, cwd=repo_path)
    
    if not res["success"]:
        return res
        
    # Split the output by newlines to create a clean Python list
    # The list comprehension ensures we drop any empty strings
    hashes = [h.strip() for h in res["output"].split("\n") if h.strip()]
        
    return {
        "success": True, 
        "hashes": hashes
    }

def git_read_file_from_commit(repo_path: str, commit_hash: str, file_path: str) -> dict:
    # Reads the exact contents of a file at a specific point in Git history
    command = ["git", "show", f"{commit_hash}:{file_path}"]
    
    res = _run_git_command(command, cwd=repo_path)
    
    # Handle the specific error where the file didn't exist yet in that commit
    if not res["success"]:
        if "exists on disk, but not in" in res.get("error", "") or "fatal: path" in res.get("error", ""):
            return {
                "success": False, 
                "error": f"File '{file_path}' did not exist in commit {commit_hash}."
            }
        return res
        
    return {
        "success": True, 
        "content": res["output"]
    }