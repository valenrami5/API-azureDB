import pandas as pd
import app.infrastructure.azure_db_connector as azure_db_connector
from app.infrastructure.dictionary_cols import DictCols

class EtlPivotedTable():
    def __init__(self) -> None:
        self.sql_manager = azure_db_connector.SqlManager()
        self.hired_employees = self.sql_manager.read_table(table_name='hired_employees')
        self.jobs = self.sql_manager.read_table(table_name='jobs')
        self.departments = self.sql_manager.read_table(table_name='departments')
    
    def filter_2021_year(self):
        rename_cols_df = self.hired_employees.rename(columns={'datetime': 'hired_date'})
        df_filtered_2021 = rename_cols_df[rename_cols_df['hired_date'].dt.year == 2021]
        return df_filtered_2021
    
    def quarter_col(self, df):
        df['Quarter'] = df['hired_date'].dt.quarter
        return df
    
    def fill_na_otros(self, df):
        df['department'] = df['department'].fillna('Otros')
        df['job'] = df['job'].fillna('Otros')
        return df
    
    def grouped_pivot(self,df):
        df = df.groupby(['department_id', 'job_id', 'Quarter']).size().reset_index(name='count')
        df = df.pivot_table(index=['department_id', 'job_id'], columns='Quarter', values='count', fill_value=0).reset_index()
        df.columns.name = None
        quarter_dict_column = DictCols().quarter_dict_cols()
        df = df.rename(columns=quarter_dict_column)
        return df
    
    def joined_df(self, df):
        df = df.merge(self.departments ,how='left', left_on='department_id', right_on='id')
        df = df.merge(self.jobs,how='left', left_on= 'job_id', right_on= 'id')
        return df
    
    def drop_sort_columns(self, df):
        df = df.drop(['department_id', 'job_id', 'id_x', 'id_y'], axis = 1)
        df = df[['department', 'job', 'Q1', 'Q2', 'Q3', 'Q4']]
        return df

    def sort_cols(self, df):
        df = df.sort_values(by = ['department', 'job'])
        return df
        
    def transform_hired_employees(self):
        df = self.filter_2021_year()
        df = self.quarter_col(df)
        df = self.grouped_pivot(df)
        df = self.joined_df(df)
        df = self.drop_sort_columns(df)
        df = self.fill_na_otros(df)
        df = self.sort_cols(df)
        return df
    
class MeanEmployeesHired(EtlPivotedTable):

    def mean_employees_dept(self, df):
        df_grouped = df.groupby('department_id')['name'].count().reset_index()
        df = df_grouped.mean(axis = 1)
        mean_value = df.mean()       
        return df_grouped, mean_value
    
    def filter_employees_by_mean(self, df, mean_value):       
        df = df[df['name'] >= mean_value]
        return df
    
    def merge_dept(self, df):
        df = df.merge(self.departments ,how='left', left_on='department_id', right_on='id')
        return df
    
    def df_order(self, df):
        df = df.drop('department_id', axis = 1)
        df = df[['id', 'department', 'name']]
        df = df.rename(columns={'name':'hired'})
        df = df.sort_values(by='hired', ascending=False)
        return df
        
    def transform_mean_employees(self):
        df = self.filter_2021_year()
        df, mean_value = self.mean_employees_dept(df)
        df = self.filter_employees_by_mean(df, mean_value)
        df = self.merge_dept(df)
        df = self.df_order(df)
        return df 



