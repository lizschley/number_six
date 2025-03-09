''' Script constants '''

# used in utilities.random methods to clear out no longer necessary data; less clutter
# Someday might reuse or rewrite, but for now this is kind of useless, since the paths don't exist
# It was easy to use and very useful, so do not want to lose
ALWAYS_ARCHIVE_INPUT_DIRECTORIES = [
                                        'data/data_for_updates/dev_input_step_three/done',
                                        'data/data_for_creates/loaded'
                                    ]
NOT_DONE_INPUT_DIRECTORIES = [
                                'data/data_for_updates/dev_input_step_three',
                                'data/data_for_creates'
                             ]

PROD_INPUT_DIRECTORY = 'data/data_for_updates/prod_input_json'
