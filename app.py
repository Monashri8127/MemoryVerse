import streamlit as st
import os
import json
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MemoryVerse: AI-Powered Digital Identity System",
    page_icon="🧠",
    layout="wide"
)

# --- DATA PERSISTENCE SETUP ---
DATA_FILE = "memoryverse_data.json"

def load_data():
    """Loads saved items from memoryverse_data.json if it exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    # Default fallback data if no file exists yet
    return [
        {
            "title": "Online Voting System Project Report",
            "category": "Projects",
            "date": "2026-06-01",
            "skills": ["Python", "SQL", "HTML", "Database Management"],
            "summary": "Built full-stack secure electronic voting system with relational schema."
        },
        {
            "title": "AI & ML Internship Completion Letter",
            "category": "Internships",
            "date": "2026-06-08",
            "skills": ["Python", "Machine Learning", "RAG Systems"],
            "summary": "Completed AI/ML internship focusing on data pipelines and LLM applications."
        },
        {
            "title": "MongoDB Developer Certification",
            "category": "Certifications",
            "date": "2026-08-15",
            "skills": ["MongoDB", "NoSQL", "Database Design"],
            "summary": "Demonstrated expertise in aggregation pipelines, indexing, and document modeling."
        },
        {
            "title": "AWS Certified Solutions Architect",
            "category": "Certifications",
            "date": "2026-10-20",
            "skills": ["Python", "Problem Solving"],
            "summary": "Processed document: AWS Certified Solutions Architect"
        }
    ]

def save_data(items):
    """Saves the current list of items to memoryverse_data.json permanently."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4)

# Initialize Session State
if "repository_items" not in st.session_state:
    st.session_state["repository_items"] = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation Module")
module = st.sidebar.selectbox(
    "Select Module",
    [
        "Module 1 & 2: Ingestion & Parsing",
        "Module 3: Relationship Graph",
        "Module 4: Digital Journey Timeline",
        "Module 5: Smart Retrieval System (Natural Search)"
    ]
)

# --- HEADER ---
st.title("🧠 MemoryVerse: AI-Powered Digital Identity System")
st.markdown("Transforming fragmented academic and professional data into an intelligent knowledge repository.")
st.warning("⚠️ Gemini API Key not set. Add your API key at the top of app.py to enable real AI parsing!")

st.markdown("---")

# ==========================================
# MODULE 1 & 2: INGESTION & PARSING
# ==========================================
if module == "Module 1 & 2: Ingestion & Parsing":
    st.subheader("Module 1 & 2: Document Ingestion & Auto-Categorization")
    st.markdown("Upload certificates, project reports, or paste your career milestones to index them.")

    with st.form("ingest_form"):
        title_input = st.text_input("Milestone Title (e.g., Python Certification)")
        category_input = st.selectbox("Category", ["Certifications", "Projects", "Internships", "Hackathons"])
        date_input = st.date_input("Date")
        skills_input = st.text_input("Key Skills (comma-separated, e.g., Python, SQL, Streamlit)")
        summary_input = st.text_area("Summary / Description")
        
        submit_btn = st.form_submit_button("Process & Save Record")
        
        if submit_btn:
            if title_input:
                new_item = {
                    "title": title_input,
                    "category": category_input,
                    "date": str(date_input),
                    "skills": [s.strip() for s in skills_input.split(",") if s.strip()],
                    "summary": summary_input
                }
                st.session_state["repository_items"].append(new_item)
                save_data(st.session_state["repository_items"])
                st.success(f"Successfully added and saved '{title_input}' permanently!")
            else:
                st.error("Please provide at least a milestone title.")

# ==========================================
# MODULE 3: INTELLIGENT RELATIONSHIP ENGINE
# ==========================================
elif module == "Module 3: Relationship Graph":
    st.subheader("Module 3: Intelligent Relationship Engine")
    st.markdown("Explore interactive connections between your credentials, projects, and underlying technical skills.")

    G = nx.Graph()
    items = st.session_state.get("repository_items", [])

    for item in items:
        title = item.get("title", "Milestone")
        category = item.get("category", "General")
        
        G.add_node(title, label=title, color="#ff4b4b", group=category)
        G.add_node(category, label=category, color="#1f77b4", group="Category")
        G.add_edge(title, category)
        
        for skill in item.get("skills", []):
            G.add_node(skill, label=skill, color="#2ca02c", group="Skill")
            G.add_edge(title, skill)

    net = Network(height="500px", width="100%", bgcolor="#0e1117", font_color="white")
    net.from_nx(G)
    
    html_path = "graph.html"
    net.save_graph(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    components.html(html_content, height=520, scrolling=True)

# ==========================================
# MODULE 4: DIGITAL JOURNEY TIMELINE
# ==========================================
elif module == "Module 4: Digital Journey Timeline":
    st.subheader("Module 4: Digital Journey Timeline")
    st.markdown("Chronological representation of your academic and professional growth.")

    items = st.session_state.get("repository_items", [])
    sorted_items = sorted(items, key=lambda x: x.get("date", ""))

    for item in sorted_items:
        st.markdown(f"### 📅 {item.get('date')} — {item.get('title')}")
        st.markdown(f"* **Category:** `{item.get('category')}`")
        st.markdown(f"* **Key Skills:** {', '.join(item.get('skills', []))}")
        st.markdown(f"* **Summary:** {item.get('summary')}")
        st.markdown("---")

# ==========================================
# MODULE 5: SMART RETRIEVAL SYSTEM
# ==========================================
elif module == "Module 5: Smart Retrieval System (Natural Search)":
    st.subheader("Module 5: Smart Retrieval System (Natural Search)")
    st.markdown("Instantly search your repository using natural language prompts.")

    query = st.text_input("Ask MemoryVerse anything (e.g., 'Show Python projects', 'What certifications do I have?')")

    if query:
        items = st.session_state.get("repository_items", [])
        query_lower = query.lower()
        
        results = []
        for item in items:
            searchable_text = f"{item.get('title', '')} {item.get('category', '')} {' '.join(item.get('skills', []))} {item.get('summary', '')}".lower()
            if any(word in searchable_text for word in query_lower.split()):
                results.append(item)
                
        if results:
            st.success(f"Found {len(results)} matching records:")
            for res in results:
                with st.expander(f"📌 {res.get('title')} ({res.get('category')})"):
                    st.write(f"**Date:** {res.get('date', 'N/A')}")
                    st.write(f"**Skills:** {', '.join(res.get('skills', []))}")
                    st.write(f"**Summary:** {res.get('summary', '')}")
        else:
            st.info("No matching records found in repository.")