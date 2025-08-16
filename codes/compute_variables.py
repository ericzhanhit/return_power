# This is the main program used to recommend the top 20 stocks for each day.
#%%
import pandas as pd
import datetime
from functions import extract_stk, check_broker, cal_past_performance, check_broker_size, check_star_analyst, check_advanced_index, check_analyst_coverage, check_five_factor, process_industry, clean_overlap_report

# 需要更新的数据
# 昨交易日，将当天下载研报包含昨天3点前发布的部分删除
last_trading_date = '2023-04-27'
# 当天交易日
current_trading_date = '2023-04-28'
# 因子库文件路径
library_path = '~/Stock_recommend/library/'
# 更新数据文件路径
downloads_path = '~/Stock_recommend/downloads/'
# 计算好的数据文件路径
processed_path = '~/Stock_recommend/processed/'

# 导入研报数据和所有因子库
#report_data_combined = pd.read_excel(library_path+'report_data_combined.xlsx')
#report_data_combined['date'] = pd.to_datetime(report_data_combined['date'])
#report_data_combined['stk1'] = report_data_combined['stk1'].map(lambda x: str(x).rjust(6,'0'))

broker_status_dataset = pd.read_excel(library_path+'broker_status.xlsx')
broker_size_dataset = pd.read_excel(library_path+'broker_size.xlsx')
star_analyst_dataset = pd.read_excel(library_path+'star_analyst.xlsx')
five_factor_dataset = pd.read_excel(library_path+'five_factors.xlsx')
industry_dataset = pd.read_excel(library_path+'industry.xlsx')
institutions_dataset = pd.read_excel(library_path+'Institution.xlsx')
advanced_index_dataset = pd.read_excel(library_path+'advanced_index.xlsx')
advanced_index_dataset['date'] = pd.to_datetime(advanced_index_dataset['date'])
advanced_index_dataset['stk1'] = advanced_index_dataset['stk1'].map(lambda x: str(x).rjust(6,'0'))
#price_dataset = pd.read_excel(library_path+'price.xlsx')
#price_dataset['date'] = pd.to_datetime(price_dataset['date'])
#price_dataset['stk1'] = price_dataset['stk1'].map(lambda x: str(x).rjust(6,'0'))
#%%
# 正式进行计算当天新获取研报各变量
raw_report = pd.read_excel(downloads_path+'公司研究_研究报告.xls')
raw_report['date_raw'] = pd.to_datetime(raw_report['日期'])
raw_report['date_str'] = raw_report['date_raw'].dt.strftime('%Y-%m-%d')
raw_report = raw_report[~pd.isnull(raw_report['date_str'])]
raw_report['date'] = raw_report['date_str'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
raw_report['year'] = raw_report['date'].dt.year
raw_report['ym'] = raw_report['date'].dt.strftime('%Y-%m')
raw_report['stk1'] = raw_report['股票'].apply(lambda x: extract_stk(x))
raw_report = pd.merge(raw_report, institutions_dataset[['机构','ins_code','ins_number','ipo']], how='left', on='机构')
raw_report = raw_report[~((raw_report['stk1'].isna())|(raw_report['ins_code'].isna()))]

processed_report_preday = pd.read_excel(processed_path+'processed_report_'+last_trading_date+'.xlsx')
processed_report_preday['stk1'] = processed_report_preday['stk1'].map(lambda x: str(x).rjust(6,'0'))
raw_report = clean_overlap_report(raw_report, processed_report_preday)

raw_report['ln_degree_roll_f1'] = raw_report.apply(lambda x:check_broker(x['机构'],x['ym'], broker_status_dataset), axis=1)
raw_report[['past_performance_avg','past_performance_sd']] = raw_report.apply(cal_past_performance, axis=1, result_type='expand', args=(report_data_combined,))
raw_report['ln_brokerage_analyst_num_f1'] = raw_report['ins_code'].apply(lambda x:check_broker_size(x, broker_size_dataset))
raw_report['star_analyst'] = raw_report['作者'].apply(lambda x: check_star_analyst(x, star_analyst_dataset))
raw_report['advanced_index_old'] = raw_report.apply(lambda x: check_advanced_index(x['stk1'],x['date'], advanced_index_dataset), axis=1)
raw_report['ln_analyst_coverage'] = raw_report.apply(lambda x: check_analyst_coverage(x['stk1'],x['date'],report_data_combined), axis=1)
raw_report = check_five_factor(raw_report, five_factor_dataset)
raw_report.rename(columns={'序号':'old_id','rm_rf':'rm_rf_f1','smb':'smb_f1','hml':'hml_f1','rmw':'rmw_f1','cma':'cma_f1'}, inplace=True)
industry_processed = process_industry(industry_dataset)
raw_report = pd.merge(raw_report, industry_processed, how='left', on='stk1')
raw_report.to_excel(processed_path+'processed_report_'+current_trading_date+'.xlsx', index=False)


# %%
