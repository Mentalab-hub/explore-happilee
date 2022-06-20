%% WAVELET THRESHOLDING

% Read in Filtered data
ExG_filt = csvread("ExG_filt.csv");
s_rate = 250;


% if EEG.srate > 500; wavLvl = 10
% elseif EEG.srate > 250 && EEG.srate <= 500; wavLvl = 9;
% elseif EEG.srate <=250; wavLvl = 8;
wavLvl = 8;
ThresholdRule = 'Hard';

%% Universal
artifacts = wdenoise(reshape(ExG_filt, size(ExG_filt, 1), ...
        [])', wavLvl, 'Wavelet', 'coif4', 'DenoisingMethod', ...
        'UniversalThreshold', 'ThresholdRule', ThresholdRule, 'NoiseEstimate', ...
        'LevelDependent')' ;

ExG_univ = ExG_filt - artifacts ;

% Export resulting data
csvwrite("ExG_univ_m.csv", transpose(ExG_univ))


%% Bayes
artifacts = wdenoise(reshape(ExG_filt, size(ExG_filt, 1), ...
        [])', wavLvl, 'Wavelet', 'coif4', 'DenoisingMethod', ...
        'Bayes', 'ThresholdRule', ThresholdRule, 'NoiseEstimate', ...
        'LevelDependent')' ;

ExG_bayes = ExG_filt - artifacts ;

% Export resulting data
csvwrite("ExG_bayes_m.csv", transpose(ExG_bayes))