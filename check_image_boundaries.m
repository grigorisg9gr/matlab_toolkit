function [patch_xy, diff] = check_image_boundaries(patch_xy, sz_im)
% Checks whether a bbox in the form of [x, y, width, height] is 
% inside the image boundaries.
% Returns the bbox constrained in the boundaries, along with the diff array
% that shows the potential translation required.

   diff = zeros(4, 1);
   % check the first two for left/ top borders (0 points). 
   if patch_xy(1) < 1, diff(1) = 1 - patch_xy(1); patch_xy(1) = 1; end
   if patch_xy(2) < 1, diff(2) = 1 - patch_xy(2); patch_xy(2) = 1; end
   % check the last two for the right/bottom borders (size of image).
   maxp = [patch_xy(1) + patch_xy(3), patch_xy(2) + patch_xy(4)];
   if maxp(1) > sz_im(2), diff(3) = maxp(1) - sz_im(2); patch_xy(3) = patch_xy(3) - diff(3) - 1; end
   if maxp(2) > sz_im(1), diff(4) = maxp(2) - sz_im(1); patch_xy(4) = patch_xy(4) - diff(4) - 1; end
   assert(min(patch_xy >= [1, 1, 0, 0]) && min(patch_xy(3 : 4) <= [sz_im(2), sz_im(1)]));
end
