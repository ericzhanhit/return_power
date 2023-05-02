
import pandas as pd
import numpy as np
from functions import get_regression_data, get_regression_predict, concat_df

# 需要更新的数据
# 当天交易日
current_trading_date = '2023-04-28'
date_pre2years = (pd.to_datetime(current_trading_date) - pd.DateOffset(years=2)).strftime('%Y-%m-%d')
date_pre1years = (pd.to_datetime(current_trading_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
date_prehalfyears = (pd.to_datetime(current_trading_date) - pd.DateOffset(months=6)).strftime('%Y-%m-%d')
# 因子库文件路径
library_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/library/'
# 更新数据文件路径
downloads_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/downloads/'
# 计算好的数据文件路径
processed_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/processed/'
# 输出预测结果文件路径
recommend_path = '/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/Stock_recommend/recommendations/'

# 导入report_data_combined,若已导入可不需要重复导入
#report_data_combined = pd.read_excel(library_path+'report_data_combined.xlsx')
#report_data_combined['date'] = pd.to_datetime(report_data_combined['date'])
#report_data_combined['stk1'] = report_data_combined['stk1'].map(lambda x: str(x).rjust(6,'0'))

processed_report_date = pd.read_excel(processed_path+'processed_report_'+current_trading_date+'.xlsx')

# 全样本回测
train_label_all_samples, x_train_all_samples = get_regression_data(report_data_combined, end_date=current_trading_date)
report_all_samples_top = get_regression_predict(train_label_all_samples, x_train_all_samples, processed_report_date, sample_size=20)

# 近两年回测
train_label_latest2year, x_train_latest2year = get_regression_data(report_data_combined, start_date=date_pre2years, end_date=current_trading_date)
report_latest2year_top = get_regression_predict(train_label_latest2year, x_train_latest2year, processed_report_date, sample_size=20)

# 近一年回测
train_label_latest1year, x_train_latest1year = get_regression_data(report_data_combined, start_date=date_pre1years, end_date=current_trading_date)
report_latest1year_top = get_regression_predict(train_label_latest1year, x_train_latest1year, processed_report_date, sample_size=20)

# 近半年回测
train_label_latesthalfyear, x_train_latesthalfyear = get_regression_data(report_data_combined, start_date=date_prehalfyears, end_date=current_trading_date)
report_latesthalfyear_top = get_regression_predict(train_label_latesthalfyear, x_train_latesthalfyear, processed_report_date, sample_size=20)

report_concat_data = concat_df(report_all_samples_top, report_latest2year_top, report_latest1year_top, report_latesthalfyear_top)
report_concat_data.to_excel(recommend_path+'recommend_stock_'+current_trading_date+'.xlsx')

