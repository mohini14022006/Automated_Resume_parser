# Import necessary libraries for building the resume parser API
import pdfplumber 
import spacy 
from flask import Flask, request, jsonify 
import psycopg2 
from psycopg2.extras import RealDictCursor 
import re 

# Load a pre-trained spaCy model for natural language processing tasks
nlp = spacy.load('en_core_web_sm')

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="your_dbname", 
    user="your_username", 
    password="your_password", 
    host="localhost", 
    port="5432"
)
cursor = conn.cursor()

# Create a table to store candidate information if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id SERIAL PRIMARY KEY,
        name TEXT,
        skills TEXT,
        education TEXT
    );
""")
conn.commit()

# Define a function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    # Initialize an empty string to store the extracted text
    text = ""
    
    # Open the PDF file and iterate over its pages
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Extract text from the current page and append it to the text string
            text += page.extract_text() + "\n"
    
    
