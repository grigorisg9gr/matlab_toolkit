function plot_landmarks(points, im, print_numbers)
% % Accepts an image and plots the sparse points. 
% % ARGS:
% % points: The 2D coordinates of the landmarks. Expected in 
% %         the format of [numLandmarks, 2] (first x, then y). To resize from 
% %         [2*numLandmarks, 1] to the proper format of [numLandmarks, 2] use: 
%           points = reshape(points, [uint8(max(size(points)) / 2), 2]);
% % im: image to overlay the landmarks. If not provided, plot only the points.
% % print_numbers: Optional arg to print the ascending id of each landmark.

if min(size(points)) == 1
    % assume that the landmarks are in the improper format of [1, 2*numLandmarks], thus 
    % reshape:
    points = reshape(points, [uint8(max(size(points)) / 2), 2]);
end
if nargin < 2
    tt = ceil(max(points, [], 1));
    width = tt(1) + 20; height = tt(2) + 20;  % due to matlab not allowing two outputs above.
    im = ones(height, width);
end
if nargin < 3
    print_numbers = 0;
end
imshow(im);hold on;
for p = 1:size(points,1)
    plot(points(p,1), points(p,2), 'b.', 'markersize', 14);
    if print_numbers
        text(points(p,1), points(p,2), num2str(p));
    end
end
drawnow;
hold off;
end
