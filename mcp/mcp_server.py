from mcp.server.fastmcp import FastMCP
 
app = FastMCP() #pip mcp dev (filename)
 
@app.tool()
def addNum(a: int, b:int):
    return a+b
 
 
@app.resource("hello://{name}")
def welcome(name: str):
    return f"Hi {name}"
 
 
@app.prompt()
def code_review(code: str, language: str) -> str:
    """A prompt to request a quick code review for a given language."""
    return f"""Please review the {code} following {language} code for bugs, performance issues, and best practices"""
