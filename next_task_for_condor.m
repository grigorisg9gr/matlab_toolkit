function [sample1, ext] = next_task_for_condor(p_todo, p_done, verbose)
% % It accepts two paths and returns the next sample for condor.
% % This function is built for clusters with high parallelization where
% % fetching a random sample is required to achieve high throughput.
if nargin < 3, verbose = true; end
ext = ''; sample1 = [];
% check the files in the folders.
dir_todo = dir(p_todo);
dir_done = dir(p_done);

%% format in cells (equivalent of the set in python).
cell_todo = cell(length(dir_todo) - 2, 1);
for el = 3 : length(dir_todo)
    % get the stem of the strings.
    %st1 = dir_todo(el).name;
    % Assumption: There is one '.' in the string!
    %st1 = st1(1 : strfind(st1, '.') - 1);
    cell_todo{el - 2, 1} = get_stem(dir_todo(el).name);
end

% easier if it is converted into a function.
cell_done = cell(length(dir_done) - 2, 1);
for el = 3 : length(dir_done)
    cell_done{el - 2, 1} = get_stem(dir_done(el).name);
end

% sanity check that there are unique identifiers in the todo path.
d1 = setdiff(unique(cell_todo), cell_todo);
if ~isempty(d1)
    fprintf('There are no unique identifiers in the path todo.\n');
    return
end

diff1 = setdiff(cell_todo, cell_done);

%% if the same length, ensure that it is completed.
if ((length(dir_todo) == length(dir_done)) && (isempty(diff1)))
    if verbose
        fprintf('The clip is done.\n');
    end
    sample1 = [];
    return
end

%% if we are here, then there are jobs to complete.
% get the extension.
tmp = dir_todo(3).name;
dots = strfind(tmp, '.');
if size(dots, 2) > 1, dots = dots(1, end); end
ext = tmp(dots : end);
% sample one point from the difference to return.
sample1 = datasample(diff1, 1);
sample1 = sample1{1};
if verbose
    fprintf('Returning sample: %s%s.\n', sample1, ext);
end
end


function stem1 = get_stem(st1)
    % % The function accepts the name (stem + extension) and returns the stem.
    dots = strfind(st1, '.');
    if size(dots, 2) > 1
        % % 31/1/2018: This covers the case of multiple dots per image.
        dots = dots(1, end);
    end
    % Mild assumption: There is at least one '.' in the string.
    stem1 = st1(1 : dots - 1);
end





