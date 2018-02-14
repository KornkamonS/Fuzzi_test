function [output, class_anss_] = t2fls_m2(x, params, rules, match_list, y_precision, teta_precision)
%%
%   here
%
%
%   y_precision = 2;    %   y setp is 1/y_precision
%   teta_precision = 2; %   # of teta is teta_precision+1
%
%%

output = 0;


umf = params{1,2};
lmf = params{2,2};
mf_idx = params{3,2};   %   เอาไว้เรียง mf จากน้อยไปมาก
b_dom = params{4,2};    %   ไม่ใช้
cumf = params{5,2};
clmf = params{6,2};

dim = size(umf,2);   %   ตามจำนวน feature
max_y = max(cumf(:,3,2));
class_num = size(cumf(:,3,2),1);

%   fuzzification
%   for now rule # == class #

gr = zeros([size(mf_idx) , 2]);

%   for upper mf

for h = 1:dim
   umf_ = umf{h};
   lmf_ = lmf{h};
   c = size(umf_,1);
   
   for i = 1:c
       
        x_ = x(h);
        a = umf_(i,1);
        b = umf_(i,2);
        c_ = umf_(i,3);
        d = 1;
        
        if i == 1
            e = 1;
        elseif i == c
            e = 2;
        else
            e = 0;
        end
        
        gr(i,h,1) = trimf(x_,a,b,c_,d,e);
        
        %..
        
        a = lmf_(i,1);
        b = lmf_(i,2);
        c_ = lmf_(i,3);
        d = lmf_(i,4);
                
        gr(i,h,2) = trimf(x_,a,b,c_,d,e);
        
   end
end


% 
% for i = 1:c
%     for h = 1:dim
%         
%         x_ = x(h);
%         a = umf(i,1,h);
%         b = umf(i,2,h);
%         c_ = umf(i,3,h);
%         d = 1;
%         
%         if i == 1
%             e = 1;
%         elseif i == c
%             e = 2;
%         else
%             e = 0;
%         end
%         
%         gr(i,h,1) = trimf(x_,a,b,c_,d,e);
%         
%     end
% end
% 
% %   for lower mf
% for i = 1:c
%     for h = 1:dim
%         
%         x_ = x(h);
%         a = lmf(i,1,h);
%         b = lmf(i,2,h);
%         c_ = lmf(i,3,h);
%         d = lmf(i,4,h);
%         
%         if i == 1
%             e = 1;
%         elseif i == c
%             e = 2;
%         else
%             e = 0;
%         end
%         
%         gr(i,h,2) = trimf(x_,a,b,c_,d,e);
%         
%     end
% end

%   firing trigger according to rules
rule_num = size(rules,1);

ft = zeros(rule_num, 2);

% x
% gr

for i = 1:rule_num
    ant = zeros(dim,2);
    for j = 1:dim
       amf = rules(i,j);    %   antecedent mf selector
       if amf == 0
          ant(j,1) = max(gr(:, j, 1));
          ant(j,2) = max(gr(:, j, 2));
       else
          ant(j,1) = gr(amf, j, 1);
          ant(j,2) = gr(amf, j, 2);
       end
    end
    
%     ant
    
    ft(i,1) = min(ant(:,1));
    ft(i,2) = min(ant(:,2));
end


ft_old = ft;

% x
% ft_old

class_anss = zeros(class_num,1);

    for ii = 1:class_num
        
        output_mf_idx = zeros(rule_num,1) + 1;  %   use NOT mf by default
        
        ft = ft_old;
        
        yes_idx = (match_list == ii);
        output_mf_idx(yes_idx) = 2;
        
%         output_mf_idx
        
        %   Create T2 Output
                y = 0:(1/y_precision):max_y;

                c_mf = zeros(rule_num,size(y,2),2);
                
                yll = zeros(rule_num,1);
                yrl = zeros(rule_num,1);
                
                nz_c_mf = {};
                nz_y = {};
                nz_r = [];

%                 ft

                % % % tic
                for i = 1:rule_num
                   %    consequence sets
                   rule_idx = match_list(i);
                   c_mf(i,:,1) = trimf(y,cumf(rule_idx,1,output_mf_idx(i)),cumf(rule_idx,2,output_mf_idx(i)),cumf(rule_idx,3,output_mf_idx(i)),cumf(rule_idx,4,output_mf_idx(i)),0);
                   c_mf(i,:,2) = trimf(y,clmf(rule_idx,1,output_mf_idx(i)),clmf(rule_idx,2,output_mf_idx(i)),clmf(rule_idx,3,output_mf_idx(i)),clmf(rule_idx,4,output_mf_idx(i)),0);
% 
%                    i
%                    c_mf(:,:,1)
                   
                   %    MIN with firing triggers
                   c_mf(i,:,1) = min([c_mf(i,:,1) ; repmat(ft(i,1),[1,size(y,2)])]);
                   c_mf(i,:,2) = min([c_mf(i,:,2) ; repmat(ft(i,2),[1,size(y,2)])]);
                   
                   
                   %   find non-zero c_mf for each rule
                   idx_u = find(c_mf(i,:,1));
                   
                   if size(c_mf(i,idx_u,1),2) > 0
                       nz_c_mf = [nz_c_mf; {c_mf(i,idx_u,1), c_mf(i,idx_u,2)}];
                       nz_y = [nz_y; {y(idx_u)}];
                       nz_r = [nz_r; i];
                       
                   end
                   
%                    i
%                    c_mf
                   
%                    s_ = size(find(c_mf(i,:,1)>0, 1, 'first'));
% 
%                    %    find Yl and Yr for type reduction
%                    if s_(1,2) > 0
%                        yll(i) = find(c_mf(i,:,1)>0, 1, 'first');
%                        yrl(i) = find(c_mf(i,:,1)>0, 1, 'last');
%                    else
%                        yll(i) = 0;
%                        yrl(i) = 0;
%                    end


                end
                
                %   finding yll & yrl
                for i = 1:size(nz_c_mf,1)
                    c = nz_c_mf(i,:);
                    
                    c_ = [c{2};c{1}];
                    c_step = (c_(2,:)-c_(1,:))/teta_precision;
                    c_size = size(c{1},2);
                    
                    rep_tet = repmat((0:(teta_precision))',[1,c_size]);
                    rep_step = repmat(c_step,[teta_precision+1,1]);
                    rep_min = repmat(c_(1,:),[teta_precision+1,1]);
                    c_ = rep_tet.*rep_step+rep_min;
                                        
                    %   https://www.mathworks.com/matlabcentral/answers/17266-create-cell-array-with-the-same-string-n-times
                    teta_idx = cell(1,c_size);
                    teta_idx(:) = {1:(teta_precision+1)};
                    teta_comb = allcomb(teta_idx{:});
                    
                    vv = zeros(size(teta_comb));
                    for j = 1:size(teta_comb,1)
                        for k = 1:size(teta_comb,2)
                            vv(j,k) = c_(teta_comb(j,k),k);
                        end
                    end
                    
                    vv.*repmat(nz_y{i},[size(teta_comb,1),1]);
                    ys = sum(vv.*repmat(nz_y{i},[size(teta_comb,1),1]),2)./sum(vv,2);
                    ys_ = ys(ys>0);
                    yll(nz_r(i)) = min(ys_);
                    yrl(nz_r(i)) = max(ys_);
                end
                              
                
                
                % % % toc

%                 yll = yll/precision;
%                 yrl = yrl/precision;

%                 %   MAX conseq sets from the rules
%                 ts_set = zeros(2, size(y,2));
%                 ts_set = max(c_mf);
                
%                 ts_set

                %   TYPE REDUCTION HERE!
                max_loop = rule_num;

                %   R
                found_the_r = false;
                the_r = -1;
                iter = 0;

                %   check non zero elements
                if nnz(yrl) == 1
%                    yr = sum(yrl.*(yrl > 0));
                   found_the_r = true;
                end

                % ft

                %   sort Yl and Yr
                [sorted, sort_idx] = sort(yrl);
                yrl = yrl(sort_idx);
                yll = yll(sort_idx);
                ft(:,1) = ft(sort_idx,1);
                ft(:,2) = ft(sort_idx,2);

                frl = (ft(:,1) + ft(:,2))/2;    %   yr = sum(frl*yrl)/sum(frl)
                yr = sum(frl.*yrl)/sum(frl);
                yrp = yr;   %   yr' = yr
                
                epsi = 0.0000001;   %   to eliminate small error (10^-14) from calculation

                while ~found_the_r && iter < max_loop
                    %   find R
                    for i = 1:rule_num-1
                        if yrl(i) <= yrp && yrp <= yrl(i+1)+epsi
                           the_r = i; 
                        end
                    end
                    
                    %   change epsi to exactly 0 then see the error
                    if the_r < 1
                       yr = yrp;
                       x
                       yrl
                       i
                       class(yrl(i))
                       yrp
                       yrl(i+1)
                       yrp-yrl(i+1)
                       ft
                       ant
                       gh
                       break;
                    end

                    %   create new set of fr from R
                    frn = zeros(rule_num,1);
                    frn(1:the_r) = ft(1:the_r,2);
                    frn(the_r+1:end) = ft(the_r+1:end,1);
                    yr = sum(frn.*yrl)/sum(frn);
                    yrpp = yr;

                    if yrpp ~= yrp
                        yrp = yr;
                    else
                        found_the_r = true;
                        yrpp = yr;
                    end

                    iter = iter + 1;
                end


                %   L
                found_the_l = false;
                the_l = -1;
                iter = 0;

                %   check non zero elements
                if nnz(yll) == 1
%                    yl = sum(yll.*(yll > 0));
                   found_the_l = true;
                end

                fll = (ft(:,1) + ft(:,2))/2;    %   yl = sum(fll*yll)/sum(fll)
                yl = sum(fll.*yll)/sum(fll);
                ylp = yl;   %   yl' = yl

                while ~found_the_l && iter < max_loop
                    %   find L
                    for i = 1:rule_num-1
                        if yll(i) <= ylp && ylp <= yll(i+1)+epsi
                           the_l = i; 
                        end
                    end

                    if the_l < 1
                       yl = ylp;
                       break; 
                    end
                    %   create new set of fl from L
                    fln = zeros(rule_num,1);
                    fln(1:the_l) = ft(1:the_l,1);
                    fln(the_l+1:end) = ft(the_l+1:end,2);
                    yl = sum(fln.*yll)/sum(fln);
                    ylpp = yl;

                    if ylpp ~= ylp
                        ylp = yl;
                    else
                        found_the_l = true;
                        ylpp = yl;
                    end

                    iter = iter + 1;
                end

                the_y = (yl + yr)/2;
                dist_ = the_y;

%                 disp('...');
%                 yll'
%                 yl
%                 yrl'
%                 yr
              class_anss(ii) = dist_;
        
    end
    
% % % %                 %   Create T2 Output
% % % %                 precision = 10;
% % % %                 y = b_dom(end,1):(1/precision):b_dom(end,2);
% % % %                 c_mf = zeros(rule_num,size(y,2),2);
% % % % 
% % % %                 yll = zeros(rule_num,1);
% % % %                 yrl = zeros(rule_num,1);
% % % % 
% % % %                 % ft
% % % % 
% % % %                 % % % tic
% % % %                 for i = 1:rule_num
% % % %                    %    consequence sets
% % % %                    rule_idx = match_list(i);
% % % %                    c_mf(i,:,1) = trimf(y,cumf(rule_idx,1),cumf(rule_idx,2),cumf(rule_idx,3),cumf(rule_idx,4),0);
% % % %                    c_mf(i,:,2) = trimf(y,clmf(rule_idx,1),clmf(rule_idx,2),clmf(rule_idx,3),clmf(rule_idx,4),0);
% % % % 
% % % %                    %    MIN with firing triggers
% % % %                    c_mf(i,:,1) = min([c_mf(i,:,1) ; repmat(ft(i,1),[1,size(y,2)])]);
% % % %                    c_mf(i,:,2) = min([c_mf(i,:,2) ; repmat(ft(i,2),[1,size(y,2)])]);
% % % % 
% % % %                    s_ = size(find(c_mf(i,:,1)>0, 1, 'first'));
% % % % 
% % % %                    %    find Yl and Yr for type reduction
% % % %                    if s_(1,2) > 0
% % % %                        yll(i) = find(c_mf(i,:,1)>0, 1, 'first');
% % % %                        yrl(i) = find(c_mf(i,:,1)>0, 1, 'last');
% % % %                    else
% % % %                        yll(i) = 0;
% % % %                        yrl(i) = 0;
% % % %                    end
% % % % 
% % % %                 %    subplot(rule_num+1,1,i);
% % % %                 %    hold on;
% % % %                 %    plot(y,c_mf(i,:,1));
% % % %                 %    plot(y,c_mf(i,:,2));
% % % %                 %    hold off;
% % % %                 end
% % % %                 % % % toc
% % % % 
% % % %                 yll = yll/precision;
% % % %                 yrl = yrl/precision;
% % % % 
% % % %                 %   MAX conseq sets from the rules
% % % %                 ts_set = zeros(2, size(y,2));
% % % %                 ts_set = max(c_mf);
% % % % 
% % % %                 % ts_set
% % % % 
% % % %                 % subplot(rule_num+1,1,rule_num+1);
% % % %                 % hold on;
% % % %                 % plot(y,ts_set(1,:,1));
% % % %                 % plot(y,ts_set(1,:,2));
% % % %                 % hold off;
% % % % 
% % % %                 % x
% % % %                 % ft
% % % % 
% % % %                 %   TYPE REDUCTION HERE!
% % % %                 max_loop = 100;
% % % % 
% % % %                 %   R
% % % %                 found_the_r = false;
% % % %                 the_r = -1;
% % % %                 iter = 0;
% % % % 
% % % %                 %   check non zero elements
% % % %                 if nnz(yrl) == 1
% % % %                    yr = sum(yrl.*(yrl > 0));
% % % %                    found_the_r = true;
% % % %                 end
% % % % 
% % % %                 % ft
% % % % 
% % % %                 %   sort Yl and Yr
% % % %                 [sorted, sort_idx] = sort(yrl);
% % % %                 yrl = yrl(sort_idx);
% % % %                 yll = yll(sort_idx);
% % % %                 ft(:,1) = ft(sort_idx,1);
% % % %                 ft(:,2) = ft(sort_idx,2);
% % % % 
% % % %                 frl = (ft(:,1) + ft(:,2))/2;    %   yr = sum(frl*yrl)/sum(frl)
% % % %                 yr = sum(frl.*yrl)/sum(frl);
% % % %                 yrp = yr;   %   yr' = yr
% % % % 
% % % %                 epsi = 0.00001;
% % % % 
% % % %                 while ~found_the_r && iter < max_loop
% % % %                     %   find R
% % % %                     for i = 1:rule_num-1
% % % %                         if yrl(i) <= yrp + epsi && yrp <= yrl(i+1) + epsi
% % % %                            the_r = i; 
% % % %                         end
% % % %                     end
% % % % 
% % % %                     if the_r < 1
% % % %                        yr = -1;
% % % %                 %        yrp
% % % %                 %        yrl
% % % %                 %        gh
% % % %                        break;
% % % %                     end
% % % % 
% % % %                     %   create new set of fr from R
% % % %                     frn = zeros(rule_num,1);
% % % %                     frn(1:the_r) = ft(1:the_r,1);
% % % %                     frn(the_r+1:end) = ft(the_r+1:end,2);
% % % %                     yr = sum(frn.*yrl)/sum(frn);
% % % %                     yrpp = yr;
% % % % 
% % % %                     if yrpp ~= yrp
% % % %                         yrp = yr;
% % % %                     else
% % % %                         found_the_r = true;
% % % %                         yrpp = yr;
% % % %                     end
% % % % 
% % % %                     iter = iter + 1;
% % % %                 end
% % % % 
% % % % 
% % % %                 %   L
% % % %                 found_the_l = false;
% % % %                 the_l = -1;
% % % %                 iter = 0;
% % % % 
% % % %                 %   check non zero elements
% % % %                 if nnz(yll) == 1
% % % %                    yl = sum(yll.*(yll > 0));
% % % %                    found_the_l = true;
% % % %                 end
% % % % 
% % % %                 fll = (ft(:,1) + ft(:,2))/2;    %   yl = sum(fll*yll)/sum(fll)
% % % %                 yl = sum(fll.*yll)/sum(fll);
% % % %                 ylp = yl;   %   yl' = yl
% % % % 
% % % %                 while ~found_the_l && iter < max_loop
% % % %                     %   find L
% % % %                     for i = 1:rule_num-1
% % % %                         if yll(i) <= ylp + epsi && ylp <= yll(i+1) + epsi
% % % %                            the_l = i; 
% % % %                         end
% % % %                     end
% % % % 
% % % %                     if the_l < 1
% % % %                        yl = -1;
% % % %                        break; 
% % % %                     end
% % % %                     %   create new set of fl from L
% % % %                     fln = zeros(rule_num,1);
% % % %                     fln(1:the_l) = ft(1:the_l,2);
% % % %                     fln(the_l+1:end) = ft(the_l+1:end,1);
% % % %                     yl = sum(fln.*yll)/sum(fln);
% % % %                     ylpp = yl;
% % % % 
% % % %                     if ylpp ~= ylp
% % % %                         ylp = yl;
% % % %                     else
% % % %                         found_the_l = true;
% % % %                         ylpp = yl;
% % % %                     end
% % % % 
% % % %                     iter = iter + 1;
% % % %                 end
% % % % 
% % % %                 the_y = (yl + yr)/2;
% % % %                 dist_ = the_y;
% % % % 






% ys = cumf(:,2);



% 
% %   type reduction
% %   we use center-of-set type reduction, so we can use firing triggers (ft)
% %   directly
% 
% %   hard code
% %       we have 5 rules
% %       we discretize type-1 into just 2 points (upper bound & lower bound)
% %       so it will be 2^5 sticks
% %
% 
% outputs_loc = [];
% ys = cumf(:,2);
% ys
% 
% for i = 1:2
%    for j = 1:2
%       for k = 1:2
%          for l = 1:2
%             for m = 1:2
%                 ft_tmp = [ft(1,i) ft(2,j) ft(3,k) ft(4,l) ft(5,m) ];
%                 tmp_g = (ft_tmp *ys)./(sum(ft_tmp));
%                 outputs_loc = [outputs_loc ; tmp_g];
%             end
%          end
%       end
%    end
% end
% 
% %   average them for actual Y (wasn't so good)
% dist_ = mean(outputs_loc);

%   compare acrual Y position with each class center

[m_ idx] = max(class_anss);
class_anss_ = class_anss';

if m_ == -1
    output = 1; %   instead of random, default is car
%     output = 0;
fgfgfgfg
else
    output = idx;
end

% if output ~= 2
%     fff
% end

% [m_ idx] = min(abs(dist_-ys));
% output = idx;



% output = match_list(idx);

% outputs_loc

% the_l
% the_r

% yll
% yrl
% 
% yl
% yr
% 
% dist_
% idx


% %   we will come back and code defuzzification later
% %       for now, we use max
% [m_ idx] = max(ft);
% output = mean(idx);

