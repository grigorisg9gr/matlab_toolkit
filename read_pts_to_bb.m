function [f_e, box_dist] = read_pts_to_bb(path_n, file, is_ln)
% Accepts a path and a name and returns the bounding box.
% It is assumed that the pts is in a format consistent with menpo pts format.
% ARGS:
% path_n: string, either the parent folder or the full name for the file.
% file: string, optional, the filename of the file.
% is_ln: bool, optional. If true, it is assumed the input file
%        includes a bounding box, otherwise it includes 68 markup landmarks.
% Returns the bounding box in the format [xmin, ymin, xmax, ymax].

if nargin < 2
    nn = path_n;
else
    nn = [path_n, filesep, file];
end
if nargin < 3  % default is bbox
    is_ln = 0 ; 
end
try
    d=fopen(nn, 'r'); A = fscanf(d, '%c', 21); % get rid of the dummy chars in the beginning
    n_points = fscanf(d, '%i'); A = fscanf(d, '%c',2); 
    tr = fscanf(d, '%f');
    if is_ln == 0 
        assert(n_points == 4);
        x = tr(1:2:end); 
        y = tr(2:2:end);
        box_dist = [min(x), min(y), max(x), max(y)]; % [xmin, ymin, xmax, ymax]
        if box_dist(1) <= 0
            box_dist(1) = 1;
        end
        if box_dist(2) <= 0
            box_dist(2) = 1;
        end
        assert(min(box_dist > 0) == 1)
    else
        assert(n_points == 68);
        start = [min(tr(79),tr(61)), min(tr(80), tr(56))]; % min_x(pts_40, 32), min_y=(pts_40, 28)
        box_dist = [start(1), start(2), max(tr(71), tr(85))-start(1), max(tr(72),tr(68))-start(2)]; 
    end
    fclose(d); f_e = 1;
catch
    box_dist = []; f_e = 0; % file_exists
end
end
