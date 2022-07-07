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
% Read in Filtered data
ExG_tap_lpf = csvread("ExG_tap_lpf.csv");       % Tapping artifact
ExG_blink_lpf = csvread("ExG_blink_lpf.csv");   % Blinking artifact
ExG_mov_lpf = csvread("ExG_mov_lpf.csv");       % Movement artifact
s_rate = 250;

% if EEG.srate > 500; wavLvl = 10
% elseif EEG.srate > 250 && EEG.srate <= 500; wavLvl = 9;
% elseif EEG.srate <=250; wavLvl = 8;
wavLvl = 8;
ThresholdRule = 'Hard';


% Signal with tapping artifact
artifacts_tap = wdenoise(reshape(ExG_tap_lpf, size(ExG_tap_lpf, 1), ...
        [])', wavLvl, 'Wavelet', 'coif4', 'DenoisingMethod', ...
        'Bayes', 'ThresholdRule', ThresholdRule, 'NoiseEstimate', ...
        'LevelDependent')' ;
ExG_tap_bayes = ExG_tap_lpf - artifacts_tap ;

% Signal with blinking artifact
artifacts_blink = wdenoise(reshape(ExG_blink_lpf, size(ExG_blink_lpf, 1), ...
        [])', wavLvl, 'Wavelet', 'coif4', 'DenoisingMethod', ...
        'Bayes', 'ThresholdRule', ThresholdRule, 'NoiseEstimate', ...
        'LevelDependent')' ;
ExG_blink_bayes = ExG_blink_lpf - artifacts_blink ;

% Signal with movement artifact
artifacts_mov = wdenoise(reshape(ExG_mov_lpf, size(ExG_mov_lpf, 1), ...
        [])', wavLvl, 'Wavelet', 'coif4', 'DenoisingMethod', ...
        'Bayes', 'ThresholdRule', ThresholdRule, 'NoiseEstimate', ...
        'LevelDependent')' ;
ExG_mov_bayes = ExG_mov_lpf - artifacts_mov ;


% Export resulting data
csvwrite("ExG_tap_bayes_m.csv", transpose(ExG_tap_bayes))
csvwrite("ExG_blink_bayes_m.csv", transpose(ExG_blink_bayes))
csvwrite("ExG_mov_bayes_m.csv", transpose(ExG_mov_bayes))