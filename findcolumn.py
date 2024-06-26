from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV file with the full path
csv_file = '/Users/anishsparida/Documents/Grant Search/govgrants.csv'
df = pd.read_csv(csv_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    column_name = 'title'  # column name 

    #  case-insensitive search 
    if column_name in df.columns:
        results = df[df[column_name].str.contains(keyword, case=False, na=False)]

        # Check if results are empty
        if results.empty:
            message = f"No results found for '{keyword}' in column '{column_name}'."
            return render_template('no_results.html', message=message)
        else:
            # Pass the results DataFrame to results.html for rendering
            return render_template('results.html', tables=[results.to_html(classes='data', header="true", index=False)])
    else:
        # Handle the case where the column does not exist
        error_message = f"Error: Column '{column_name}' not found in the CSV file."
        return render_template('error.html', error=error_message)

@app.route('/details/<int:row_id>')
def details(row_id):
    if row_id < len(df):
        row_data = df.iloc[row_id].to_dict()
        return render_template('details.html', row=row_data)
    else:
        return "Error: Row ID out of range."

if __name__ == '__main__':
    app.run(debug=True)
