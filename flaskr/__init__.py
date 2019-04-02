import os
from flask import Flask, request, render_template
from werkzeug import secure_filename
import csv
import json
import pandas as pd

def getUniqueValuesHeader(folder_name, num, column_name):

    folder_path = folder_name

    raw_file_list = os.listdir(folder_path)
    file_list = []
    for x in raw_file_list:
        new_file_path = folder_name+"/"+x
        print(new_file_path)
        file_list.append(new_file_path)

    repeat_values = []
    numValuesFound = False
    file_index = 0

    final_df = pd.DataFrame()

    while (numValuesFound != True) and (file_index < len(file_list)):
        csv_df = pd.read_csv(file_list[file_index], error_bad_lines=False)

        filter_df = csv_df[~csv_df[column_name].isin(repeat_values)]
        filter_df = filter_df.groupby(column_name).count().reset_index()
        single_col_df = filter_df[[column_name]]

        found_values_list = single_col_df[column_name].tolist()
        repeat_values = repeat_values + found_values_list

        final_df = final_df.append(single_col_df)

        print(str(file_index)+": "+str(file_list[file_index]))
        file_index += 1
        if final_df.shape[0] >= num:
            numValuesFound = True

    final_df = final_df.head(num)
    final_df.to_csv('values-header.csv', index=False, header=False)
    if final_df.shape[0] >= num:
        return("Operation Successful, "+str(final_df.shape[0])+" values found.")
    else:
        return("Operation Unsuccessful, only "+str(final_df.shape[0])+" values found.")

def getUniqueValuesNoHeader(folder_name, num, column_num):

    folder_path = folder_name

    raw_file_list = os.listdir(folder_path)
    file_list = []
    for x in raw_file_list:
        new_file_path = folder_name+"/"+x
        print(new_file_path)
        file_list.append(new_file_path)

    repeat_values = []
    numValuesFound = False
    file_index = 0

    final_df = pd.DataFrame()

    while (numValuesFound != True) and (file_index < len(file_list)):
        csv_df = pd.read_csv(file_list[file_index], error_bad_lines=False, header=None)

        filter_df = csv_df[~csv_df[column_num].isin(repeat_values)]
        filter_df = filter_df.groupby(column_num).count().reset_index()
        single_col_df = filter_df[[column_num]]

        found_values_list = single_col_df[column_num].tolist()
        repeat_values = repeat_values + found_values_list

        final_df = final_df.append(single_col_df)

        print(str(file_index)+": "+str(file_list[file_index]))
        file_index += 1
        if final_df.shape[0] >= num:
            numValuesFound = True

    final_df = final_df.head(num)
    final_df.to_csv('values-no-header.csv', index=False, header=False)
    if final_df.shape[0] >= num:
        return("Operation Successful, "+str(final_df.shape[0])+" values found.")
    else:
        return("Operation Unsuccessful, only "+str(final_df.shape[0])+" values found.")

def calculateNumbers(num1, num2):
    return num1 + num2

def getAbsolutePath():
    path = os.getcwd()
    return path


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/')
    def index():
        return render_template('hello.html')

    @app.route('/ag_header', methods=['GET', 'POST'])
    def test():
        path = request.form['folder_path']
        col_name = request.form['column_name']
        amount = request.form['ag_amount']

        return getUniqueValuesHeader(path, int(amount), col_name)
    
    @app.route('/ag_noheader', methods=['GET', 'POST'])
    def test2():
        print("happy!")
        path = request.form['folder_path']
        col_num = request.form['column_name']
        amount = request.form['ag_amount']

        return getUniqueValuesNoHeader(path, int(amount), int(col_num))

    # @app.route('/upload')
    # def upload_file():
    #     return render_template('upload.html')
        
    # @app.route('/uploader', methods = ['GET', 'POST'])
    # def upload_file2():
    #     if request.method == 'POST':
    #         f = request.files['file']
    #         filename = secure_filename(f.filename)
    #         f.save(os.path.join(getAbsolutePath()+"/flaskr/saved_files", filename))

    #         return render_template('upload_success.html')


    return app

