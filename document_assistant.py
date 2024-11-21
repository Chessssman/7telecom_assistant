import os
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import stop_words


class DocumentAssistant:
    def __init__(self, documents_dir, model_name='all-MiniLM-L6-v2', threshold=0.5, language='ru'):
        # Initialize neural network model for embedding
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold
        self.language = language

        # Load stop words for better query processing
        try:
            self.stop_words = set(stop_words.get_stop_words(language))
        except:
            self.stop_words = set()

        # Document processing
        self.documents = []
        self.embeddings = []
        self.load_documents(documents_dir)

    def preprocess_text(self, text):
        """
        Preprocess text by removing stop words and normalizing
        """
        # Remove stop words
        words = text.lower().split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)

    def load_documents(self, directory):
        """
        Load and process documents from the specified directory
        Supports PDF and DOCX files
        """
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            # PDF processing
            if filename.endswith('.pdf'):
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ' '.join([page.extract_text() for page in reader.pages])
                    processed_text = self.preprocess_text(text)
                    self.documents.append(processed_text)

            # DOCX processing
            elif filename.endswith('.docx'):
                doc = docx.Document(filepath)
                text = ' '.join([para.text for para in doc.paragraphs])
                processed_text = self.preprocess_text(text)
                self.documents.append(processed_text)

        # Create embeddings for all documents
        self.embeddings = self.model.encode(self.documents)

    def find_best_answer(self, query):
        """
        Find the best matching document for a given query
        """
        # Preprocess query
        processed_query = self.preprocess_text(query)

        query_embedding = self.model.encode([processed_query])[0]

        # Calculate cosine similarities
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]

        # Find best match above threshold
        best_match_index = similarities.argmax()
        if similarities[best_match_index] >= self.threshold:
            return self.documents[best_match_index]

        return ''