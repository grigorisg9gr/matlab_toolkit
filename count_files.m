function nr_files = count_files(dir1)
% % Fat way to count the files in a dir.
% % Verified against ['find ', dir1, ' -print | wc -l']  that
% % this is indeed faster.
[~,cmdout] = system(['ls -f ', dir1, '| wc -l']);
nr_files =  str2num(cmdout);
end
