function result = modify_gdocs(opt,varargin)
% grigoris, 24 July 2014: This function makes all modifications/requests to
% gdocs. It calls the python script "modiy_drive" with the following
% options: 
% for writing:              modify_gdocs('w', Name_of_Spreadsheet, Name_of_Worksheet, row, col, value)
% for reading one value:    value = modify_gdocs('r', Name_of_Spreadsheet, Name_of_Worksheet, row, col)
% for reading a range:      values = modify_gdocs('rr', Name_of_Spreadsheet, Name_of_Worksheet, row_start, row_end, col_start, col_end)
%
% Copyright (C) 2014 Grigorios G. Chrysos
% available under the terms of the Apache License, Version 2.0

% constants: 
uid =   'your_mail@gmail.com';              % your e-mail id 
pass =  'pass';                             % password of your e-mail
path =  '/path/to/project/';                % path of the file modify_drive.py

str = form_varargin(varargin);
if strcmp(opt, 'w') % write in gdoc  
    num_opt = '1';
elseif strcmp(opt, 'r') % read a cell value from a gdoc
    num_opt = '2';
elseif strcmp(opt, 'rr') % read range values from a gdoc
    num_opt = '3';
elseif strcmp(opt, 'h') % prints helpful message
    fprintf('This function makes all modifications/requests to gdocs\n');
    fprintf('options: \nfor writing:\t\t\t modify_gdocs(w, Name_of_Spreadsheet, Name_of_Worksheet, row, col, value)\n');
    fprintf('for reading one value:\t\t\t value = modify_gdocs(r, Name_of_Spreadsheet, Name_of_Worksheet, row, col)\n');
    fprintf('for reading a range:\t\t\t values = modify_gdocs(rr, Name_of_Spreadsheet, Name_of_Worksheet, row_start, col_start, row_end, col_end)\n\n');
    fprintf('Copyright (C) 2014 Grigorios G. Chrysos\n\n');
    return ;
else
    warning('No such module exists, check again your first argument.'); num_opt = '0';
end
[status, result] = system(['cd ' path '; python modify_drive.py ', num_opt, ' ', str ' ' uid ' ' pass]);
if status ~=0 
    warning('Potential problem in the interaction with the gdoc. Printing stack:');
    fprintf(result);
end

end

function str = form_varargin(varargin1)
% convert varargin in a string with space among cells
str=[];
for i=1:length(varargin1)
    insert = varargin1{i};
    if isnumeric(varargin1{i})
        insert = num2str(varargin1{i});
    end
    str=[str,' ',insert];
end
end
