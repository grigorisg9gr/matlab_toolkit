function [f_e, lns] = read_pts_to_ln(path_n, file)
% Accepts a path and a name and returns the landmarks.
% It is assumed that the pts is in a format consistent with menpo pts format.
% ARGS:
% path_n: string, the parent folder for the file.
% file: string, the filename of the file.
% Returns the matrix of landmarks in the format ([x1, y1; x2, y2;...]).

try
    d=fopen([path_n, filesep, file], 'r'); A = fscanf(d, '%c', 21); % get rid of the dummy chars in the beginning
    n_points = fscanf(d, '%i'); A = fscanf(d, '%c',2); 
    tr = fscanf(d, '%f');
    x = tr(1:2:end); 
    y = tr(2:2:end);
    lns = [x, y];
    fclose(d); f_e = 1;
catch
    lns = []; f_e = 0; % file_exists
end
end
