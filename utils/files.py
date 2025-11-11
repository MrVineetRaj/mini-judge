import os
from utils.languages import LANGUAGE_EXTENSIONS

def store_file(source_code:str, language:int,id:str,stdin:str):
  try:
    ext = LANGUAGE_EXTENSIONS.get(language)
    folder_path = os.path.join("submissions",id)
    os.makedirs(folder_path,exist_ok=True)
    file_path = os.path.join(folder_path,f"submission.{ext}")
    with open(file_path,'w') as f:
      f.write(source_code)   
    input_file_path = os.path.join(folder_path,f"stdin.txt")
    with open(input_file_path,'w') as f:
      f.write(stdin)

    return {"success":True,"file_path":file_path,"folder_path":folder_path}
  except Exception as e:
    print(f"Error {e}")
    return {"success":False}
  
