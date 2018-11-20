def print_progressbar ( iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█' ):
    """ 
    prints a progress bar 
    from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    percent = ( "{0:." + str( decimals ) + "f}" ).format( 100 * ( iteration / float( total ) ) )
    filledLength = int( length * iteration // total )
    bar = fill * filledLength + '-' * ( length - filledLength )
    print( '\r%s |%s| %s%% %s' % ( prefix, bar, percent, suffix ), end = '\r' )

    if iteration == total: 
        print()