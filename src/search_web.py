import os
from pydantic import SecretStr
import requests
from bs4 import BeautifulSoup
import bs4
from langchain_deepseek import ChatDeepSeek
from googlesearch import search
from server import mcp

# @mcp.prompt()
# def search_web_phone(query: str):
#     return f"""
#     You are an assistant helping users to find information about phones.
#     If the information (e.g. about color, camera, price) cannot be found in the graph database,
#     you must call the `search_web` tool with the original query to find it from the web.

#     The user asked: "{query}"

#     First, try using `retrieve_graph` to query the database. If the result is empty or doesn't contain enough detail,
#     immediately call `search_web(query)` to find and summarize the answer.
#     """

@mcp.tool()
def search_web(query: str, num_results: int = 3):
    """
    Use this tool to search the web when you can't find information about a user's question from the database.
    This tool can be called directly or called after no information is found with the 'retrieve_graph' tool
    Input:
        query: str -> The user query to search the web
        num_results: int -> The number of results to return
    Output:
        answer: str -> The answer from AI
    """
    # 1. Lấy top URL từ Google
    urls = []
    for url in search(query, num_results=num_results, lang="vi"):
        urls.append(url)
    
    # 2. Lấy nội dung chính từ từng URL
    contents = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=7)
            soup = BeautifulSoup(resp.text, "html.parser")
            # Lấy title và đoạn đầu tiên có nội dung
            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            desc = ""
            # Ưu tiên meta description
            meta = soup.find('meta', attrs={'name': 'description'})
            if meta and isinstance(meta, bs4.element.Tag):
                meta_content = meta.get('content', '')
                if isinstance(meta_content, str):
                    desc = meta_content.strip()
            if not desc:
                # Nếu không có, lấy đoạn đầu tiên trong body
                p = soup.find('p')
                if p and p.get_text():
                    desc = p.get_text().strip()
            # Ghép lại
            content = f"{title}\n{desc}"
            contents.append(content)
        except Exception:
            continue
    
    # 3. Gửi lên OpenAI GPT để tóm tắt trả lời
    llm = ChatDeepSeek(
        temperature=0, 
        model="deepseek-chat",
        api_key=SecretStr(os.getenv("DEEPSEEK_API_KEY") or ""),
        api_base=os.getenv("DEEPSEEK_API_BASE") or "",
        max_tokens=1024
    )
    context = "\n\n".join(contents)
    prompt = f"Question: {query}\nBelow is the information found on the web:\n{context} \
    \n\nPlease answer the question above in a short, accurate way."

    try:
        answer = llm.invoke(prompt).content
    except Exception as e:
        answer = "Cannot summarize information from the web. Error: " + str(e)
    return answer

# if __name__ == "__main__":
#     print(search_web("What is the capital of France?"))