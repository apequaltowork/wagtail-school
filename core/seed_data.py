"""
Hand-written demo content for Kestrel Ridge College.

Everything here is fictional: the school, the suburb, the people and the numbers.
Phone numbers use the ranges ACMA sets aside for fiction; email addresses use
the reserved .example domain.

This module is plain data (no Django imports) so the asset generator in
seed/make_assets.py can read the staff list too.
"""

SCHOOL = {
    'school_name': 'Kestrel Ridge College',
    'address': '1 Ridgeway Drive\nKestrel Ridge NSW 2799\nAustralia',
    'phone': '(02) 5550 1962',
    'email': 'enquiries@kestrelridge.example',
    'office_hours': 'Monday to Friday, 8:00 am to 4:30 pm\nClosed on public holidays',
    'map_embed_url': (
        'https://www.openstreetmap.org/export/embed.html'
        '?bbox=148.6%2C-33.6%2C149.8%2C-32.9&layer=mapnik'
    ),
    'facebook_url': 'https://www.facebook.com/kestrelridge.example',
    'instagram_url': 'https://www.instagram.com/kestrelridge.example',
    'youtube_url': 'https://www.youtube.com/c/kestrelridge-example',
    'linkedin_url': 'https://www.linkedin.com/school/kestrelridge-example',
    'footer_text': (
        'An independent, co-educational Kindergarten to Year 12 school on the edge of '
        'the Kestrel Ridge escarpment, educating curious, kind and capable young people since 1962.'
    ),
}

# ---------------------------------------------------------------------------
# Images and documents (files live in seed/assets/)
# ---------------------------------------------------------------------------

BANNERS = [
    # key, filename, title
    ('campus', 'banner-campus.jpg', 'The Ridgeway Building at dusk'),
    ('grounds', 'banner-grounds.jpg', 'The eucalypt walk and school grounds'),
    ('library', 'banner-library.jpg', 'Shelves in the Fairweather Library'),
    ('pattern', 'banner-pattern.jpg', 'Navy and gold geometric pattern'),
    ('sport', 'banner-sport.jpg', 'Ridgeway Oval running track'),
    ('stage', 'banner-stage.jpg', 'Performing Arts Centre stage lights'),
]

CATEGORIES = [
    # name, slug, colour, image filename
    ('Academic', 'academic', '#1c4e80', 'category-academic.jpg'),
    ('Sport', 'sport', '#2e6b30', 'category-sport.jpg'),
    ('Arts', 'arts', '#7a2e6b', 'category-arts.jpg'),
    ('Community', 'community', '#8a4b12', 'category-community.jpg'),
    ('Open Day', 'open-day', '#9c1f2e', 'category-open-day.jpg'),
]

DOCUMENTS = [
    # key, filename, title
    ('uniform', 'uniform-price-list.pdf', 'Uniform Price List'),
    ('term_dates', 'term-dates.pdf', 'Term Dates'),
    ('enrolment_pack', 'enrolment-information-pack.pdf', 'Enrolment Information Pack'),
]

# ---------------------------------------------------------------------------
# Staff
# ---------------------------------------------------------------------------

DEPARTMENTS = [
    # name, slug, order
    ('Leadership', 'leadership', 1),
    ('English', 'english', 2),
    ('Mathematics', 'mathematics', 3),
    ('Science', 'science', 4),
    ('HASS', 'hass', 5),
    ('Arts', 'arts', 6),
    ('PE & Sport', 'pe-sport', 7),
    ('Wellbeing', 'wellbeing', 8),
    ('Administration', 'administration', 9),
]

# Avatar background colours, cycled through the staff list.
AVATAR_COLOURS = ['#14284b', '#2a4574', '#8a6d12', '#1c4e80', '#2e6b30', '#7a2e6b', '#8a4b12', '#3b4a66']

STAFF = [
    {
        'first_name': 'Miriam', 'last_name': 'Okonkwo-Hale', 'role': 'Principal',
        'department': 'leadership', 'ext': '101',
        'qualifications': 'PhD (Education), MEd (Leadership), BA DipEd',
        'bio': [
            'Dr Okonkwo-Hale joined Kestrel Ridge College as Principal in 2015 after twelve years in '
            'senior leadership at independent schools in Sydney and Wellington. She began her career '
            'teaching English and History, and still teaches a Year 9 literature elective each year.',
            'Her doctoral research looked at how students build a sense of belonging in their first year '
            'of secondary school, and that work shapes the College\'s transition program today.',
        ],
    },
    {
        'first_name': 'Thomas', 'last_name': 'Brennan-Ruiz', 'role': 'Deputy Principal',
        'department': 'leadership', 'ext': '102',
        'qualifications': 'MEd (Curriculum), BSc DipEd',
        'bio': [
            'Mr Brennan-Ruiz oversees teaching and learning across the Senior School, including the HSC '
            'program and the College timetable. He is a physics teacher by training.',
            'Outside school he coaches the Year 8 mixed touch football team and is a keen amateur astronomer.',
        ],
    },
    {
        'first_name': 'Priya', 'last_name': 'Ramaswamy', 'role': 'Head of Junior School',
        'department': 'leadership', 'ext': '103',
        'qualifications': 'MEd (Early Childhood), BTeach (Primary)',
        'bio': [
            'Ms Ramaswamy leads the Junior School from Kindergarten to Year 6. She has taught every year '
            'level from Kindergarten to Year 6 and is passionate about early literacy.',
            'She introduced the Junior School\'s outdoor learning days, which take every class into the '
            'bushland reserve at least twice a term.',
        ],
    },
    {
        'first_name': 'Callum', 'last_name': 'Fraser', 'role': 'Head of English',
        'department': 'english', 'ext': '210',
        'qualifications': 'MA (Literature), BA DipEd',
        'bio': [
            'Mr Fraser has led the English faculty since 2018. He is an HSC marker and has written '
            'study guides on Australian poetry.',
            'He runs the senior debating program and the lunchtime creative writing group, "The Inkwell".',
        ],
    },
    {
        'first_name': 'Sophie', 'last_name': 'Tran', 'role': 'English Teacher',
        'department': 'english', 'ext': '211',
        'qualifications': 'BA BTeach (Secondary)',
        'bio': [
            'Ms Tran teaches English from Year 7 to Year 12 and coordinates the College\'s reading '
            'challenge for Years 7 and 8.',
            'She also manages the student newspaper, The Kestrel Courier, which publishes twice a term.',
        ],
    },
    {
        'first_name': 'Daniel', 'last_name': 'Kowalczyk', 'role': 'Head of Mathematics',
        'department': 'mathematics', 'ext': '220',
        'qualifications': 'MTeach, BSc (Mathematics)',
        'bio': [
            'Mr Kowalczyk worked as a data analyst before moving into teaching. He leads the Mathematics '
            'faculty and teaches Mathematics Extension 1 and 2.',
            'He coaches the College\'s teams in the Australian Mathematics Competition and runs a '
            'Thursday afternoon maths help desk in the library.',
        ],
    },
    {
        'first_name': 'Mei-Lin', 'last_name': 'Zhou', 'role': 'Mathematics Teacher',
        'department': 'mathematics', 'ext': '221',
        'qualifications': 'BEd (Secondary Mathematics)',
        'bio': [
            'Ms Zhou teaches Mathematics from Year 7 to Year 10 and leads the numeracy support program.',
            'She is a volunteer with the robotics club, where she helps students with the programming side '
            'of their builds.',
        ],
    },
    {
        'first_name': 'Samuel', 'last_name': 'Adeyemi', 'role': 'Head of Science',
        'department': 'science', 'ext': '230',
        'qualifications': 'PhD (Chemistry), GradDipEd',
        'bio': [
            'Dr Adeyemi spent eight years in industrial research before joining the College in 2016. He '
            'leads the Science faculty and teaches Chemistry in Years 11 and 12.',
            'Each August he organises the Science Week Showcase, where students present their '
            'independent research projects to families.',
        ],
    },
    {
        'first_name': 'Rosa', 'last_name': 'Villanueva', 'role': 'Biology and Chemistry Teacher',
        'department': 'science', 'ext': '231',
        'qualifications': 'BSc (Biology), MTeach',
        'bio': [
            'Ms Villanueva teaches Science in Years 7 to 10 and Biology in the Senior School.',
            'She looks after the College\'s native plant nursery and the water-monitoring project at '
            'Ridgeway Creek.',
        ],
    },
    {
        'first_name': 'Liam', 'last_name': 'O\'Driscoll', 'role': 'Head of HASS',
        'department': 'hass', 'ext': '240',
        'qualifications': 'MA (History), BA DipEd',
        'bio': [
            'Mr O\'Driscoll leads Humanities and Social Sciences, which covers History, Geography, '
            'Economics, Business Studies and Legal Studies.',
            'He runs the Year 10 Canberra study tour and the College\'s mock parliament.',
        ],
    },
    {
        'first_name': 'Isabelle', 'last_name': 'Moreau', 'role': 'Director of Music',
        'department': 'arts', 'ext': '250',
        'qualifications': 'MMus (Performance), BMus, GradDipEd',
        'bio': [
            'Ms Moreau leads the College\'s music program, including the concert band, string ensemble, '
            'jazz band and three choirs.',
            'She trained as a cellist and still performs with a regional chamber orchestra.',
        ],
    },
    {
        'first_name': 'Kiri', 'last_name': 'Walker-Ngata', 'role': 'Visual Arts Teacher',
        'department': 'arts', 'ext': '251',
        'qualifications': 'BFA, MTeach',
        'bio': [
            'Ms Walker-Ngata teaches Visual Arts and Photography from Year 7 to Year 12.',
            'She curates the annual Junior School Art Exhibition and the Year 12 Body of Work showcase.',
        ],
    },
    {
        'first_name': 'Marcus', 'last_name': 'Delaney', 'role': 'Director of Sport',
        'department': 'pe-sport', 'ext': '260',
        'qualifications': 'BEd (Health and Physical Education)',
        'bio': [
            'Mr Delaney coordinates the College\'s sport program, from the inter-house carnivals to '
            'representative teams in eleven sports.',
            'A former state-level rower, he started the College rowing program in 2019.',
        ],
    },
    {
        'first_name': 'Amira', 'last_name': 'Haddad', 'role': 'School Counsellor',
        'department': 'wellbeing', 'ext': '270',
        'qualifications': 'MPsych (Counselling), BA (Psychology)',
        'bio': [
            'Ms Haddad is a registered psychologist and the College counsellor. Students can book a time '
            'with her directly, or be referred by a teacher or parent.',
            'She leads the Year 7 peer support program and the parent information evenings on '
            'adolescent wellbeing.',
        ],
    },
    {
        'first_name': 'Grace', 'last_name': 'Pemberton', 'role': 'Registrar',
        'department': 'administration', 'ext': '100',
        'qualifications': 'BBus (Management)',
        'bio': [
            'Mrs Pemberton manages enrolments and is usually the first person new families meet. She '
            'arranges school tours and answers questions about places, fees and scholarships.',
            'She has worked at the College since 2009.',
        ],
    },
]

# ---------------------------------------------------------------------------
# Events — day offsets are relative to the day the seed runs
# ---------------------------------------------------------------------------

EVENTS = [
    # Upcoming
    {
        'title': 'Spring Open Morning', 'slug': 'spring-open-morning', 'category': 'open-day',
        'offset': 9, 'length': 0, 'start': '09:30', 'end': '12:30', 'location': 'Main Quadrangle',
        'summary': 'Tour the College with student guides, meet our teachers and see classes in action.',
        'body': [
            'Our Open Morning is the best way to get a feel for daily life at Kestrel Ridge. Student guides '
            'will take you through the Junior School, the science laboratories, the library and the '
            'Performing Arts Centre.',
            'The Principal will speak in the Great Hall at 10:00 am and again at 11:30 am. The Registrar '
            'will be available all morning to answer questions about enrolment.',
        ],
    },
    {
        'title': 'Senior School Information Evening', 'slug': 'senior-school-information-evening',
        'category': 'academic', 'offset': 16, 'length': 0, 'start': '18:00', 'end': '19:30',
        'location': 'Performing Arts Centre',
        'summary': 'An evening for Year 10 families about subject selection for Years 11 and 12.',
        'body': [
            'Heads of faculty will explain the subjects on offer for the Higher School Certificate and how '
            'subject choices affect university and career pathways.',
            'Students are encouraged to attend with their parents or guardians. Light refreshments will be '
            'served from 5:30 pm.',
        ],
    },
    {
        'title': 'Inter-house Athletics Carnival', 'slug': 'inter-house-athletics-carnival',
        'category': 'sport', 'offset': 23, 'length': 0, 'start': '08:30', 'end': '15:00',
        'location': 'Ridgeway Oval',
        'summary': 'Students from Years 3 to 12 compete for the four houses in track and field events.',
        'body': [
            'The carnival is a full school day. Students should wear their house colours, bring a hat, '
            'water bottle and sunscreen, and arrive at the oval by 8:15 am.',
            'Families are welcome to watch from the grandstand. The canteen will be open all day.',
        ],
    },
    {
        'title': 'Spring Music Concert', 'slug': 'spring-music-concert', 'category': 'arts',
        'offset': 30, 'length': 0, 'start': '18:30', 'end': '20:30', 'location': 'Performing Arts Centre',
        'summary': 'The concert band, string ensemble, jazz band and choirs perform their spring program.',
        'body': [
            'This year\'s program includes new Australian works for band and strings, a jazz set '
            'and a combined choir finale.',
            'Entry is free, but seats are limited. Please collect tickets from the front office.',
        ],
    },
    {
        'title': 'Year 12 Valedictory Assembly', 'slug': 'year-12-valedictory-assembly',
        'category': 'academic', 'offset': 41, 'length': 0, 'start': '10:00', 'end': '12:00',
        'location': 'Great Hall',
        'summary': 'We farewell the graduating class and celebrate their years at the College.',
        'body': [
            'The assembly includes the presentation of the Principal\'s Award, speeches from the school '
            'captains and a slideshow of the class\'s time at Kestrel Ridge.',
            'Families of Year 12 students are warmly invited. A morning tea follows in the quadrangle.',
        ],
    },
    {
        'title': 'Community Working Bee', 'slug': 'community-working-bee', 'category': 'community',
        'offset': 48, 'length': 0, 'start': '08:00', 'end': '12:00', 'location': 'Junior School playground',
        'summary': 'Help us plant, mulch and paint. Morning tea and a sausage sizzle are provided.',
        'body': [
            'Projects this term include new garden beds for the Junior School, repainting the handball '
            'courts and planting 200 native seedlings from our nursery along Ridgeway Creek.',
            'Please bring gloves and a hat. Children are welcome when accompanied by an adult.',
        ],
    },
    {
        'title': 'Junior School Art Exhibition', 'slug': 'junior-school-art-exhibition', 'category': 'arts',
        'offset': 55, 'length': 2, 'start': '15:00', 'end': '18:00', 'location': 'Fairweather Library',
        'summary': 'Artwork from every Junior School class, from Kindergarten collage to Year 6 printmaking.',
        'body': [
            'The exhibition runs for three afternoons. Each class has a wall, and students will be on hand '
            'to talk about their work.',
            'The opening on the first afternoon includes a short performance by the Junior School choir.',
        ],
    },
    {
        'title': 'Twilight Open Evening', 'slug': 'twilight-open-evening', 'category': 'open-day',
        'offset': 68, 'length': 0, 'start': '16:30', 'end': '19:00', 'location': 'Main Quadrangle',
        'summary': 'An after-work opportunity for families to tour the College and meet staff.',
        'body': [
            'The Twilight Open Evening follows the same format as our Open Morning, for families who '
            'cannot attend during the day.',
            'Tours leave from the quadrangle every fifteen minutes. The last tour departs at 6:15 pm.',
        ],
    },
    # Past
    {
        'title': 'Science Week Showcase', 'slug': 'science-week-showcase', 'category': 'academic',
        'offset': -12, 'length': 0, 'start': '15:30', 'end': '18:00', 'location': 'Science Centre',
        'summary': 'Students presented their independent research projects to families and judges.',
        'body': [
            'Over 60 students from Years 7 to 11 presented projects ranging from water quality in Ridgeway '
            'Creek to the physics of paper aeroplanes.',
            'Congratulations to the Year 9 team whose project on native bee habitats won the judges\' award.',
        ],
    },
    {
        'title': 'Grandparents\' Day', 'slug': 'grandparents-day', 'category': 'community',
        'offset': -26, 'length': 0, 'start': '09:00', 'end': '12:00', 'location': 'Junior School',
        'summary': 'Junior School students welcomed their grandparents and special friends into class.',
        'body': [
            'More than 300 grandparents and special friends joined us for classroom visits, a concert in '
            'the Great Hall and morning tea.',
            'Thank you to the Parents and Friends Association for organising the morning tea.',
        ],
    },
    {
        'title': 'Winter Sports Presentation Night', 'slug': 'winter-sports-presentation-night',
        'category': 'sport', 'offset': -40, 'length': 0, 'start': '18:00', 'end': '20:00',
        'location': 'Great Hall',
        'summary': 'We celebrated the winter season across football, netball, hockey and rugby.',
        'body': [
            'Awards were presented for best and fairest, most improved and coaches\' awards in every team.',
            'The evening closed with the announcement of the Sportsperson of the Year for the Junior and '
            'Senior Schools.',
        ],
    },
    {
        'title': 'Robotics Club Regional Challenge', 'slug': 'robotics-club-regional-challenge',
        'category': 'academic', 'offset': -61, 'length': 1, 'start': '09:00', 'end': '16:00',
        'location': 'Science Centre',
        'summary': 'Kestrel Ridge hosted twelve schools for a two-day robotics challenge.',
        'body': [
            'Teams designed, built and programmed robots to complete a series of rescue-themed tasks.',
            'Our Year 10 team placed second overall and won the award for best engineering notebook.',
        ],
    },
]

# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

YEAR_LEVELS = ['Kindergarten'] + ['Year {}'.format(n) for n in range(1, 13)]
TERMS = ['Term 1', 'Term 2', 'Term 3', 'Term 4']
HEARD_ABOUT = ['Friend or family', 'Social media', 'Open Day', 'Website', 'Other']

ENQUIRY_FIELDS = [
    # label, field_type, required, choices
    ("Parent/Guardian's full name", 'singleline', True, ''),
    ('Email address', 'email', True, ''),
    ('Phone number', 'singleline', False, ''),
    ("Student's first name", 'singleline', True, ''),
    ('Year level of entry', 'dropdown', False, ', '.join(YEAR_LEVELS)),
    ('Preferred start term', 'radio', False, ', '.join(TERMS)),
    ('Languages spoken at home (e.g. Français, Español)', 'singleline', False, ''),
    ('How did you hear about us?', 'checkboxes', False, ', '.join(HEARD_ABOUT)),
    ('Questions or comments', 'multiline', False, ''),
    ('Subscribe to our newsletter', 'checkbox', False, ''),
]

CONTACT_SUBJECTS = ['General enquiry', 'Admissions', 'Accounts', 'Events']

CONTACT_FIELDS = [
    ('Your name', 'singleline', True, ''),
    ('Email', 'email', True, ''),
    ('Subject', 'dropdown', True, ', '.join(CONTACT_SUBJECTS)),
    ('Message', 'multiline', True, ''),
]

# Ingredients for the 30 enquiry and 10 contact submissions (combined with a fixed random seed).
PARENT_FIRST_NAMES = [
    'Aisha', 'Ben', 'Chloé', 'Dimitri', 'Elena', 'Farid', 'Georgia', 'Hamish', 'Ines', 'Jarrah',
    'Keiko', 'Luca', 'Maya', 'Nikhil', 'Olivia', 'Pablo', 'Quinn', 'Rania', 'Stefan', 'Tahlia',
    'Umar', 'Vanessa', 'Wiremu', 'Xavier', 'Yasmin', 'Zoltan', 'Anh', 'Bronwyn', 'Chidi', 'Delphine',
]
PARENT_LAST_NAMES = [
    'Abernethy', 'Baptiste', 'Castellano', 'Dimitriou', 'Eastwood-Park', 'Farouk', 'Gallagher',
    'Hoang', 'Iwasaki', 'Jankowski', 'Kaur', 'Lindqvist', 'McAllister', 'Nakamura', 'Oyelaran',
    'Petrakis', 'Quintero', 'Rahimi', 'Sørensen', 'Thorne', 'Umeh', 'Valdés', 'Whitford', 'Yilmaz',
]
STUDENT_FIRST_NAMES = [
    'Amelia', 'Arlo', 'Beatrice', 'Charlie', 'Eloise', 'Felix', 'Hugo', 'Isla', 'Jasper', 'Leilani',
    'Mateo', 'Nina', 'Oscar', 'Poppy', 'Rafael', 'Saanvi', 'Theo', 'Willow', 'Zara', 'Kai',
]
LANGUAGES = [
    '', '', '', 'English', 'Français', 'Español', 'Mandarin', 'Tiếng Việt', 'Arabic', 'Greek',
    'Hindi and English', 'Português', 'Deutsch', 'Italiano', 'Te reo Māori', 'Korean',
]
ENQUIRY_COMMENTS = [
    '',
    '',
    'Could we book a tour in the next few weeks?',
    'Is there a bus service from the northern suburbs?',
    "We're relocating from Melbourne mid-year — are there places available in Term 3?",
    'Our daughter plays the violin. Could she join the string ensemble straight away?',
    'Do you offer before and after school care for the Junior School?',
    'What scholarships are available for Year 7 entry?',
    'My son has a peanut allergy. How does the canteen manage allergies?',
    'Can we meet the Head of Junior School before applying?',
    'Is there a sibling discount on tuition fees?',
    'We would like to know more about the robotics program.',
]
CONTACT_MESSAGES = [
    ('General enquiry', 'Hi, is the school pool open to the community on weekends?'),
    ('General enquiry', 'Can you tell me where to buy second-hand uniforms?'),
    ('Admissions', 'We missed the Open Morning. Is there another chance to see the school this term?'),
    ('Admissions', 'What documents do we need for the enrolment application?'),
    ('Accounts', 'Could you resend our Term 3 fee statement? The link in the email expired.'),
    ('Accounts', 'We would like to set up a monthly payment plan for tuition fees.'),
    ('Events', 'Are tickets needed for the Spring Music Concert?'),
    ('Events', 'Is there parking near Ridgeway Oval for the athletics carnival?'),
    ('General enquiry', "I'm a former student (class of 1988) — is there an alumni association?"),
    ('Events', 'Can grandparents attend the Junior School Art Exhibition?'),
]


def staff_photo_filename(member):
    return 'staff-{}-{}.jpg'.format(
        member['first_name'].lower(), member['last_name'].lower().replace("'", '')
    )
