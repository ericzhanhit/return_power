# This is a collection of functions that are used in the main program.

import pandas as pd
import numpy as np
import datetime
#from tqdm import tqdm
import statsmodels.api as sm
#import statsmodels.formula.api as smf
#from math import floor
from scipy.stats import percentileofscore


def get_regression_data(data, start_date='2005-07-15', end_date='2023-03-28'):
    date_range = pd.date_range(start_date, end_date)
    variable_list = ['original_id','avg_q1_new','issue_return','ln_degree_roll_f1','past_performance_avg', 'past_performance_sd', 'ipo','ln_brokerage_analyst_num_f1','star_analyst', 'advanced_index_old', 'ln_analyst_coverage', 'rm_rf_f1','smb_f1', 'hml_f1', 'rmw_f1', 'cma_f1','ind_2','ind_3','ind_4','ind_5','ind_6']
    data_select = data[data['date'].isin(date_range)][variable_list].dropna()
    x_train_select = data_select.values[:,3:]
    #original_id_train = data_select.values[:,0].astype(int)
    train_label_select = data_select.values[:,1]
    #true_label_select = data_select.values[:,2]
    return train_label_select, x_train_select

def get_regression_predict(train_label_select, x_train_select, report_need_test,sample_size):
    variable_list = ['ln_degree_roll_f1','past_performance_avg', 'past_performance_sd', 'ipo','ln_brokerage_analyst_num_f1','star_analyst', 'advanced_index_old', 'ln_analyst_coverage', 'rm_rf_f1','smb_f1', 'hml_f1', 'rmw_f1', 'cma_f1','ind_2','ind_3','ind_4','ind_5','ind_6']
    x1_train = sm.add_constant(x_train_select)
    est = sm.OLS(train_label_select, x1_train).fit()
    
    x_test = report_need_test[variable_list].values
    x1_test = sm.add_constant(x_test, has_constant='add')
    y_test_pred_ols = est.predict(x1_test)
    report_need_test['y_pred'] = y_test_pred_ols
    report_need_test = report_need_test.sort_values(by=['y_pred'], ascending = False)
    report_need_test.reset_index(drop=True, inplace=True)
    report_need_test_select = report_need_test.loc[0:(sample_size-1),['date','股票','机构','y_pred']]
    return report_need_test_select

def clean_overlap_report(raw_report, processed_report):
    duplicate_index = np.nan
    for index,row in processed_report.iterrows():
        stk = row['stk1']
        title = row['标题']
        ins = row['机构']
        authors = row['作者']
        for index1,row1 in raw_report.iterrows():
            stk1 = row1['stk1']
            title1 = row1['标题']
            ins1 = row1['机构']
            authors1 = row1['作者']
            if stk == stk1 and title == title1 and ins == ins1 and authors == authors1:
                duplicate_index = index1
                break
        break
    if np.isnan(duplicate_index):
        clean_report = raw_report
    else:
        clean_report = raw_report.loc[0:duplicate_index-1,:]
    return clean_report

def check_broker(ins, ym, broker_status_dataset):
    broker_status_dataset_select = broker_status_dataset[broker_status_dataset['update_month']==ym]
    broker_status_dataset_select = broker_status_dataset_select[broker_status_dataset_select['机构']==ins]
    if broker_status_dataset_select.shape[0] > 0:
        broker_status = broker_status_dataset_select['ln_degree_roll_f1'].values[0]
    else:
        broker_status = None
    return broker_status

def check_broker_size(ins_code, broker_size_dataset):
    broker_data = broker_size_dataset[broker_size_dataset['ins_code']==ins_code]
    if broker_data.shape[0] > 0:
        broker_size = broker_data['analyst_num'].values[0]
        ln_broker_size = np.log(1+broker_size)
    else:
        ln_broker_size = None
    return ln_broker_size

def cal_advanced_index(price_dataset, stock_list, compute_date, update_date):
    advanced_index_df = pd.DataFrame(columns=['date','stk1','positive_num','threeday_return','threeday_return_power','advanced_index'])
    date_trading = sorted(price_dataset['date'].unique())
    compute_date = np.datetime64(compute_date)
    date_range = date_trading[date_trading.index(compute_date)-2:date_trading.index(compute_date)+1]
    date_range = pd.to_datetime(date_range)
    price_data_select = price_dataset[(price_dataset['stk1'].isin(stock_list))&(price_dataset['date'].isin(date_range))]
    return_matrix = np.full((len(stock_list), len(date_range)), np.nan)
    for index, row in price_data_select.iterrows():
        stock = row['stk1']
        date1 = row['date']
        ri = row['ChangeRatio']
        stock_index= np.where(stock_list==stock)[0][0]
        date_index = np.where(date_range==date1)[0][0]
        return_matrix[stock_index, date_index] = ri
    
    # 判断条件1
    positive_num = np.sum(return_matrix>0,axis=1)
    condition1 = positive_num==3
    
    # 判断条件2
    return_matrix_plus1 = return_matrix+1
    threeday_return = np.prod(return_matrix_plus1,axis=1)-1
    condition2 = threeday_return>=0.1
    
    # 判断条件3
    threeday_return_power = np.array([percentileofscore(threeday_return[~np.isnan(threeday_return)],i)/100 for i in threeday_return])
    condition3 = threeday_return_power>=0.8
    
    advanced_index = (condition1|condition2|condition3).astype(int)
    advanced_index_df['date'] = np.repeat(np.datetime64(update_date),len(stock_list))
    advanced_index_df['stk1'] = stock_list
    advanced_index_df['positive_num'] = positive_num
    advanced_index_df['threeday_return'] = threeday_return
    advanced_index_df['threeday_return_power'] = threeday_return_power
    advanced_index_df['advanced_index'] = advanced_index
    return advanced_index_df

def check_star_analyst(authors, star_analyst_dataset):
    star_analyst_set = star_analyst_dataset['2022年'].values.tolist()
    author_list = authors.split(',')
    for i in author_list:
        if i in star_analyst_set:
            star_analyst = 1
        else:
            star_analyst = 0
    return star_analyst

def check_advanced_index(stk, date, advanced_index_dataset):
    advanced_index_df = advanced_index_dataset[(advanced_index_dataset['stk1']==stk)&(advanced_index_dataset['date']==date)]
    if advanced_index_df.shape[0]>0:
        advanced_index = advanced_index_df['advanced_index'].values[0]
    else:
        advanced_index = 0
    return advanced_index

def check_analyst_coverage(stk, date, report_data_combined):
    date_range = pd.date_range(date-datetime.timedelta(180), date-datetime.timedelta(1))
    coverage_data = report_data_combined[(report_data_combined['stk1']==stk)&(report_data_combined['date'].isin(date_range))]
    ln_analyst_coverage = np.log(1+coverage_data.shape[0])
    return ln_analyst_coverage

# 过去滚动表现
def cal_past_performance(row, report_data_combined):
    ins_code = row['ins_code']
    date = row['date']
    if ins_code == None:
        past_performance_avg = None
        past_performance_sd = None
    else:
        date_range = pd.date_range(date-datetime.timedelta(180), date-datetime.timedelta(1))
        select_data1 = report_data_combined[report_data_combined['ins_code'].isin([ins_code])]
        select_data2 = select_data1[select_data1['date'].isin(date_range)]
        past_performance_avg = select_data2['avg_quantile_current'].mean()
        past_performance_sd = select_data2['avg_quantile_current'].std()
    return past_performance_avg, past_performance_sd

def extract_stk(stk):
    split_stk = stk.split('(')
    if len(split_stk)==2:
        stk1 = split_stk[1][0:6]
    else:
        stk1 = None
    return stk1

def check_five_factor(raw_report, five_factor_dataset):
    five_factor_select = five_factor_dataset[['ym_use','rm_rf','smb','hml','rmw','cma']]
    five_factor_select.rename(columns={'ym_use':'ym'}, inplace=True)
    raw_report = pd.merge(raw_report, five_factor_select, how='left', on='ym')
    return raw_report

def process_industry(industry_dataset):
    industry_dataset['stk1'] = industry_dataset['stk'].map(lambda x: str(x).rjust(6,'0'))
    industry_select = industry_dataset[['stk1','ind_code_A']]
    industry_select['ind_2'] = industry_select['ind_code_A'].map(lambda x: 1 if x == 2 else 0)
    industry_select['ind_3'] = industry_select['ind_code_A'].map(lambda x: 1 if x == 3 else 0)
    industry_select['ind_4'] = industry_select['ind_code_A'].map(lambda x: 1 if x == 4 else 0)
    industry_select['ind_5'] = industry_select['ind_code_A'].map(lambda x: 1 if x == 5 else 0)
    industry_select['ind_6'] = industry_select['ind_code_A'].map(lambda x: 1 if x == 6 else 0)
    industry_select.drop(columns=['ind_code_A'], inplace=True)
    return industry_select

def process_price(raw_price_dataset, price_dataset):
    raw_price_dataset = raw_price_dataset.loc[2:,]
    raw_price_dataset.rename(columns={'Stkcd':'stk1','Trddt':'date'}, inplace=True)
    raw_price_dataset['date'] = pd.to_datetime(raw_price_dataset['date'])
    raw_price_dataset['stk1'] = raw_price_dataset['stk1'].map(lambda x: str(x).rjust(6,'0'))
    raw_last_date = sorted(raw_price_dataset['date'].unique())
    
    price_dataset['date'] = pd.to_datetime(price_dataset['date'])
    price_dataset['stk1'] = price_dataset['stk1'].map(lambda x: str(x).rjust(6,'0'))
    last_date = sorted(price_dataset['date'].unique())
    
    if raw_last_date[-1] == last_date[-1]:
        price_dataset_new = price_dataset
        print('该数据集已经是最新的')
    else:
        price_dataset_new = pd.concat([price_dataset, raw_price_dataset], axis=0, ignore_index=True)
        print('该数据集正在更新中')
    return price_dataset_new

def find_return(stk, date, price_dataset):
    date_set = np.array(sorted(price_dataset['date'].unique()))
    if date in date_set:
        date_index = np.where(date_set==date)[0][0]
    else:
        date_index = np.where(date_set==date_set[date_set>date][0])[0][0]
    date_index_next = date_index+1
    issue_return_data = price_dataset[(price_dataset['stk1']==stk)&(price_dataset['date']==date_set[date_index_next])]['ChangeRatio'].values
    if len(issue_return_data)==0:
        issue_return = np.nan
    else:
        issue_return = issue_return_data[0]
    return issue_return

def cal_quantile(row, price_dataset, stock_list):
    stk = row['stk1']
    date = row['date']
    issue_return = row['issue_return']
    date_set = np.array(sorted(price_dataset['date'].unique()))
    if date in date_set:
        date_index = np.where(date_set==date)[0][0]
    else:
        date_index = np.where(date_set==date_set[date_set>date][0])[0][0]
    date_index_next = date_index+1
    price_data = price_dataset[price_dataset['stk1'].isin(stock_list)]
    current_return_data = price_data[(price_data['stk1']==stk)&(price_data['date']==date_set[date_index])]['ChangeRatio'].values
    if len(current_return_data)==0:
        current_return = np.nan
    else:
        current_return = current_return_data[0]
    return_current_set = price_data[price_data['date']==date_set[date_index]]['ChangeRatio'].values
    return_next_set = price_data[price_data['date']==date_set[date_index_next]]['ChangeRatio'].values
    return_current_set = return_current_set.astype(float)
    return_next_set = return_next_set.astype(float)
    quantile_current = percentileofscore(return_current_set[~np.isnan(return_current_set)], current_return)/100
    quantile_next = percentileofscore(return_next_set[~np.isnan(return_next_set)], issue_return)/100
    if quantile_next == 1:
        quantile_next = 0.999
        avg_q1_new = np.log(quantile_next/(1-quantile_next))
    else:
        avg_q1_new =  np.log(quantile_next/(1-quantile_next))
    return avg_q1_new, quantile_current

# combined all dataset
def concat_df(report_all_samples, report_latest2year, report_latest1year, report_latesthalfyear):
    concat_data = pd.DataFrame(columns=['全样本回归','近两年样本','近一年样本','近半年样本'])
    #concat_data = pd.DataFrame(columns=['全样本回归','近两年样本','近一年样本','近半年样本'])
    stock_all_samples = report_all_samples['股票'].values.tolist()
    stock_latest2year = report_latest2year['股票'].values.tolist()
    stock_latest1year = report_latest1year['股票'].values.tolist()
    stock_latesthalfyear = report_latesthalfyear['股票'].values.tolist()
    stock_intersect = []
    #求全样本和前两年的交集
    for i in range(1,len(stock_all_samples)):
        intersect = list(set(stock_all_samples[0:i]).intersection(set(stock_latest2year[0:i])))
        stock_intersect.extend(intersect)
    stock_intersect_set = list(set(stock_intersect))
    stock_intersect_set.sort(key = stock_intersect.index)
    stock_intersect_df = pd.DataFrame(stock_intersect_set, columns=['前两模型交集'])
    concat_data['全样本回归'] = stock_all_samples
    concat_data['近两年样本'] = stock_latest2year
    concat_data['近一年样本'] = stock_latest1year
    concat_data['近半年样本'] = stock_latesthalfyear
    concat_data = pd.concat([concat_data, stock_intersect_df], ignore_index=True, axis=1)
    concat_data.columns = ['全样本回归','近两年样本','近一年样本','近半年样本','前两模型交集']
    return concat_data

def gen_network(data, compute_month, all_nodes):
    data_ym = data[data['ym']==compute_month]
    print(f'当月研报数：{data_ym.shape[0]}')
    #data_year.drop_duplicates(subset=['ins_code','stk1','日期'], inplace=True, ignore_index=True)
    net_matrix = np.zeros((len(all_nodes), len(all_nodes)))
    for index, row in data_ym.iterrows():
        node = row['ins_code']
        date = row['date']
        stk = row['stk1']
        ins_index = all_nodes.index(node)
        date_range = pd.date_range(date, date+datetime.timedelta(6))
        select_data = data_ym[data_ym['date'].isin(date_range)]
        select_data1 = select_data[select_data['stk1']==stk]
        select_data2 = select_data1[select_data1['ins_code']!=node]
        other_ins_set = sorted(select_data2['ins_code'].unique())
        for other_ins in other_ins_set:
            other_ins_index = all_nodes.index(other_ins)
            select_data3 = select_data2[select_data2['ins_code']==other_ins]
            bi_num = select_data3[select_data3['date']==date].shape[0]
            single_num = select_data3[select_data3['date']>date].shape[0]
            if bi_num>0:
                net_matrix[ins_index, other_ins_index] += 1
                net_matrix[other_ins_index, ins_index] += 1
            else:
                pass
            if single_num>0:
                net_matrix[other_ins_index, ins_index] += 1
            else:
                pass
    return net_matrix

def degree_centrality(net_matrix, all_nodes):
    degree_dict = {}
    for i in all_nodes:
        degree_dict[i] = net_matrix[:,all_nodes.index(i)].sum()
    return degree_dict

def add_to_df(df, all_nodes, compute_month, degree):
    data = pd.DataFrame(columns=['ins_code','compute_month','degree_roll_f1', 'ln_degree_roll_f1'])
    data['ins_code'] = all_nodes
    data['compute_month'] = compute_month
    data['degree_roll_f1'] = degree
    data['ln_degree_roll_f1'] = np.log(data['degree_roll_f1']+1)
    added_df = pd.concat([df, data], axis=0)
    return added_df

