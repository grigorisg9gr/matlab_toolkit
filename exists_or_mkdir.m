function made = exists_or_mkdir(path)
% % Accepts a path and generates the folder structure if
% % it does not exist. It returns whether it was made 
% % or already existed.
made = false;
if exist(path) == 0
    unix(['mkdir -p ' path]);
    made = true;
end
end
