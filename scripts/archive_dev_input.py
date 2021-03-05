'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Archive dev input
'''
import sys
import utilities.random_methods as utils


def run(*args):
    '''
        Usage:
        Two possibilities: 1. Archive all non-production input data files.  2. Exclude files that
        have not been moved to the done directory.

        The default, meaning no script args, archives even the input files that have not been
        removed to the done folder.  Moving dev files to done is currently a manual process, because of
        the iterative nature of editing files or in case there was an error.

        If you know there is an input file that you want to keep, just move it from the done file
        and run with the exclude_not_done argument

        I do not archive production input, since the archive directory is not on the EC2 server.

        >>> python manage.py runscript -v3 s3_updater --script-args
        or
        >>> python manage.py runscript -v3 archive_dev_input --script-args exclude_not_done
    '''
    if len(args) > 1:
        sys.exit(f'Error! Too many args {args}')

    if len(args) == 0:
        num_processed = utils.archive_files_from_input_directories()
    elif args[0] == 'exclude_not_done':
        num_processed = utils.archive_files_from_input_directories(False)
        print('Excluded input files that had not been moved to the done folder')

    if num_processed is None:
        sys.exit(f'Invalid argument: {args}.')

    sys.exit(f'After looping through the input data, {num_processed} files were moved.')
