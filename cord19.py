import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
import streamlit as st
from datetime import datetime  # Fixed import statement

class CORD19Analyzer:
    def __init__(self, file_path='metadata.csv'):  # Fixed file path
        self.df = None
        # Use raw string or forward slashes for Windows paths
        self.file_path = file_path
        self.load_data()
    
    def load_data(self):
        """Load and initial data processing"""
        print("Loading data...")
        try:
            # Read in chunks to handle memory issues
            chunk_size = 10000
            chunks = []
            for chunk in pd.read_csv(self.file_path, low_memory=False, chunksize=chunk_size):
                chunks.append(chunk)
            self.df = pd.concat(chunks, ignore_index=True)
            print(f"Initial data shape: {self.df.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create a minimal dataframe for testing if file not found
            self.df = pd.DataFrame({
                'title': ['Test Paper 1', 'Test Paper 2'],
                'abstract': ['Test abstract 1', 'Test abstract 2'],
                'publish_time': ['2020-01-01', '2021-01-01'],
                'journal': ['Journal A', 'Journal B']
            })
    
    def clean_data(self):
        """Clean and prepare the data"""
        print("Cleaning data...")
        df_clean = self.df.copy()
        
        # Remove rows without titles
        df_clean = df_clean.dropna(subset=['title'])
        
        # Handle missing values
        if 'abstract' in df_clean.columns:
            df_clean['abstract'] = df_clean['abstract'].fillna('')
        if 'journal' in df_clean.columns:
            df_clean['journal'] = df_clean['journal'].fillna('Unknown')
        
        # Convert dates
        try:
            df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
            df_clean['year'] = df_clean['publish_time'].dt.year
        except:
            df_clean['publish_time'] = pd.NaT
            df_clean['year'] = None
        
        # Create new features
        df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))
        df_clean['title_word_count'] = df_clean['title'].apply(lambda x: len(str(x).split()))
        
        self.df_clean = df_clean
        print(f"Cleaned data shape: {self.df_clean.shape}")
    
    def analyze_data(self):
        """Perform data analysis"""
        print("Analyzing data...")
        
        # Year distribution
        if 'year' in self.df_clean.columns:
            self.year_counts = self.df_clean['year'].value_counts().sort_index()
            self.year_counts = self.year_counts[self.year_counts.index.notna()]
        else:
            self.year_counts = pd.Series()
        
        # Journal distribution
        if 'journal' in self.df_clean.columns:
            self.top_journals = self.df_clean['journal'].value_counts().head(10)
        else:
            self.top_journals = pd.Series()
        
        # Word frequency
        if 'title' in self.df_clean.columns:
            all_titles = ' '.join(self.df_clean['title'].dropna().astype(str))
            cleaned_titles = self.clean_text(all_titles)
            words = cleaned_titles.split()
            word_freq = Counter(words).most_common(50)
            
            # Filter stop words
            stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'as', 'by', 'an', 'at'}
            self.filtered_words = [(word, count) for word, count in word_freq 
                                  if word not in stop_words and len(word) > 2]
        else:
            self.filtered_words = []
    
    def clean_text(self, text):
        """Clean text for analysis"""
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        return text
    
    def create_visualizations(self):
        """Create all visualizations"""
        print("Creating visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        ax1, ax2, ax3, ax4 = axes.flatten()
        
        # Plot 1: Publications by year
        if len(self.year_counts) > 0:
            ax1.bar(self.year_counts.index, self.year_counts.values)
            ax1.set_title('Publications by Year')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Count')
        else:
            ax1.text(0.5, 0.5, 'No year data available', ha='center', va='center')
            ax1.set_title('Publications by Year')
        
        # Plot 2: Top journals
        if len(self.top_journals) > 0:
            top_journals_plot = self.top_journals.head(8)
            ax2.barh(range(len(top_journals_plot)), top_journals_plot.values)
            ax2.set_yticks(range(len(top_journals_plot)))
            ax2.set_yticklabels([j[:30] + '...' if len(j) > 30 else j for j in top_journals_plot.index])
            ax2.set_title('Top Publishing Journals')
            ax2.set_xlabel('Number of Papers')
        else:
            ax2.text(0.5, 0.5, 'No journal data available', ha='center', va='center')
            ax2.set_title('Top Publishing Journals')
        
        # Plot 3: Word cloud
        if 'title' in self.df_clean.columns:
            all_titles = ' '.join(self.df_clean['title'].dropna().astype(str))
            if all_titles.strip():  # Check if not empty
                wordcloud = WordCloud(width=400, height=300, background_color='white').generate(all_titles)
                ax3.imshow(wordcloud, interpolation='bilinear')
                ax3.set_title('Title Word Cloud')
                ax3.axis('off')
            else:
                ax3.text(0.5, 0.5, 'No title data available', ha='center', va='center')
                ax3.set_title('Title Word Cloud')
        else:
            ax3.text(0.5, 0.5, 'No title data available', ha='center', va='center')
            ax3.set_title('Title Word Cloud')
        
        # Plot 4: Top words
        if len(self.filtered_words) > 0:
            words, counts = zip(*self.filtered_words[:10])
            ax4.barh(range(len(words)), counts)
            ax4.set_yticks(range(len(words)))
            ax4.set_yticklabels(words)
            ax4.set_title('Top 10 Words in Titles')
            ax4.set_xlabel('Frequency')
        else:
            ax4.text(0.5, 0.5, 'No word frequency data available', ha='center', va='center')
            ax4.set_title('Top 10 Words in Titles')
        
        plt.tight_layout()
        plt.savefig('cord19_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def run_analysis(self):
        """Run complete analysis"""
        self.clean_data()
        self.analyze_data()
        self.create_visualizations()
        
        print("\n=== ANALYSIS SUMMARY ===")
        print(f"Total papers analyzed: {len(self.df_clean)}")
        if len(self.year_counts) > 0:
            print(f"Time range: {self.year_counts.index.min()} - {self.year_counts.index.max()}")
        if len(self.top_journals) > 0:
            print(f"Top journal: {self.top_journals.index[0]} ({self.top_journals.iloc[0]} papers)")
        if len(self.filtered_words) > 0:
            print(f"Top word: '{self.filtered_words[0][0]}' ({self.filtered_words[0][1]} occurrences)")

# Main execution
if __name__ == "__main__":
    # Use a relative path or check if file exists
    import os
    if os.path.exists('metadata.csv'):
        analyzer = CORD19Analyzer('metadata.csv')
    else:
        print("metadata.csv not found. Using sample data for demonstration.")
        analyzer = CORD19Analyzer()
    
    analyzer.run_analysis()