import base64

graph = """
graph LR
    User([👤 User]) -->|1. Topic| Scanner[🔍 Scanner Agent]
    Scanner -->|2. Tickers| Team
    
    subgraph Team [Analyst Team]
        direction TB
        Tech[📈 Technical]
        Inst[🏛️ Institutional]
        Social[🐦 Social]
    end
    
    Team -->|3. Analysis| Summarizer[📝 Summarizer Agent]
    Summarizer -->|4. Report| Email[📧 Email Agent]
    Email -.->|5. Send| User
    
    classDef agent fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef user fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    
    class Scanner,Summarizer,Email,Tech,Inst,Social agent;
    class User user;
"""

graph_bytes = graph.encode("utf8")
base64_bytes = base64.b64encode(graph_bytes)
base64_string = base64_bytes.decode("ascii")

url = f"https://mermaid.ink/img/{base64_string}?type=png"
print(url)
