segmentation:Divide the filtered data from the Butterworth filter into a sample every 8 seconds
classification:Divide all samples into three categories based on perclos values
Wavelet decomposition:db4 wavelet was used to perform six layer decomposition on EEG data, obtaining EEG signals in five frequency bands: delta (1-4 Hz), theta (4-8 Hz), alpha (8-14 Hz), beta (14-31 Hz), and gamma (31-50 Hz).
Relative wavelet energy、Relative wavelet entropy complex network、Network normalization、Threshold selection：The construction process of complex networks with relative wavelet entropy
Extract DE、Add channel columnDE、MappingDE、ClassificationDE、NormalizationDE、Data fillingDE：The construction process of differential entropy space mapping
Lift 14 channels、SQ、Add channel columnSQ、MappingSQ、NormalizationSQ、Data fillingSQ：The construction process of symmetric quotient space mapping
Symmetric quotient differential entropy fusion、Three feature fusion：The process of feature fusion
Divide training tests：Partition process for training set and dataset
Triple Splicing Classification、Verification set：For the classification and validation process
