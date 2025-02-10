% datas=top5;
% datas = input(2:2:end, :);
datas=hs300(4,:);



factors=zeros(11,length(datas(:,1)))
for a=1:length(datas(:,1))
    returnn=zeros(length(datas(a,:))-1,1)
    for j=2:length(datas(1,:))
        returnn(j-1)=(datas(a,j)-datas(a,j-1))/datas(a,j);
    end
    
    factors(1,a)=mean(returnn)
    factors(2,a)=std(returnn)
    factors(3,a)=min(returnn)
    factors(4,a)=prctile(returnn,25)
    factors(5,a)=median(returnn)
    factors(6,a)=prctile(returnn,75)
    factors(7,a)=max(returnn)
    factors(8,a)=skewness(returnn)
    factors(9,a)=kurtosis(returnn)
    % 计算资产平均收益率
% returns_avg = mean(returnn);
returns_avg = (datas(a,end)-datas(a,1))/length(datas(a,:))
% 计算资产年化标准差
returns_std = std(returnn);
% Returns = tick2ret(TestData)
% 计算夏普比率
     factors(10,a) = (mean(returnn) - 0.05/99) / std(returnn) * sqrt( 99);

%         factors(10,a)=sharpe(returnn,0)
    factors(11,a)=maxdrawdown(datas(a,:))
    
    factors(12,a)=length(find(returnn>0))/length(returnn)
end
