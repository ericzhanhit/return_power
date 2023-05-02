
import pandas as pd
from functions import gen_network, degree_centrality, add_to_df
# update month
date = '2023-03-31'
update_month = '2023-04'
compute_month = '2023-03'
# 因子库文件路径
library_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/library/'
# 更新数据文件路径
downloads_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/downloads/'
# 计算好的数据文件路径
processed_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/processed/'

# 每月更新broker_status之前，需要将前一个月的所有研报都更新到report_data_combined中
# 更新到report_data_combined之后，report_data_combined可以不用导出，因为因变量尚无法更新
processed_report = pd.read_excel(processed_path+'processed_report_'+date+'.xlsx')
report_data_combined = pd.read_excel(library_path+'report_data_combined.xlsx')
processed_report = processed_report[['old_id', 'date', 'stk1', 'ins_number', 'ln_degree_roll_f1', 'past_performance_avg','past_performance_sd', 'ipo', 'ln_brokerage_analyst_num_f1','star_analyst', 'advanced_index_old', 'ln_analyst_coverage', 'rm_rf_f1','smb_f1', 'hml_f1', 'rmw_f1', 'cma_f1', 'ind_2', 'ind_3', 'ind_4','ind_5', 'ind_6', 'ins_code']]
report_data_combined = pd.concat([report_data_combined, processed_report], axis=0, ignore_index=True)

institutions_dataset = pd.read_excel(library_path+'Institution.xlsx')
all_nodes = institutions_dataset['ins_code'].tolist()
report_data_combined['ym'] = report_data_combined['date'].dt.strftime('%Y-%m')

broker_status_old = pd.read_excel(library_path+'broker_status.xlsx')
degree_df = pd.DataFrame(columns=['ins_code','compute_month','degree_roll_f1', 'ln_degree_roll_f1'])
net_matrix = gen_network(report_data_combined, compute_month, all_nodes)
degree = degree_centrality(net_matrix, all_nodes)
degree_df = add_to_df(degree_df, all_nodes, compute_month, list(degree.values()))

broker_status = pd.merge(degree_df, institutions_dataset[['机构','ins_code','ins_number']], how='left', on='ins_code')
broker_status['update_month'] = update_month
broker_status_update = pd.concat([broker_status_old, broker_status], axis=0, ignore_index=True)
broker_status_update.to_excel(library_path+'broker_status.xlsx',index=0)

