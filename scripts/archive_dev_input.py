'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Archive dev input
'''
import sys
import utilities.random_methods as utils


def run(*args):
    '''
        Usage:
        Three possibilities: 1. Archive all input data files.  2. Exclude files that
        have not been moved to the done directory.  3. Exclude files used to update production

        Run with default before you run db_update_s1 with the for_prod argument.   Think about this
        if you need to delete associations.  That is the only thing needed to update production
        that can not be created by db_update_s1

        The default (no script args), archives the input files that have not been
        removed to the done folder and the production input files.

        >>> python manage.py runscript -v3 s3_updater --script-args
        or
        >>> python manage.py runscript -v3 archive_dev_input --script-args exclude_not_done
        or
        >>> python manage.py runscript -v3 archive_dev_input --script-args exclude_prod

    '''
    params = {}

    for arg in args:
        params[arg] = True

    num_processed = utils.archive_files_from_input_directories(**params)

    sys.exit(f'After looping through input files (args=={args}), {num_processed} files were moved.')
