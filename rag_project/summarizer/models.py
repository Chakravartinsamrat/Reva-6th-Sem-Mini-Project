from django.db import models

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('tech', 'Technical Document'),
        ('news', 'Newspaper/Article'),
        ('blog', 'Blog Post'),
        ('other', 'Other'),
    ]
    
    TASKS = [
        ('summarize', 'Summarize'),
        ('reformat', 'Reformat'),
        ('grammar', 'Grammar Check'),
        ('all', 'All Tasks'),
    ]
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    text_content = models.TextField(blank=True, null=True)
    task = models.CharField(max_length=10, choices=TASKS, default='summarize')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title