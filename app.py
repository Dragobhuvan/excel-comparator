from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            try:
                df = pd.read_excel(file, sheet_name=None)
                sheet1 = df[list(df.keys())[0]]
                sheet2 = df[list(df.keys())[1]]
                differences = []
                for index, row in sheet1.iterrows():
                    for col in sheet1.columns:
                        value1 = row[col]
                        value2 = sheet2.at[index, col]
                        if value1 != value2:
                            diff = {
                                'row': index + 1,
                                'column': col,
                                'sheet1_value': value1,
                                'sheet2_value': value2
                            }
                            differences.append(diff)
                return render_template('result.html', differences=differences)
            except Exception as e:
                error = "An error occurred while processing the Excel file: " + str(e)
                return render_template('index.html', error=error)
    return render_template('index.html')
if __name__ == '__main__':
  app.run()
