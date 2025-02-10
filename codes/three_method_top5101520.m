shareNum=1000000;                         %设置初始金额；
cost_rate=0.0012;
lens=[5,10,15,20]; 
names={'olssssssssssss';'gbdt';;'LSTM'}

cycle_return=[];
cycle_pic=[];
cycle_money=[];
cycle_hs_daily=[];

% 加载区
load('d_final_processed_data.mat')

for mm=1:length(names)
    filename = strcat('recommend_',cell2mat(names(mm)));
    extension= '.xlsx';
    fullfilename = strcat(filename, extension);
% 导入 Excel 文件到 MATLAB 的数据表中
%找出不在最终列表中的值
%去掉策略中不在final_raw_data的股票代码
    dataTable = readtable(fullfilename);
   
    %数据处理：去除最终表中没有的数据
    [stk,dates,return_power_pred]=f_raw_process(dataTable,final_raw_data);
     all_date=str2double(string(datestr(dates, 'yyyymmdd')));
    uni_date=unique(all_date);
    %初始化该半年的存储结构
    final_money=zeros(2,length(uni_date));
    final_money(1,:)=uni_date; 
    final_money(2,1)=shareNum;
    final_yield=zeros(2,length(uni_date));
    final_yield(1,:)=uni_date; 
    final_yield(2,1)=0;
    final_allmoney=[];
    final_return=[];
    final_rate=[];
    final_rate(1,:)=lens;   
    
        %% 交易区
for jj=1:length(lens)
    len=lens(jj);
    p_strategy=f_strategy(dates,stk,return_power_pred,len);
   jj;
    
    for ii=1:length(final_money(1,:))-1 %从第一天交易至最后一天
        ii;
        current_date=final_money(1,ii);
        site_all=find(p_strategy(:,1)==current_date);
        %计算今日交易股票数量：
        if length(site_all)<=len
            p_len=length(site_all);
        else
            p_len=len;
        end
        %计算交易情况，并记录购买股票的手数
        %1：标的代码；2：买入单价；3：卖出单价；4.手数；5：收益
        target_calculate_structure=zeros(p_len,5);

        final_money(2,ii+1)=final_money(2,ii);
        
        final_yield(2,ii+1)=0;
        stock_list=[];
         for j=1:p_len
             stock_list(j)=p_strategy(site_all(j),2);
             target_calculate_structure(j,1)=p_strategy(site_all(j),2);
             if isnan(final_raw_data(find(final_raw_data(:,1)==target_calculate_structure(j,1)),find(final_raw_data(1,:)==current_date)))||isnan(final_raw_data(find(final_raw_data(:,1)==target_calculate_structure(j,1)),find(final_raw_data(1,:)==current_date)+1))
                  target_calculate_structure(j,4)=0;
                  target_calculate_structure(j,5)=0;
             else
                target_calculate_structure(j,2)=final_raw_data(find(final_raw_data(:,1)==target_calculate_structure(j,1)),find(final_raw_data(1,:)==current_date));
                target_calculate_structure(j,3)=final_raw_data(find(final_raw_data(:,1)==target_calculate_structure(j,1)),find(final_raw_data(1,:)==current_date)+1);
                all_money=final_money(2,find(final_money(1,:)==current_date));
                %分配手数
                target_calculate_structure(j,4)=floor(all_money*p_strategy(site_all(j),3)/target_calculate_structure(j,2));
                target_calculate_structure(j,5)=(target_calculate_structure(j,3)-target_calculate_structure(j,2))*target_calculate_structure(j,4)-target_calculate_structure(j,3)*target_calculate_structure(j,4)*cost_rate;
             end
             final_money(2,ii+1)=final_money(2,ii+1)+target_calculate_structure(j,5);
             final_yield(2,ii+1)=final_yield(2,ii+1)+target_calculate_structure(j,5);
             
         end
         
    end
    final_allmoney =[final_allmoney;final_money]   ;
    final_return=[final_return;final_yield]   ;
    
    final_rate(2,jj)=(final_money(2,end)-  final_money(2,1) )/final_money(2,1); 
end
     cycle_money=[cycle_money;final_allmoney];   
     
%      if ~isempty(find(final_hs300(1,:)==uni_date(end)))&&~isempty(find(final_hs300(1,:)==uni_date(1)))
%         final_rate(1,length(lens)+1)=300;
%          final_rate(2,length(lens)+1)=         (final_hs300(2, find(final_hs300(1,:)==uni_date(end)))-final_hs300(2,find(final_hs300(1,:)==uni_date(1))))/final_hs300(2,find(final_hs300(1,:)==uni_date(1)))
%      else
%          final_rate(1,length(lens)+1)=300;
%          final_rate(2,length(lens)+1)=nan;
%          
%      end
     cycle_return=[cycle_return;final_rate]   ;
     cycle_pic=[cycle_pic;final_return];
 end
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    