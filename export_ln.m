function export_ln(p_out, ln, expected_points)
% Given the name of a file (p_out) and the landmarks,
% it writes them in a file. The landmarks should be in a 
% matrix of the format [numLandmarks, 2] with
% 1st dim x, 2nd the y. 
if nargin > 2
    assert(size(ln, 1) == expected_points)
end

fileID = fopen(p_out, 'w');
fprintf(fileID, 'version: 1\n');
fprintf(fileID, 'n_points: %d\n', size(ln, 1));
fprintf(fileID,'{\n');
for ft = 1 : size(ln, 1)
    fprintf(fileID, '%f %f\n', ln(ft, 1), ln(ft, 2));
end
fprintf(fileID, '}');
fclose(fileID); 
end
