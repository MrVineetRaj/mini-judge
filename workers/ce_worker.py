from services.redis import redis_conn,RedisQueue
from utils.config import mini_judge_config
from rq import Queue
import os
import subprocess
from utils.languages import LANGUAGE_EXTENSIONS
from utils.db import update_submission_output
import shutil
from utils.external_api import send_webhook


queue_name = mini_judge_config["QUEUE_NAME"]


codeExecutionJob = RedisQueue(queue_name=queue_name,redis_conn=redis_conn)

codeExecutionQueue:Queue = RedisQueue.getQueue(codeExecutionJob)


def execute_code(language:int,folder_path:str,id:str):
  ext = LANGUAGE_EXTENSIONS[language]
  submission_file = f"{folder_path}/submission.{ext}"
  input_file =  f"{folder_path}/stdin.txt"
  
  try:
    # Run Node.js process with stdin redirected from the file
    input = open(input_file, "r").read()
    print("input",input)
    stdout = ""
    stderr = ""
    if(language == 1):
      result = subprocess.run(
          ["node", submission_file],
          input=input,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
          timeout=2  # optional: to prevent infinite loops
      )
      stdout=result.stdout
      stderr=result.stderr
    elif(language == 2):
      result = subprocess.run(
          ["python3", submission_file],
          input=input,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
          timeout=2  # optional: to prevent infinite loops
      )
      print(result)
      stdout=result.stdout
      stderr=result.stderr
    elif(language == 3):
      executable_file = f"{folder_path}/submission.out"
      compile_process = subprocess.run(
        ["g++", submission_file, "-o", executable_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
      )
      if compile_process.returncode != 0:
          print("=== COMPILATION ERROR ===")
          print(compile_process.stderr.strip())
          return {"stdout": "", "stderr": compile_process.stderr, "error": "Compilation failed"}

      # Run step
      result = subprocess.run(
          [executable_file],
          input=input,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
          timeout=2
      )

      stdout = result.stdout
      stderr = result.stderr

    print("\n\n\n\n")
    # Print outputs
    print("=== STDOUT ===")
    print(stdout)
    print("=== STDERR ===")
    print(stderr)

    submission_detail = update_submission_output(id,stdout,stderr)
    webhook_url = submission_detail["webhook"]


    send_webhook(submission=submission_detail,message="code executed")



    if os.path.exists(folder_path):
      shutil.rmtree(folder_path)
    # if result.stderr:
    #     print("=== STDERR ===")
    #     print(result.stderr.strip())


    print("\n\n\n\n")
  except subprocess.TimeoutExpired:
    print("Execution timed out! The code took too long.")
  except Exception as e:
      print("Something went wrong:", e)
