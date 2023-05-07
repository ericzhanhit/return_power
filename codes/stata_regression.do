

reg logit_return_power_1 broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst i.industry
est store r1

reg logit_return_power_1 broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst advance_reaction ln_analyst_coverage i.industry
est store r2

reg logit_return_power_1 broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst advance_reaction  ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf smb hml rmw cma i.industry
est store r3

reg logit_return_power_90 broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst i.industry
est store r4

reg logit_return_power_90 broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst advance_reaction  ln_analyst_coverage i.industry
est store r5

reg logit_return_power_90 broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst advance_reaction  ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf smb hml rmw cma i.industry
est store r6

esttab r1 r2 r3 r4 r5 r6 using model.rtf, ar2 compress nogap b(3) t(2) keep(broker_status prior_performance_avg prior_performance_sd listed ln_broker_size star_analyst advance_reaction ln_analyst_coverage ln_page ln_num_authors ln_title_len ln_num_sentence ln_avg_sentence_len ln_sd_sentence_len rm_rf smb hml rmw cma) star(* 0.1 ** 0.05 *** 0.01)
