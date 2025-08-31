clc
clear
close all
% IMPORTANT: When trying to remove outliers from the data change the below values
lowerthrust = 40; %This changes the lower bound of when to start graphing data
upperthrust = 50; %This changes the upper bound of when to stop graphing dat
MaxThrustPrecent = 2; %This sets how much larger than the peak thrust to elimate data values, ie 1.5 means elminate all values above 50% make thrust
Spacing = 10; %This is the number of data points recorded before the inital and final changes in thrust

% Define the file path for the CSV file
% file_path = 'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\New Age AeroBing\Rockets\Budget 1\Madeline STATIC FIRE\Data\2-4-24 Data\DATAMadeline2-4-24 - Important.csv';
% file_path = 'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\New Age AeroBing\Rockets\Budget 1\Madeline STATIC FIRE\Data\2-4-24 Data\DATAMadeline2-4-24.csv';
% file_path = 'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\New Age AeroBing\Static Fires\Jared;Jenna\Data\Jared12-10.csv';
% file_path = 'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\New Age AeroBing\Static Fires\Jared;Jenna\Data\JaredData11-19.txt';
% file_path = 'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\New Age AeroBing\Static Fires\Twin Cores\TwinCoreData.csv';
% file_path = 'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\New Age AeroBing\Static Fires\PP Code\DATA4-25-24';
file_path = 'DATA_TRIMMED';



%'C:\Users\happy\OneDrive - Binghamton University\Sean Weber - AeroBing\Jared\OpenMotah\Jared12-10.CSV'; % Replace 'csv2.csv' with your actual CSV file name and path

% Read the data from the CSV file
dataTable = readtable(file_path, 'HeaderLines', 1); % Skip the first row if it contains headers

%% Getting user input Variables
% Create a dialog box with a text input field
prompt1 = {'What is the expected max thrust:'};
dlgtitle1 = 'In Newtons';
dims1 = [1 35];
definput1 = {'0'}; % Default value
MaxThrust = inputdlg(prompt1,dlgtitle1,dims1,definput1);

% In case of emergenices
userInput = MaxThrust{1};
containsLetter = any(isletter(userInput));

if containsLetter
    % Load the video file
    videoFile = 'Shhhh.mp4';
    videoObj = VideoReader(videoFile);

    % Play the video frame by frame
    while hasFrame(videoObj)
        frame = readFrame(videoObj);
        imshow(frame);
        drawnow; % Update the display
    end
    return;
end


% Convert the user input to the desired variable type
MaxThrustInput = str2double(MaxThrust{1}); % Assuming the input is numeric
TooLarge = MaxThrustInput * MaxThrustPrecent;

%% Getting Data
% Extract time (first column), thrust (seventh column), and pressure (eighth column) data
time_sec = dataTable{:, 1}; % Assuming time is in the first column (in seconds)
thrust_N = dataTable{:, 3}; % Assuming thrust is in the seventh column
pressure_psi = dataTable{:, 5}; % Assuming pressure is in the eighth column
L = length(thrust_N); % Lenght of the thust matrix

% Convert time from seconds to milliseconds
time_ms = time_sec / 1000; % Convert time to milliseconds

% Find indices where thrust is greater than 20N and drops below 20N
indices_above_20N = find(thrust_N > upperthrust);
indices_below_20N = find(thrust_N < lowerthrust);
% These above lines are storing the location of where all the value above
% of below 5N
IAL = length(indices_above_20N);
IBL = length(indices_below_20N);
% These two above lines just find the lengths of the matricies storing the
% thrust values above and below 20N

% Take the avergae around those incideies to make sure they are the acutal
% curve and not just ranom data points
% indices_above_20N_after = zeros(IAL ,1);
diffthrust = zeros((2*Spacing) + 1, 1);
indices_above_20Nfixed = zeros(1);
% These two above lines r just creating vectors to speed up processing time
j = 1;
l = 2;
% The two above lines just set the variable for the for loops
for i = 1:IAL
    l = 2; % This just resets the varibale l back to 2 after each loop
    k = indices_above_20N(i,1); % This is just storing the force locations from the beginning to the current lopp itteriation
    iThrustData = thrust_N(k-Spacing:k+Spacing, 1); % This is creating a new matrix gathering 20 thrust values before and after the current value the loop is evaulating
    ITDlen = length(iThrustData); % This is finding the length of that value
    DumbBig = thrust_N(k, 1); % This is storing the current thrust value being evaluated 
    if DumbBig > TooLarge % 10000
        continue
    end
    % This if statment is testing if the current thrust value is under a
    % certain value and telling the loop to continue if it is

    % The continue function here basically removes that thrust value from
    % the accurate thrust values by making the for loop skip over it before
    % it can store the value as you see later

    diffthrust = diff(iThrustData); % This caluclates the difference between each thrust value 
    if max(diffthrust) > 1000
        continue
    end
    % This if statment is checking to see if the differences over the each
    % thrust are too high indicating that it should be ignored
    % and using the continue function to do it

    iAvg = sum(iThrustData)/length(iThrustData); % This is just finding the average of the new thrust values we created for this loop
    if iAvg > 20
        indices_above_20Nfixed(j, 1) = indices_above_20N(i, 1);
        j = j + 1;
    end
    % This for loop is taking all the value that pass the previous tests
    % and creating a new matrix for all the loctions of these fixed thrust
    % values
end

if indices_above_20Nfixed == 0
    disp('There were not enough data points to gather data now displaying the max pressure and thrust recorded')
    disp(['Max Thrust: ',num2str(thrust_N(indices_above_20N(end), 1)), ' Max Pressure: ', num2str(pressure_psi(indices_above_20N(end)))])
    return
end
% Just in case there are no found values for the fixed thrust location
% values it dispalys the max pressure and thrust recorded

% Check if the thrust drops below 20N in the data
if ~isempty(indices_below_20N) %This isempty function just tells us if 
% there are no value that go below 20N and by adding the ~ infront of it, it becomes the reverse of that so now
% this whole if function just serves to tell us if there are any values above 20N

    % Select 200 points around when thrust exceeds 20N
    start_A20N = max(indices_above_20Nfixed(1) - Spacing, 1);
    % This selects a point 100 data points before the target point to
    % beging graphing. The max(---, 1) just makes sure this number is
    % positve and doesnt break anything
    end_index_A20N = min(indices_above_20Nfixed(1) + Spacing, length(thrust_N));
    % This selects a point 100 data points after the target point to
    % beging graphing. The max(---, 1) just makes sure this number is
    % positve and doesnt break anything. Doesnt even look like its used    

    % Select data after the last time thrust drops below 20N
    % LDB = indices_below_20N(end);
    % This finds the last data value of the indices_below_20N matrix
    % BeginNew = LDB + 1;
    % This just creates a new data point by adding one to the LDB variable
    % meaing its exactly one grater than the end of the previous matrix
    % end_A20N = min(LDB + 200, length(thrust_N));
    % This makes sure that the data value we got for the BeginNew matix is
    % actually the minmum value by comparing it to the next 200 data points

    % The above way was fuckng stupid and wrong. Imma fix it
    LDB2 = indices_above_20Nfixed(end);
    BeginNew2 = LDB2 + 1;
    TimeofBurn = time_ms(indices_above_20Nfixed(end)) - time_ms(indices_above_20Nfixed(1));
    end_A20N = min(LDB2 + 200, LDB2);


    
    % Filtered data based on conditions
    filtered_time_above_20N = time_ms(start_A20N:end_A20N);
    filtered_thrust_above_20N = thrust_N(start_A20N:end_A20N);
    filtered_pressure_above_20N = pressure_psi(start_A20N:end_A20N);
    % All three of these are now isolating the data we are actually gonna
    % graph over and whats acutlaly important 
    
    % Calculate Impulse (Riemann sum of thrust)
    dt = diff(filtered_time_above_20N); % Calculate time intervals
    impulse = sum(filtered_thrust_above_20N(1:end-1) .* dt); % Riemann sum calculation
    
    % Plot time vs. thrust and pressure
    figure;
    subplot(2, 1, 1);
    plot(filtered_time_above_20N, filtered_thrust_above_20N, '-');
    xlabel('Time (s)');
    ylabel('Thrust (N)');
    title('Time vs. Thrust');
    grid on;
    
    % Display maximum thrust value in the top left corner of the thrust plot
    max_thrust = max(filtered_thrust_above_20N);
    text(0.02, 0.98, sprintf('Max Thrust: %.2f N', max_thrust), 'Units', 'normalized', 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top', 'Color', 'red', 'FontSize', 10, 'Parent', gca);
    
    % Display Impulse under the max thrust on the graph
    text(0.02, 0.85, sprintf('Impulse: %.2f Ns', impulse), 'Units', 'normalized', 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top', 'Color', 'blue', 'FontSize', 10, 'Parent', gca);

     % Display Impulse under the Time burnt
    timeBurn = time_ms(end_A20N) - time_ms(start_A20N);
    text(0.02, 0.72, sprintf('Burn Time: %.2f Ns', timeBurn), 'Units', 'normalized', 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top', 'Color', 'green', 'FontSize', 10, 'Parent', gca);
    
    subplot(2, 1, 2);
    plot(filtered_time_above_20N, filtered_pressure_above_20N, '-');
    xlabel('Time (s)');
    ylabel('Pressure (psi)');
    title('Time vs. Pressure');
    grid on;
    
    % Display maximum pressure value in the top left corner of the pressure plot
    max_pressure = max(filtered_pressure_above_20N);
    text(0.02, 0.98, sprintf('Max Pressure: %.2f psi', max_pressure), 'Units', 'normalized', 'HorizontalAlignment', 'left', 'VerticalAlignment', 'top', 'Color', 'red', 'FontSize', 10, 'Parent', gca);
else
    disp('Thrust does not drop below 20N in the data.');
end
