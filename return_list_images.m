function [img_list, suffix] = return_list_images(p_fr)
% Returns the list of images in a path.
% It tries to find the first non-empty extension that returns images.
% ASSUMPTION: All images have the same extension.
assert(isdir(p_fr) == 1); 

% additional considered extensions (ONLY if the previous are empty).
ext = {'png', 'jpg', 'jpeg', 'pgm'};

for i = 1:length(ext)
    img_list = dir([p_fr, '*', ext{i}]); 
    if ~isempty(img_list)
        % if found a non-empty set. 
        break;
    end
end
if ~isempty(img_list)
    suffix = ext{i};
else
    suffix = [];  % just in case it's eventually empty.
end
end
