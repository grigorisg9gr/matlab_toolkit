function decision = use_gpu(decision, verbose)
% Checks whether the GPU should be used (if one can be found). 
% ARGS:
%     decision: (boolean) try to impose this decision if possible
%     verbose:  (boolean) Whether to print any message on potential 
%                         inconsistencies.

try
    gpuDevice();
    finds_gpu = true;
catch
    finds_gpu = false;
end

if nargin >= 1 && finds_gpu == decision
    % the decision agrees with the finds_gpu, return that.
    ;
elseif nargin >= 1 && decision
    % then, the user asks for GPU, but non is found.
    error('None GPU found, even though GPU execution was requested.\n');
end
% all the other cases covered by returning decision = False basically
decision = false;
end
