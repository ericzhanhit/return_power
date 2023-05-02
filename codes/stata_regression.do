

*** Robustness Check1: 替换网络变量
*** 拼接各种中心性， alternative_centrality
merge m:1 ins_number ym using "/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/data/230423_robust/alternative_centrality.dta"

save "/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/data/230423_robust/report_data_robust_230423.dta", replace


*** eigenvector_roll_f1
reg avg_q1_new eigenvector_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r1

reg avg_q90_new eigenvector_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r2

*** betweenness_roll_f1
reg avg_q1_new betweenness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r3

reg avg_q90_new betweenness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r4

*** closeness_roll_f1
reg avg_q1_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r5

reg avg_q90_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r6

esttab r1 r2 r3 r4 r5 r6 using model3.rtf, ar2 compress nogap b(3) t(2) keep(eigenvector_roll_f1 betweenness_roll_f1 closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1) star(* 0.1 ** 0.05 *** 0.01)

****  基于closeness 算baseline 和 full model的回归
reg avg_q1_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst i.ind_code_A if missing_select==0
est store r1

reg avg_q1_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage i.ind_code_A if missing_select==0
est store r2

reg avg_q1_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r3

reg avg_q90_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst i.ind_code_A if missing_select==0
est store r4

reg avg_q90_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage i.ind_code_A if missing_select==0
est store r5

reg avg_q90_new closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if missing_select==0
est store r6

esttab r1 r2 r3 r4 r5 r6 using model2.rtf, ar2 compress nogap b(3) t(2) keep(closeness_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1) star(* 0.1 ** 0.05 *** 0.01)




*** Robustness Check2: 划分股票上市市场
*** 拼接市场类型， markettype
merge m:1 stk1 using "/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/data/230423_robust/listed_market_place.dta"

merge 1:1 original_id using "/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/data/230312/report_data_train_avg_quantile_new90.dta"
gen avg_q90_new = ln(avg_quantile_new90/(1-avg_quantile_new90))

save "/Users/wednesday/Documents/0科研/个人研究/0哈工大_独立科研项目/1研报项目/data/230423_robust/report_data_robust_230423.dta", replace


*** 沪市
reg avg_q1_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(marketplace==1)
est store r1

reg avg_q90_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(marketplace==1)
est store r2

*** 深市
reg avg_q1_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(marketplace==2)
est store r3

reg avg_q90_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(marketplace==2)
est store r4


esttab r1 r2 r3 r4 using model1.rtf, ar2 compress nogap b(3) t(2) keep(ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1) star(* 0.1 ** 0.05 *** 0.01)


*** Robustness Check3: 疫情前和疫情后


gen date=dofc(日期)
format date %td
gen date1=date
gen outbreak=(date1>=21915)



*** 疫情前
reg avg_q1_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(outbreak==0)
est store r1

reg avg_q90_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(outbreak==0)
est store r2

*** 疫情后
reg avg_q1_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(outbreak==1)
est store r3

reg avg_q90_new ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1 i.ind_code_A if (missing_select==0)&(outbreak==1)
est store r4

esttab r1 r2 r3 r4 using model3.rtf, ar2 compress nogap b(3) t(2) keep(ln_degree_roll_f1 past_performance_avg past_performance_sd ipo ln_brokerage_analyst_num_f1 star_analyst advanced_index_old ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf_f1 smb_f1 hml_f1 rmw_f1 cma_f1) star(* 0.1 ** 0.05 *** 0.01)

















































