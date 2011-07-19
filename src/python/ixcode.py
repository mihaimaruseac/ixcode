# IxCode - app for code spelunking :: block diagram
# Python code version of the tool

def main(filename, functions, opts, arg_err):
    """
    Entry point for this tool.

    It must return the standardized AST for each of the functions to be
    parsed. If functions is [] then all functions found in file must be
    returned, otherwise only those found in functions. Caller of this function
    is responsible for transforming this AST to a valid DOT input file and
    running dot afterwards to get the diagram.

        filename - filename to parse
        functions - list of functions to parse
        arg_err - callback for errors caused by a command line argument
        opts - user options
        --
        returns: AST for the required functions
    """
    pass

