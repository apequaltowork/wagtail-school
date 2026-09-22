"""
Page copy for the demo site, as simple block descriptors that
seed_demo turns into StreamField data.

    ('heading', text[, size])
    ('paragraph', html)            -- [[slug|text]] becomes an internal page link
    ('image', banner_key, caption, alt_text)
    ('quote', text, attribution)
    ('cta', heading, text, page_slug, button_label)
    ('document', document_key, label)
    ('table', rows)                -- first row is the header
"""

HOME = {
    'hero_title': 'Curious minds. Kind hearts. Capable hands.',
    'hero_intro': (
        'An independent, co-educational Kindergarten to Year 12 school on the Kestrel Ridge '
        'escarpment, where every student is known, challenged and cared for.'
    ),
    'hero_image': 'campus',
    'cta_page': 'enrolment-enquiry',
    'cta_label': 'Enquire about enrolment',
    'quick_links': [
        ('Enrol with us', 'Places, tours and how to apply', 'admissions'),
        ('Upcoming events', 'Open mornings, concerts and carnivals', 'events'),
        ('Learning', 'From Kindergarten to the HSC', 'learning'),
        ('Contact us', 'Phone, email and how to find us', 'contact-us'),
    ],
    'body': [
        ('heading', 'Welcome to Kestrel Ridge'),
        ('paragraph',
         '<p>For more than sixty years, Kestrel Ridge College has offered a warm, rigorous education to '
         'families across the ridge and the valley below. We are big enough to offer a wide curriculum and '
         'more than forty co-curricular activities, and small enough that every teacher knows every '
         'student by name.</p>'
         '<p>Read the [[principals-welcome|Principal\'s welcome]], explore our '
         '[[junior-school|Junior School]] and [[senior-school|Senior School]], or come and see us in person '
         'at our next Open Morning.</p>'),
        ('quote',
         'We want every student to leave Kestrel Ridge knowing how to learn, how to care for others, and '
         'how to stand up for what is right.',
         'Dr Miriam Okonkwo-Hale, Principal'),
        ('cta', 'Visit us at an Open Morning',
         'Tour the College with our student guides and meet the teachers who will know your child.',
         'events', 'See upcoming events'),
    ],
}

STANDARD_PAGES = [
    # (parent slug or None for home, slug, title, show_in_menus, banner key, intro, body)
    (None, 'about', 'About', True, 'grounds',
     'Kestrel Ridge College is an independent, co-educational school for students from Kindergarten '
     'to Year 12.',
     [
         ('paragraph',
          '<p>The College sits on twenty hectares of bushland on the edge of the Kestrel Ridge escarpment. '
          'Around 1,100 students learn across two schools: the Junior School (Kindergarten to Year 6) '
          'and the Senior School (Years 7 to 12).</p>'
          '<p>We are a not-for-profit school governed by the Kestrel Ridge Education Society, a board of '
          'parents, former students and community members.</p>'),
         ('heading', 'At a glance'),
         ('table', [
             ['', 'Junior School', 'Senior School'],
             ['Year levels', 'Kindergarten to Year 6', 'Years 7 to 12'],
             ['Students', 'Around 420', 'Around 680'],
             ['Average class size', '22', '24 (Years 7-10), 16 (Years 11-12)'],
             ['School day', '8:40 am to 3:10 pm', '8:30 am to 3:20 pm'],
         ]),
         ('image', 'grounds', 'The eucalypt walk links the Junior and Senior Schools.',
          'A path through tall gum trees on the school grounds'),
     ]),
    ('about', 'principals-welcome', "Principal's Welcome", True, 'pattern',
     'A letter from our Principal, Dr Miriam Okonkwo-Hale.',
     [
         ('paragraph',
          '<p>Dear families,</p>'
          '<p>Thank you for your interest in Kestrel Ridge College. Choosing a school is one of the most '
          'important decisions a family makes, and I hope these pages give you a real sense of who we '
          'are.</p>'
          '<p>Our students are curious. They ask good questions and they are not afraid to get things '
          'wrong on the way to getting them right. Our teachers are experts in their subjects, but more '
          'than that, they are experts in young people. They notice when a student is ready for a '
          'challenge, and they notice when a student needs a quiet word of encouragement.</p>'
          '<p>We are also a school that looks outward. Our students plant trees along Ridgeway Creek, '
          'volunteer at the community pantry, perform for local aged-care residents and compete against '
          'schools across the state.</p>'
          '<p>The best way to understand Kestrel Ridge is to visit. I would be delighted to welcome you at '
          'one of our Open Mornings, or you can [[enrolment-enquiry|make an enquiry]] and our Registrar '
          'will arrange a personal tour.</p>'
          '<p>Warm regards,</p>'
          '<p><b>Dr Miriam Okonkwo-Hale</b><br/>Principal</p>'),
     ]),
    ('about', 'our-history', 'Our History', True, 'campus',
     'From a single weatherboard classroom in 1962 to a Kindergarten to Year 12 school of 1,100 students.',
     [
         ('paragraph',
          '<p>Kestrel Ridge College was founded in 1962 by a group of local families who wanted a '
          'co-educational school close to home. The first 38 students met in a weatherboard hall on '
          'Ridgeway Drive, taught by two teachers and a part-time music master.</p>'),
         ('heading', '1962 to 1979: Early years', 'h3'),
         ('paragraph',
          '<p>The Ridgeway Building, with its clock tower, opened in 1966. By 1975 the College had grown '
          'to 400 students and its first Year 12 class sat the Higher School Certificate.</p>'),
         ('heading', '1980 to 1999: A Kindergarten to Year 12 school', 'h3'),
         ('paragraph',
          '<p>The Junior School opened in 1988, making Kestrel Ridge a Kindergarten to Year 12 school. '
          'The Great Hall followed in 1994, built largely with funds raised by the Parents and Friends '
          'Association.</p>'),
         ('heading', '2000 to today', 'h3'),
         ('paragraph',
          '<p>The Performing Arts Centre opened in 2003 and the Science Centre in 2011. In 2019 the '
          'Fairweather Library was renovated as a light-filled learning commons, named for the College\'s '
          'first librarian.</p>'),
         ('image', 'campus', 'The Ridgeway Building has been the heart of the College since 1966.',
          'An illustration of the Ridgeway Building with its clock tower at dusk'),
     ]),
    ('about', 'vision-and-values', 'Vision & Values', True, 'grounds',
     'Our vision is for every student to become a curious, kind and capable young adult.',
     [
         ('paragraph',
          '<p>Four values guide everything we do, from the classroom to the sports field.</p>'),
         ('heading', 'Curiosity', 'h3'),
         ('paragraph', '<p>We ask questions, look for evidence and enjoy learning for its own sake.</p>'),
         ('heading', 'Kindness', 'h3'),
         ('paragraph', '<p>We treat others with respect, include people and look after one another.</p>'),
         ('heading', 'Courage', 'h3'),
         ('paragraph', '<p>We try new things, speak up for what is right and learn from our mistakes.</p>'),
         ('heading', 'Community', 'h3'),
         ('paragraph', '<p>We belong to something bigger than ourselves, and we give back to it.</p>'),
         ('quote', 'Be curious, be kind, be brave, belong.', 'The College motto'),
     ]),
    (None, 'admissions', 'Admissions', True, 'pattern',
     'We welcome enquiries for every year level from Kindergarten to Year 12.',
     [
         ('heading', 'How to apply'),
         ('paragraph',
          '<ol><li>Make an [[enrolment-enquiry|enrolment enquiry]] online or call our Registrar.</li>'
          '<li>Attend an Open Morning or book a personal tour.</li>'
          '<li>Complete the application form and pay the application fee.</li>'
          '<li>Your child is invited to a friendly interview with the Head of School.</li>'
          '<li>We make offers in writing. Accept your place by paying the enrolment deposit.</li></ol>'),
         ('paragraph',
          '<p>Main entry points are Kindergarten, Year 5 and Year 7, but places do become available in '
          'other years. Siblings of current students are given priority.</p>'),
         ('document', 'enrolment_pack', 'Download the Enrolment Information Pack'),
         ('document', 'term_dates', 'Term dates for this year'),
         ('cta', 'Ready to take the next step?',
          'Tell us a little about your family and our Registrar will be in touch within two school days.',
          'enrolment-enquiry', 'Make an enquiry'),
     ]),
    ('admissions', 'fees-and-scholarships', 'Fees & Scholarships', True, 'pattern',
     'Tuition fees for this year, along with the scholarships and bursaries we offer.',
     [
         ('heading', 'Tuition fees'),
         ('paragraph',
          '<p>All amounts are fictional and include GST where it applies. Fees can be paid each term, '
          'each month or once a year.</p>'),
         ('table', [
             ['Year level', 'Annual tuition', 'Per term', 'Building levy'],
             ['Kindergarten to Year 2', '$11,480', '$2,870', '$600'],
             ['Year 3 to Year 6', '$13,960', '$3,490', '$600'],
             ['Year 7 to Year 10', '$19,720', '$4,930', '$900'],
             ['Year 11 to Year 12', '$22,160', '$5,540', '$900'],
         ]),
         ('heading', 'Other costs', 'h3'),
         ('paragraph',
          '<p>An application fee of $150 is payable with each application, and an enrolment deposit of '
          '$1,500 secures a place. The deposit is refunded when your child leaves the College. Uniforms, '
          'camps and some excursions are charged separately.</p>'),
         ('document', 'uniform', 'Uniform Price List'),
         ('heading', 'Scholarships and bursaries'),
         ('paragraph',
          '<p>Academic, music and all-rounder scholarships of up to 50% of tuition are offered for entry '
          'to Years 7 and 10. Means-tested bursaries are available at every year level for families who '
          'would otherwise be unable to afford a Kestrel Ridge education.</p>'
          '<p>Applications for next year\'s scholarships open in Term 1. Contact the Registrar for '
          'details.</p>'),
     ]),
    (None, 'learning', 'Learning', True, 'library',
     'A broad, challenging curriculum from Kindergarten to the Higher School Certificate.',
     [
         ('paragraph',
          '<p>Learning at Kestrel Ridge follows the NSW curriculum, taught by specialist teachers who '
          'bring their subjects to life. Students build strong foundations in literacy and numeracy, then '
          'go deeper with every year.</p>'),
         ('paragraph',
          '<p>Explore the [[junior-school|Junior School]], the [[senior-school|Senior School]], our '
          '[[co-curricular|co-curricular program]] and how we look after [[wellbeing|student '
          'wellbeing]].</p>'),
     ]),
    ('learning', 'junior-school', 'Junior School', True, 'library',
     'Kindergarten to Year 6: a joyful, secure start to school.',
     [
         ('paragraph',
          '<p>The Junior School has its own buildings, playgrounds and library, and around 420 students. '
          'Each class has a home teacher, supported by specialists in music, visual arts, physical '
          'education, languages and library.</p>'),
         ('heading', 'What students learn'),
         ('paragraph',
          '<ul><li><b>English and Mathematics</b> every day, with small-group support and extension.</li>'
          '<li><b>Science and Technology</b>, including coding from Year 3.</li>'
          '<li><b>History and Geography</b>, with local studies of the ridge and the creek.</li>'
          '<li><b>French</b> from Kindergarten.</li>'
          '<li><b>Creative Arts</b>: music, drama, dance and visual arts.</li></ul>'),
         ('heading', 'Outdoor learning'),
         ('paragraph',
          '<p>Every class spends at least two days a term learning in the College\'s bushland reserve, '
          'measuring trees, writing poetry and tracking the birds that give the ridge its name.</p>'),
         ('image', 'library', 'Every Junior School class visits the library each week.',
          'Colourful books on library shelves'),
     ]),
    ('learning', 'senior-school', 'Senior School', True, 'library',
     'Years 7 to 12: depth, choice and preparation for life after school.',
     [
         ('paragraph',
          '<p>In Years 7 and 8 students study a broad core of subjects and try electives across the '
          'arts, technology and languages. From Year 9 they choose electives, and in Years 11 and 12 '
          'they follow a Higher School Certificate pattern built around their strengths and goals.</p>'),
         ('heading', 'Subjects offered in Years 11 and 12'),
         ('table', [
             ['Area', 'Subjects'],
             ['English', 'English Advanced, English Standard, Extension 1 and 2'],
             ['Mathematics', 'Standard, Advanced, Extension 1 and 2'],
             ['Science', 'Biology, Chemistry, Physics, Earth and Environmental Science'],
             ['HASS', 'Modern History, Ancient History, Geography, Economics, Legal Studies, Business Studies'],
             ['Arts', 'Music 1 and 2, Visual Arts, Drama'],
             ['Languages', 'French Continuers, Japanese Continuers'],
             ['Other', 'PDHPE, Design and Technology, Software Engineering'],
         ]),
         ('heading', 'Careers and pathways'),
         ('paragraph',
          '<p>Our careers adviser meets every student in Years 10, 11 and 12. Students take part in '
          'work experience in Year 10 and university visits in Year 11.</p>'),
     ]),
    ('learning', 'co-curricular', 'Co-curricular', True, 'stage',
     'More than forty clubs, teams and ensembles, before school, at lunchtime and after school.',
     [
         ('heading', 'Sport'),
         ('paragraph',
          '<p>Students can play in eleven sports, including football, netball, basketball, hockey, '
          'cricket, tennis, rowing and cross country. Every student also competes for one of the four '
          'houses in the swimming, athletics and cross-country carnivals.</p>'),
         ('heading', 'Music'),
         ('paragraph',
          '<p>Around a third of our students learn an instrument. Ensembles include the concert band, '
          'string ensemble, jazz band, Junior School choir, Senior choir and a chamber choir.</p>'),
         ('image', 'stage', 'The Performing Arts Centre seats 480.',
          'Stage lights shining on music stands in an empty theatre'),
         ('heading', 'Debating and public speaking'),
         ('paragraph',
          '<p>Teams from Year 5 to Year 12 compete in regional debating competitions, and our senior '
          'students take part in mock trial and model United Nations.</p>'),
         ('heading', 'Robotics and coding'),
         ('paragraph',
          '<p>The robotics club meets twice a week in the Science Centre. Teams design, build and '
          'program robots for state and regional challenges.</p>'),
     ]),
    ('learning', 'wellbeing', 'Wellbeing', True, 'grounds',
     'Students learn best when they feel safe, known and supported.',
     [
         ('paragraph',
          '<p>Every student belongs to a pastoral care group that meets each morning with the same '
          'teacher for several years. Heads of Year, the College counsellor and our chaplaincy team work '
          'together to support students and families.</p>'),
         ('heading', 'Our program'),
         ('paragraph',
          '<ul><li><b>Peer support</b>: Year 11 leaders mentor every new Year 7 student.</li>'
          '<li><b>Positive education</b> lessons each fortnight, from Kindergarten to Year 10.</li>'
          '<li><b>Digital wellbeing</b> workshops for students and parents.</li>'
          '<li><b>Counselling</b>, available to any student, confidentially.</li></ul>'),
         ('quote',
          'The small things matter most: a teacher who says hello by name, a friend who saves you a seat.',
          'Year 8 student'),
     ]),
]

EVENT_INDEX = {
    'title': 'Events',
    'slug': 'events',
    'intro': '<p>Open mornings, concerts, carnivals and community days. Families are always welcome.</p>',
}

STAFF_INDEX = {
    'title': 'Our Staff',
    'slug': 'our-staff',
    'intro': '<p>Meet some of the teachers and staff who make Kestrel Ridge College what it is.</p>',
}

ENQUIRY_PAGE = {
    'parent': 'admissions',
    'title': 'Enrolment Enquiry',
    'slug': 'enrolment-enquiry',
    'intro': (
        '<p>Tell us a little about your family and our Registrar will contact you within two school '
        'days to answer your questions and arrange a tour.</p>'
    ),
    'thank_you_text': (
        '<p>Thank you for your enquiry. Our Registrar will be in touch within two school days.</p>'
        '<p>In the meantime, you might like to read about our [[fees-and-scholarships|fees and '
        'scholarships]].</p>'
    ),
    'to_address': 'admissions@kestrelridge.example',
    'from_address': 'website@kestrelridge.example',
    'subject': 'New enrolment enquiry',
}

CONTACT_PAGE = {
    'title': 'Contact Us',
    'slug': 'contact-us',
    'intro': '<p>Send us a message and the right person will reply within two school days.</p>',
    'thank_you_text': '<p>Thank you for getting in touch. We will reply within two school days.</p>',
    'to_address': 'enquiries@kestrelridge.example',
    'from_address': 'website@kestrelridge.example',
    'subject': 'Website contact form',
}
