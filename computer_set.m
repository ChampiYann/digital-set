% matrix =        [2 3 2 3;3 3 3 3;3 3 1 2]; %Shape: oval,rect,wave
% matrix(:,:,2) = [1 1 2 1;2 2 3 2;3 2 2 3]; %number: 1,2,3
% matrix(:,:,3) = [2 2 3 1;3 3 1 2;1 2 1 3]; %color: red, green, purple
% matrix(:,:,4) = [3 2 2 1;1 3 3 3;1 2 3 2]; %fill: empty,half,full

general=nchoosek([1:12],3);

%shape possibilities
shape_pos = nchoosek(reshape(matrix(:,:,1)',1,[]),3);
shape_sum = sum(shape_pos,2);

%number possibilities
num_pos = nchoosek(reshape(matrix(:,:,2)',1,[]),3);
num_sum = sum(num_pos,2);

%color possibilities
color_pos = nchoosek(reshape(matrix(:,:,3)',1,[]),3);
color_sum = sum(color_pos,2);

%fill possibilities
fill_pos = nchoosek(reshape(matrix(:,:,4)',1,[]),3);
fill_sum = sum(fill_pos,2);

%find pair
result = find(mod(shape_sum,3)==0&mod(num_sum,3)==0&mod(color_sum,3)==0&mod(fill_sum,3)==0);

disp(general(result,:))