#!/usr/bin/env python3
import ollama
import sys
import os
import subprocess

def get_command(user_input):
    system_prompt = (
        "you are a linux terminal assistant. translate the user request into a SIGNALL shell command"
        "output ONLY raw command. No bactricks , no quotes , no explaination"
    )
    response = ollama.chat(
        model='llama3',
        messages=[
            {'role' : 'system' , 'content' : system_prompt},
            {'role' : 'user' , 'content' : user_input}
        ]
    )
    return response['message']['content'].strip()

def main():
    if len(sys.argv)<2:
        print("usage: termass <your request in english>")
        return
    
    user_request = " ".join(sys.argv[1:])
    command = get_command(user_request)

    print(f"\nAI Suggestion: {command}")

    confirm = input("Run this ? (y/n) :").lower()
    if confirm =='y':
        subprocess.run(command,shell=True)
    else:
        print("Aborted.")
        

if __name__ == "__main__":
    main()
    

