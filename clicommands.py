import os
def show_help():
    print(f"""
OCRForge - A Smart OCR Utility tool
          
Commands:
          --v: triggers voice talkback.
          --nv: disables voice talkback
        Note: run python {os.path.basename(__file__)} --v (or --nv), it toggles the mode to your preference.
              Then upon next file startup you dont need to specify unless you want to change the mode.

          --docs: Gives you the link to detailed documentation available on OCRforge CLI's GitHub Repository

          --history: shows you the history of your previous OCR executions
        Note: the github repo doesnt include a history log file. Please create a history_log.json file in the
              same directory as rest files to save your history. If you want to store it in a different location
              you can change it in config.py file

Additional points to remember: 
        1. Make sure to install all the dependencies before running the tool.
        2. Ensure you have a valid Groq API key stored in a env variable GROQ_API_KEY.
        3. If you want you can upgrade the API to a more premium one such as OpenAI's or Claude's
        4. If you find any issue or wish to contribute to this project, make sure to do it via Gtihub.
        
That's it! it's simple to use and highly effective, be it your summarizing pains, or your homework, or some information your curiosity demands,
OCR Forge has got it all sorted for you!

I hope you like to use this tool. Please send me your feedback via Github or Linkedin.
                                          
                                                                                        - Signing off (for now!)
                                                                                          Dewashish Hemant Lambore
                                                                                          (Original Creator)
                                                                                          24/05/25 
""")
    
    
def show_docs():
    
    print("\nPlease refer to the following for detailed documentation, quickstart guide and setup guide:\n🔗 GitHub Repository: https://github.com/DewashishCodes/OCR-Forge-CLI")