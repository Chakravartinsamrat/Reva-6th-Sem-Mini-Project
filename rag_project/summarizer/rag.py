import os
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class RAGSystem:
    def __init__(self, model_name="llama3.2"):
        
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        
        self.llm = OllamaLLM(model=model_name, temperature=0.3)
    
    
    def create_vector_store(self, text):
        """Split the text and create a vector store."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.split_text(text)
        
        # Create vector store
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        return vector_store
    
    def get_relevant_context(self, vector_store, query, k=4):
        """Retrieve relevant context for the query."""
        docs = vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context
    
    def summarize_text(self, text, doc_type="tech"):
        """Summarize the text using RAG approach."""
        # Create vector store from the text
        vector_store = self.create_vector_store(text)
        
        
        if doc_type == "tech":
            query = "Summarize this technical document highlighting key technical points and findings"
        elif doc_type == "news":
            query = "Summarize this news article capturing the main events, people involved, and key facts"
        elif doc_type == "blog":
            query = "Summarize this blog post highlighting the main ideas, arguments, and conclusions"
        else:
            query = "Provide a comprehensive summary of this document"
        
        # Get relevant context
        context = self.get_relevant_context(vector_store, query)
        
        #  prompt template for summarization
        summarize_template = """
        You are an expert text summarizer. You need to create a comprehensive summary of the following text.
        
        Document Type: {doc_type}
        
        Text:
        {context}
        
        Provide a well-structured summary that captures the key points, main ideas, and important details.
        Make sure the summary is coherent, concise, and complete.
        """
        
        summarize_prompt = PromptTemplate(
            input_variables=["context", "doc_type"],
            template=summarize_template
        )
        
        # Create and run chain
        summarize_chain = LLMChain(llm=self.llm, prompt=summarize_prompt)
        summary = summarize_chain.run(context=context, doc_type=doc_type)
        
        return summary
    
    def reformat_text(self, text):
        """Reformat the text to improve readability and structure."""
        reformat_template = """
        You are an expert editor. Your task is to reformat the following text to improve its readability, 
        structure, and organization without changing the core content or meaning.
        
        Text:
        {text}
        
        Please reformat the text with:
        - Clear paragraph breaks
        - Appropriate headings and subheadings where necessary
        - Bullet points for lists if applicable
        - Consistent formatting throughout
        
        Return the reformatted text.
        """
        
        reformat_prompt = PromptTemplate(
            input_variables=["text"],
            template=reformat_template
        )
        
        reformat_chain = LLMChain(llm=self.llm, prompt=reformat_prompt)
        reformatted_text = reformat_chain.run(text=text)
        
        return reformatted_text
    
    def grammar_check(self, text):
        """Check and correct grammar, spelling, and style issues."""
        grammar_template = """
        You are an expert proofreader and grammar checker. Your task is to correct any grammar, 
        spelling, punctuation, or style issues in the following text without changing the meaning.
        
        Text:
        {text}
        
        Please provide the corrected version of the text, highlighting any significant changes you made.
        """
        
        grammar_prompt = PromptTemplate(
            input_variables=["text"],
            template=grammar_template
        )
        
        grammar_chain = LLMChain(llm=self.llm, prompt=grammar_prompt)
        corrected_text = grammar_chain.run(text=text)
        
        return corrected_text
    
    def process_document(self, text, doc_type, task):
        """Process document based on the specified task."""
        if task == "summarize":
            return self.summarize_text(text, doc_type)
        elif task == "reformat":
            return self.reformat_text(text)
        elif task == "grammar":
            return self.grammar_check(text)
        elif task == "all":
            # Perform all tasks in sequence
            summary = self.summarize_text(text, doc_type)
            reformatted = self.reformat_text(summary)
            final = self.grammar_check(reformatted)
            return final
        else:
            return "Invalid task specified"