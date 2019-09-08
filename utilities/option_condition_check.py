import optparse

def check_option_condition(parser, options, args):
    """
        Check optparse parameter condition
        parser: OptionParser class
        options: option parsed from parser
        args: additional argument
    """
    parser.check_required("-o")
    if options.option == 'liste':
        parser.check_required("-l")
        parser.check_required("-u")

    elif options.option == 'latlng':
        parser.check_required("-d")
        parser.check_required("-u")
        parser.check_required("--latitude")
        parser.check_required("--longitude")

    elif options.option == 'bulk_latlng':
        parser.check_required("-u")
        parser.check_required("--input")
        parser.check_required("--backup")
    
    return parser