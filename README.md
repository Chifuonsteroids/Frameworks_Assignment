# 📊 CORD-19 Data Explorer  

This project provides an **interactive Streamlit application** for exploring the [CORD-19](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) dataset metadata (`metadata.csv`). It enables users to analyze publication trends, identify top journals, visualize word frequency in titles, and filter data by year and journal.  

---

## 🚀 Features  

- 📅 **Filter by Year Range** – Select which years of publications to explore  
- 📊 **Publications by Year** – View trends of research publications over time  
- 📚 **Top Journals** – See the top journals publishing COVID-19 related research  
- ☁️ **Word Cloud** – Generate a word cloud from research paper titles  
- 📦 **Source Distribution** – Explore distribution by data source (if available)  
- 🔎 **Journal Drill-Down** – Select a specific journal to view its publication trend  
- 📥 **Export Filtered Data** – Download filtered results as CSV  

---

## 🛠 Installation  

Clone the repository:  

```bash
git clone https://github.com/Chifuonsteroids/Frameworks_Assignment.git
cd Frameworks_Assignment


▶️ Usage

Make sure you have metadata.csv inside the project directory.

You can download it from the official CORD-19 dataset
.

Run the Streamlit app:

streamlit run cord19_app.py


Open the provided local URL in your browser (e.g., http://localhost:8501).

📂 Project Structure
Frameworks_Assignment/
│── cord19_app.py       # Main Streamlit application
│── metadata.csv        # CORD-19 metadata file (not included in repo, must be downloaded)
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
│── notebooks/          # (Optional) Jupyter notebooks for exploration
│── outputs/            # Saved visualizations (PNG files)

📖 Example Workflow

Select year range (e.g., 2020–2021) from the sidebar

Preview the filtered dataset in a table

Explore:

📊 Publications per year (bar chart)

📚 Top publishing journals (horizontal bar chart)

☁️ Word cloud of paper titles

📦 Source distribution (if available)

🔎 Select a journal from dropdown to view its publication trend

Click Download Filtered Data as CSV to save results

✨ Expected Outcomes

By running this app, you’ll be able to:

Understand publication patterns across years

Identify major journals in COVID-19 research

Explore key themes through word frequency in paper titles

Export subsets of the dataset for further analysis

📝 Author

Developed by Chifuonsteroids for the Frameworks Assignment.
