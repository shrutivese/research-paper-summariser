import os
import time
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Define output directory
OUT_DIR = "data"
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# Base URL for arXiv search
BASE_URL = "http://export.arxiv.org/api/query?"

# Search query parameters
MAX_RESULTS = 5  # Number of results per API call (latest 5 papers)

# Mapping of categories to arXiv categories
CATEGORIES = {
    'Artificial Intelligence': 'cs.AI',
    'Hardware Architecture': 'cs.AR',
    'Computational Complexity': 'cs.CC',
    'Computational Engineering, Finance, and Science': 'cs.CE',
    'Computational Geometry': 'cs.CG',
    'Computation and Language': 'cs.CL',
    'Cryptography and Security': 'cs.CR',
    'Computer Vision and Pattern Recognition': 'cs.CV',
    'Computers and Society': 'cs.CY',
    'Databases': 'cs.DB',
    'Distributed, Parallel, and Cluster Computing': 'cs.DC',
    'Digital Libraries': 'cs.DL',
    'Discrete Mathematics': 'cs.DM',
    'Data Structures and Algorithms': 'cs.DS',
    'Emerging Technologies': 'cs.ET',
    'Formal Languages and Automata Theory': 'cs.FL',
    'General Literature': 'cs.GL',
    'Graphics': 'cs.GR',
    'Computer Science and Game Theory': 'cs.GT',
    'Human-Computer Interaction': 'cs.HC',
    'Information Retrieval': 'cs.IR',
    'Information Theory': 'cs.IT',
    'Machine Learning': 'cs.LG',
    'Logic in Computer Science': 'cs.LO',
    'Multiagent Systems': 'cs.MA',
    'Multimedia': 'cs.MM',
    'Mathematical Software': 'cs.MS',
    'Numerical Analysis': 'cs.NA',
    'Neural and Evolutionary Computing': 'cs.NE',
    'Networking and Internet Architecture': 'cs.NI',
    'Other Computer Science': 'cs.OH',
    'Operating Systems': 'cs.OS',
    'Performance': 'cs.PF',
    'Programming Languages': 'cs.PL',
    'Robotics': 'cs.RO',
    'Symbolic Computation': 'cs.SC',
    'Sound': 'cs.SD',
    'Software Engineering': 'cs.SE',
    'Social and Information Networks': 'cs.SI',
    'Systems and Control': 'cs.SY'
}

def fetch_papers(category, max_results=10):
    """
    Fetch papers from arXiv API based on the search query.
    Args:
        category: The category to search for.
        max_results: The maximum number of results to fetch.
    Returns:
        A list of papers with their metadata.
    """
    search_query = f"search_query=cat:{CATEGORIES[category]}&sortBy=submittedDate&sortOrder=descending"
    url = f"{BASE_URL}{search_query}&max_results={max_results}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def parse_papers(xml_data):
    """
    Parse the XML data returned by the arXiv API to extract paper metadata.
    Args:
        xml_data: The XML data as a string.
    Returns:
        A list of dictionaries containing paper metadata.
    """
    soup = BeautifulSoup(xml_data, 'xml')
    entries = soup.find_all('entry')
    papers = []
    for entry in entries:
        paper = {
            'id': entry.id.text,
            'title': entry.title.text.strip(),
            'summary': entry.summary.text.strip(),
            'published': entry.published.text,
            'authors': [author.find('name').text for author in entry.find_all('author')],
            'link': entry.find('link', {'type': 'text/html'})['href']
        }
        papers.append(paper)
    return papers

def save_papers_as_text(papers, output_dir):
    """
    Save the paper metadata to text files in the output directory.
    Args:
        papers: A list of dictionaries containing paper metadata.
        output_dir: The directory to save the files in.
    """
    for paper in papers:
        paper_id = paper['id'].split('/')[-1]
        filename = os.path.join(output_dir, f"{paper_id}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {paper['title']}\n")
            f.write(f"Authors: {', '.join(paper['authors'])}\n")
            f.write(f"Published: {paper['published']}\n")
            f.write(f"Link: {paper['link']}\n\n")
            f.write(f"Summary:\n{paper['summary']}\n")
        time.sleep(1)  # Be polite and avoid hitting the server too hard

def main(category):
    print(f"Fetching latest {MAX_RESULTS} papers for {category}...")
    xml_data = fetch_papers(category, max_results=MAX_RESULTS)
    if xml_data:
        papers = parse_papers(xml_data)
        if papers:
            save_papers_as_text(papers, OUT_DIR)
            return papers
        else:
            print("No papers found.")
            return []
    else:
        print("Failed to fetch papers.")
        return []

def ask_question(prompt):
    """
    Ask a question to the microservice running at pathway:8000.
    Args:
        prompt: The question to ask.
    Returns:
        The response from the microservice.
    """
    url = "http://pathway:8000/v1/pw_ai_answer"
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get a response from the microservice."}

# Streamlit UI
st.title("Research Paper Summariser")

# Define the available categories
categories = list(CATEGORIES.keys())

# User selects their area of interest
category = st.selectbox("Choose your area of interest:", categories)

# Initialize a session state variable to store fetched papers
if 'papers' not in st.session_state:
    st.session_state.papers = []

if st.button("Fetch Papers"):
    st.session_state.papers = main(category)

# Sidebar for introduction and displaying fetched paper titles
st.sidebar.header("Introduction")
st.sidebar.write("""
This project allows you to fetch the latest research papers from arXiv based on your area of interest.
1. Select an area of interest from the dropdown menu.
2. Click the 'Fetch Papers' button to get the top 5 latest papers in that category.
3. You can then ask questions related to the fetched papers.
""")

if st.session_state.papers:
    st.sidebar.header("Fetched Papers")
    for paper in st.session_state.papers:
        st.sidebar.write(paper['title'])

# Main page for displaying dropdowns and questions
if st.session_state.papers:
    st.header("Ask Questions")
    paper_titles = [paper['title'] for paper in st.session_state.papers]
    selected_paper_title = st.selectbox("Select a paper to ask questions about:", paper_titles)
    technical_level = st.selectbox("Select your technical understanding level:", ["Basic", "Intermediate", "Advanced"])

    # question = st.text_area("Type your question here:")
    if st.button("Submit Question"):
        selected_paper = next(paper for paper in st.session_state.papers if paper['title'] == selected_paper_title)
        prompt = f"Please summarize the following paper at a {technical_level.lower()} level of technical understanding:\n\nTitle: {selected_paper['title']}\n\nSummary: {selected_paper['summary']}\n"
        response = ask_question(prompt)
        st.write("Response:", response)
else:
    st.write("No papers fetched yet. Please select a category and click 'Fetch Papers'.")
