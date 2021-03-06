import numpy
from scipy.stats import pearsonr

# This function was borrowed from https://github.com/esdalmaijer/reliability/
def split_half(x, n_splits=100, mode='spearman-brown'):
    
    """Computes the split-half reliability, which speaks to the internal
    consistency of the measurement.
    
    Example usage: Say you have a sample of 100 participants, and you assessed
    them with a questionnaire with 20 items that all measure the same
    construct. This data is in a variable 'x' with shape (20, 100). To compute
    the split-half reliability, call:

    r, sem = split_half(x, n_splits=100, mode='spearman-brown')
    
    The variable 'r' tells you the split-half reliability, the variable 'sem'
    reflects the standard error of the mean, computed as the square root of
    the standard deviation of r divided by the square root of the number of
    splits, i.e. sem = sd / sqrt(n_splits)
    
    Arguments
    
    x           -   A NumPy array with shape (M,N), where M is the number of
                    observations and N is the number of participants or tests.
                    M will be split in half to compute the reliability, not N!
    
    Keyword Arguments
    
    n_splits    -   An integer that indicates the number of times you would
                    like to split the data in X. Default value is 100.
    
    mode        -   A string that indicates the type of split-half reliability.
                    You can choose from: 'correlate' or 'spearman-brown'.
                    Default value is 'spearman-brown'.
    
    Returns
    (r, sem)    -   r is the average split-half reliability over n_splits.
                    sem standard error of the mean split-half reliability.
    """
    
    # Check the input.
    if n_splits < 1:
        raise Exception("Expected n_splits to be 1 or more, not '%s'." % \
            (n_splits))
    allowed_modes = ['correlation', 'spearman-brown']
    if mode not in allowed_modes:
        raise Exception("Mode '%s' not supported! Please use a mode from %s" \
            % (mode, allowed_modes))
    
    # Get the number of observations per subject, and the number of subjects.
    n_observations, n_subjects = x.shape
    
    # Compute the size of each group.
    n_half_1 = n_observations//2
    n_half_2 = n_observations - n_half_1
    # Generate a split-half-able vector. Assign the first half 1 and the
    # second half 2.
    halves = numpy.ones((n_observations, n_subjects), dtype=int)
    halves[n_half_1:, :] = 2
    
    # Run through all runs.
    r_ = numpy.zeros(n_splits, dtype=float)
    for i in range(n_splits):

        # Shuffle the split-half vector along the first axis.
        numpy.random.shuffle(halves)

        # Split the data into two groups.
        x_1 = numpy.reshape(x[halves==1], (n_half_1, n_subjects))
        x_2 = numpy.reshape(x[halves==2], (n_half_2, n_subjects))
        
        # Compute the averages for each group.
        m_1 = numpy.mean(x_1, axis=0)
        m_2 = numpy.mean(x_2, axis=0)
        
        # Compute the correlation between the two averages.
        pearson_r, p = pearsonr(m_1, m_2)

        # Store the correlation coefficient.
        if mode == 'correlation':
            r_[i] = pearson_r
        elif mode == 'spearman-brown':
            r_[i] = 2.0 * pearson_r / (1.0 + pearson_r)
    
    # Compute the average R value.
    r = numpy.mean(r_, axis=0)
    # Compute the standard error of the mean of R.
    sem = numpy.std(r_, axis=0) / numpy.sqrt(n_splits)
    
    return r, sem

