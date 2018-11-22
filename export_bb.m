function export_bb(bb_path, name, bb, simple)
% Given a path (bb_path) and a name, it exports the bounding box
% provided in a file. The bb can either be a 4 element bb with the format
% [xmin, ymin, xmax, ymax] or in the [2, 4] matrix. 
if nargin < 4
    simple = 1;
end
assert(length(bb) == 4)
fileID = fopen([bb_path name],'w');
fprintf(fileID,'version: 1\n');
fprintf(fileID,'n_points: 4\n');
fprintf(fileID,'{\n');
if simple == 1  % simple requires 4 values for a rectangle bb
    bb1{1} = num2str(bb(1)); bb1{2} = num2str(bb(2)); bb1{3} = num2str(bb(3)); bb1{4} = num2str(bb(4));
    fprintf(fileID,'%s %s\n', bb1{1}, bb1{2});
    fprintf(fileID,'%s %s\n', bb1{1}, bb1{4});
    fprintf(fileID,'%s %s\n', bb1{3}, bb1{4});
    fprintf(fileID,'%s %s\n', bb1{3}, bb1{2});
else
    assert(size(bb, 1) == 2);  % expected format: bb = [y1, y2, y1, y2; x1, x1, x2, x2], size(bb) = [2, 4]
    fprintf(fileID,'%f %f\n', bb(2, 1), bb(1, 1)); % written: [xmin, ymin]
    fprintf(fileID,'%f %f\n', bb(2, 2), bb(1, 2));
    fprintf(fileID,'%f %f\n', bb(2, 4), bb(1, 4));
    fprintf(fileID,'%f %f\n', bb(2, 3), bb(1, 3)); % written: [xmax, ymin]
end

fprintf(fileID,'}');
fclose(fileID); 
end
