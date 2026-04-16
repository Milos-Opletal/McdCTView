import os
import json
from dotenv import load_dotenv
from MyMcdAPI import MyMcdAPI

load_dotenv()

def main():
    email = os.environ['MCD_EMAIL']
    password = os.environ['MCD_PASSWORD']
    api = MyMcdAPI(email, password)
    api.login()
    
    codes = api.get_default_codes()
    verifications = codes.get("verifications", [])
    
    names = []
    for v in verifications:
        name_cs = v.get("name", {}).get("cs", "").strip()
        name_sk = v.get("name", {}).get("sk", "").strip()
        display_name = name_cs or name_sk
        if display_name:
            names.append(display_name)
    
    names.sort()
    for name in names:
        print(f"- {name}")

if __name__ == '__main__':
    main()
