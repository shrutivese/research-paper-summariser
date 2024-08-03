# research-paper-summariser
A research paper summarization tool using LLM that fetches the latest research papers from arXiv based on your area of interest. Using a Streamlit interface, users can select their field, fetch the top 5 latest papers, and ask questions to get tailored summaries at different technical levels (Basic, Intermediate, Advanced).

# demo

https://github.com/shrutivese/research-paper-summariser/assets/155245815/82d3e7a3-0e6c-41b3-a199-a56437324dba

# built using
- Gemini LLM : Since the research papers may contain graphs and diagrams a amultimodal LLM such as Gemini may result in better output.
- Pathway : Provides powerful pipeline
- Streamlit
- vsolatorio/GIST-small-Embedding-v0 Embedder

# how it works
![Concept map (2)](https://github.com/shrutivese/research-paper-summariser/assets/155245815/aad1c873-2a94-4e0e-a9de-d2dec8333fed)

The project contains two folders - 
1. demo-question-answering : This is from Pathway's llm app repo : https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/demo-question-answering
The code has been modified to include the Gemini pro LLM model instead of OpenAI. This code  essentially implements the RAG question answering.

2. paper-source : This contains the code for the Streamlit UI elements and the code to gather resource papers via arXiv API calls. Within this , a data folder is created which stores the necessary information

The above 2 services are run on docker on port 8000 and 8501 respectively. Requests from paper-source to genrate a summary is sent to the pathway demo-question-answering service , which generates a summary suited to user's chosen level of understanding (basic/advanced/intermediate).

# how to run
1. Create a Gemini API key 
2. Create a .env file in the demo-question-answering file and store the Gemini Api key :  GEMINI_API_KEY=******* (put the key in quotes)
3. Install docker desktop
4. Use docker-compose up --build
5. Navigate to localhost:8501 for the streamlit UI
6. Select your area of interest from the dropdown and click on fetch papers
7. After papers are fetched . select the paper to be summarised , your level of understanding from the drpopdown and click on submit question.





