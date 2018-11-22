function execution_stats_grigoris(end_line)
% % This is the version of execution_stats() from pyutils.
% % It prints some helpful messages for time/machine.
% % ARGS:
% %  end_line: Optional arg: If true, then end with a new line,
% %            otherwise print inline.
if nargin < 1
    end_line = false;
end
% grigoris, 12/3/2016: Some useful printing messages. 

% computer name:
[~,hostname]= system('hostname');
% date: 
date = datestr(now,'mmmm.dd.yyyy.HH.MM.SS');
if end_line
    fprintf('Date: %s. Computer: %s\n', date, hostname);
else
    % % the hostname include one end of line, so get rid of it.
    fprintf('[Date: %s. Computer: %s] ', date, hostname(1:end-1));
end
end
