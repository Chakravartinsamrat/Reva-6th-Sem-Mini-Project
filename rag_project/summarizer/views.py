from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Document
from .document_processor import DocumentProcessor
from .rag import RAGSystem
import os

def index(request):
    """View for the main page with the upload form."""
    if request.method == 'POST':
        title = request.POST.get('title')
        document_type = request.POST.get('document_type')
        task = request.POST.get('task')
        file = request.FILES.get('document_file')
        
        if file:
            # Save document
            document = Document.objects.create(
                title=title,
                document_type=document_type,
                file=file,
                task=task
            )
            
            # Process the document
            file_path = document.file.path
            
            # Extract text from the file
            text_content = DocumentProcessor.process_file(file_path, document_type)
            document.text_content = text_content
            document.save()
            
            return redirect('process_document', document_id=document.id)
        else:
            messages.error(request, 'Please upload a file')
    
    return render(request, 'summarizer/index.html')

def process_document(request, document_id):
    """Process the uploaded document and display the results."""
    document = get_object_or_404(Document, id=document_id)
    
    if not document.processed_content:
        try:
            # Initialize RAG system
            rag_system = RAGSystem()
            
            # Process document
            processed_content = rag_system.process_document(
                document.text_content,
                document.document_type,
                document.task
            )
            
            # Save processed content
            document.processed_content = processed_content
            document.save()
            
        except Exception as e:
            messages.error(request, f'Error processing document: {str(e)}')
            return redirect('index')
    
    context = {
        'document': document,
        'original_text': document.text_content,
        'processed_text': document.processed_content,
        'task': document.get_task_display()
    }
    
    return render(request, 'summarizer/result.html', context)