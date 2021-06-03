''' This is for list data that is stored in constants and used for Testing'''


PARA_DISPLAY_OUTPUT_DATA_FOR_TESTING = {
    'paragraphs': [
        {
            'id': 'first',
            'references': '<a href="https://literature.org/" target="_blank">literature</a><br>',
            'subtitle': 'Fiction',
            'subtitle_note': '* Note - only public domain for listening to fall asleep.',
            'image_path': '',
            'image_classes': 'default',
            'image_alt': '',
            'text': '<p>Fiction is my number one non-domestic animal  love.  My '
                    'favorite animal is Rick.  He shares my love of fiction.</p>',
            'slug': 'fiction',
            'short_title': 'fiction',
        },
        {
            'id': 'second',
            'references': '<a href="https://gymcastic.com/" '
                          'target="_blank">JessicaSpencerKensley</a><br>',
            'subtitle': 'A sometimes wonderful, but often annoying podcast',
            'subtitle_note': '',
            'image_path': '',
            'image_info_key': 'default',
            'text': '<p>Jessica, Spencer and Kensley are fun to listen to. Jessica '
                    'and Spencer can be annoying, but Kensley rarely is. But like '
                    'the way I feel about my cats,  I  like them all equally in spite '
                    'of their natures.</p>',
            'slug': 'fiction',
            'short_title': 'fiction',
        }],
    'title': 'Listening',
    'title_note': '*Note - subjects I listen to',
    'group_type': ''
}

PARA_DISPLAY_INPUT_DATA_FOR_TESTING = {
    'group': {
        'group_title': 'Listening',
        'group_note': '*Note - subjects I listen to',
        'group_type': '',
    },
    'references': [{
        'link_text': 'Literature',
        'url': 'https://literature.org/',
        'short_text': 'lit',
        'slug': 'literature',
    }, {
        'link_text': 'JessicaSpencerKensley',
        'url': 'https://gymcastic.com/',
        'short_text': 'jessspencerkensley',
        'slug': 'tired_of_this_podcast',

    }],
    'paragraphs': [{
        'id': 'first',
        'subtitle': 'Fiction',
        'note': '* Note - only public domain for listening to fall asleep.',
        'image_path': '',
        'image_classes': 'default',
        'image_alt': '',
        'text': '<p>Fiction is my number one non-domestic animal love.  My favorite animal is '
                'Rick. He shares my love of fiction.</p>',
        'order': 'fiction',
        'slug': 'fiction',
        'short_title': 'fiction',
    }, {
        'id': 'second',
        'subtitle': 'A sometimes wonderful, but often annoying podcast',
        'note': '',
        'image_path': '',
        'image_classes': 'default',
        'image_alt': '',
        'text': '<p>Jessica, Spencer and Kensley are fun to listen to. Jessica '
                'and Spencer can be annoying, but Kensley rarely is. But like '
                'the way I feel about my cats,  I like them all equally in '
                'spite of their natures.</p>',
        'order': 'a sometimes wonderful, but often annoying podcast',
        'slug': 'a-sometimes-wonderful-but-often-annoying-podcast',
        'short_title': 'Annnoying Podcast',

    }],
    'para_id_to_link_text': {
        'first': ['Literature'],
        'second': ['JessicaSpencerKensley']
    },
    'slug_to_lookup_link': {},
}

PARA_DISPLAY_DB_INPUT_DATA_FOR_TESTING = {
    'group_title': 'Listening',
    'group_note': '*Note - subjects I listen to',
    'group_type': '',
    'paragraphs': [{
        'paragraph_id': 'first',
        'subtitle': 'Fiction',
        'subtitle_note': '* Note - only public domain for listening to fall asleep.',
        'image_path': '',
        'image_classes': 'default',
        'image_alt': '',
        'text': '<p>Fiction is my number one non-domestic animal  love.  My '
                'favorite animal is Rick.  He shares my love of fiction.</p>',
        'order': 'fiction',
        'reference_id': 'books',
        'link_text': 'Literature',
        'url': 'https://literature.org/',
        'slug': 'literature',
        'short_title': 'lit',
    }, {
        'paragraph_id': 'second',
        'subtitle': 'A sometimes wonderful, but often annoying podcast',
        'subtitle_note': '',
        'image_path': '',
        'image_classes': 'default',
        'image_alt': '',
        'text': '<p>Jessica, Spencer and Kensley are fun to listen to. Jessica and Spencer can be '
                'annoying, but Kensley rarely is. But like the way I feel about my cats, '
                'I  like them all equally in spite of their natures.</p>',
        'order': 'a sometimes wonderful, but often annoying podcast',
        'reference_id': 'gym',
        'link_text': 'JessicaSpencerKensley',
        'url': 'https://gymcastic.com/',
        'short_title': 'jessspencerkensley',
        'slug': 'tired_of_this_podcast',
    }],
}

PARA_DISPLAY_ONE_PARA_INPUT = {
    'group': {
        'group_title': 'standalone para',
        'group_note': '',
        'group_type': ''
    },
    'references': [{
        'link_text': 'AWS_CloudFront_Latest_on20210111_UpdatingExistingObjects',
        'url': 'https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/UpdatingExistingObjects.html',
        'short_text': 'Cloudfront Update Existing',
        'slug': 'aws_cloudfront_latest_on20210111_updatingexistingobjects'
    }],
    'paragraphs': [{
        'id': 180,
        'subtitle': 'S3 Caching Strategy',
        'note': '',
        'text': "<p>Caching is generally a wonderful way to make your site faster. Here are two methods for caching that are easily implemented: </p> <ol> <li>Using cache-control headers. In my Django settings, I have the following: <pre><code>AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}</code></pre> This makes it so the maximum time the browser will cache the |beg|aws-simple-storage-service|end| object added through boto3 is for 24 hours (86,400 seconds). You can also set this in the AWS console.</li> <li>Setting cache behavior in Cloudfront. For the most part, I just took the defaults, which gives me 24 hour caching.</li> </ol> <p>Caching is wonderful when your files don't change, but right after I installed |beg|cloudfront|end|, I experienced its downside. My javascript changes did not show up and clearing my browser cache did nothing. So I renamed my file and all was ok. My thoughts were what a pain, but research showed me that this was one of the recommended solutions: |beg_ref|aws_cloudfront_latest_on20210111_updatingexistingobjects|end_ref|. </p> <p>After some experimentation, decided to go with the recommended solution.  But first, it was necessary to eliminate the pain points.</p><p>Created a script that does the following: <ol><li>Compress the SCSS to CSS</li><li>Rename the css and/or js file by adding the epoch date (for versioning)</li><li>Leave the originally named files in the originals folder, in order to use git for tracking the changes</li><li>Update the html common code with the versioned filename</li><li>Upload all the newly versioned files, plus any new images, to S3</li><li>|beg_group|what-are-the-facts|end_group|</li></ol>",
        'image_path': '',
        'image_classes': 'default',
        'image_alt': '',
        'slug': 's3-caching-strategy',
        'short_title': 'S3 Caching Strategy',
        'order': 's3 caching strategy'
    }],
    'para_id_to_link_text': {
        180: ['AWS_CloudFront_Latest_on20210111_UpdatingExistingObjects']
    },
    'slug_to_lookup_link': {
        'para_slug_to_short_title': {
            'aws-simple-storage-service': 'S3',
            'cloudfront': 'Cloudfront'
        },
        'ref_slug_to_reference': {
            'aws_cloudfront_latest_on20210111_updatingexistingobjects': {
                'link_text': 'Cloudfront Update Existing',
                'url': 'https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/UpdatingExistingObjects.html'
            },
        },
        'group_slug_to_short_name': {
            'what-are-the-facts': 'Facts?',
        },
    }
}

LIST_OF_SIMILAR_DICTIONARIES = [
    {'name': 'Nemo', 'color': 'black', 'sex': 'female', 'birth_year': 1964},
    {'name': 'Sammy', 'color': 'orange and white', 'sex': 'female', 'birth_year': 1994},
    {'name': 'Mac', 'color': 'orange', 'sex': 'male', 'birth_year': 1994},
    {'name': 'Ninja', 'color': 'black', 'sex': 'female', 'birth_year': 2017},
    {'name': 'Ronin', 'color': 'orange and white', 'sex': 'male', 'birth_year': 2017}
]

LIST_OF_DIFFERENT_DICTIONARIES = [
    {'name': 'Nemo', 'color': 'black', 'sex': 'female', 'birth_year': 1964},
    {'name': 'Sammy', 'color': 'orange and white', 'sex': 'female', 'birth_year': 1994},
    {'name': 'Mac', 'color': 'orange', 'sex': 'male', 'birth_year': 1994},
    {'name': 'Ninja', 'color': 'black', 'sex': 'female', 'birth_year': 2017, 'alive': True},
    {'name': 'Ronin', 'color': 'orange and white', 'sex': 'male', 'birth_year': 2017, 'alive': True}
]
