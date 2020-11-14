# Generated by Django 3.1 on 2020-11-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0008_auto_20201114_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglanguage',
            name='language',
            field=models.CharField(choices=[('ab', 'Abkhaz'), ('aa', 'Afar'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('sq', 'Albanian'), ('am', 'Amharic'), ('ar', 'Arabic'), ('an', 'Aragonese'), ('hy', 'Armenian'), ('as', 'Assamese'), ('av', 'Avaric'), ('ae', 'Avestan'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('bm', 'Bambara'), ('ba', 'Bashkir'), ('eu', 'Basque'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bh', 'Bihari'), ('bi', 'Bislama'), ('bs', 'Bosnian'), ('br', 'Breton'), ('bg', 'Bulgarian'), ('my', 'Burmese'), ('ca', 'Catalan; Valencian'), ('ch', 'Chamorro'), ('ce', 'Chechen'), ('ny', 'Chichewa; Chewa; Nyanja'), ('zh', 'Chinese'), ('cv', 'Chuvash'), ('kw', 'Cornish'), ('co', 'Corsican'), ('cr', 'Cree'), ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'), ('dv', 'Divehi; Maldivian;'), ('nl', 'Dutch'), ('dz', 'Dzongkha'), ('en', 'English'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('ee', 'Ewe'), ('fo', 'Faroese'), ('fj', 'Fijian'), ('fi', 'Finnish'), ('fr', 'French'), ('ff', 'Fula'), ('gl', 'Galician'), ('ka', 'Georgian'), ('de', 'German'), ('el', 'Greek, Modern'), ('gn', 'Guaraní'), ('gu', 'Gujarati'), ('ht', 'Haitian'), ('ha', 'Hausa'), ('he', 'Hebrew (modern)'), ('hz', 'Herero'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('ie', 'Interlingue'), ('ga', 'Irish'), ('ig', 'Igbo'), ('ik', 'Inupiaq'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('iu', 'Inuktitut'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('kl', 'Kalaallisut'), ('kn', 'Kannada'), ('kr', 'Kanuri'), ('ks', 'Kashmiri'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('ki', 'Kikuyu, Gikuyu'), ('rw', 'Kinyarwanda'), ('ky', 'Kirghiz, Kyrgyz'), ('kv', 'Komi'), ('kg', 'Kongo'), ('ko', 'Korean'), ('ku', 'Kurdish'), ('kj', 'Kwanyama, Kuanyama'), ('la', 'Latin'), ('lb', 'Luxembourgish'), ('lg', 'Luganda'), ('li', 'Limburgish'), ('ln', 'Lingala'), ('lo', 'Lao'), ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lv', 'Latvian'), ('gv', 'Manx'), ('mk', 'Macedonian'), ('mg', 'Malagasy'), ('ms', 'Malay'), ('ml', 'Malayalam'), ('mt', 'Maltese'), ('mi', 'Māori'), ('mr', 'Marathi (Marāṭhī)'), ('mh', 'Marshallese'), ('mn', 'Mongolian'), ('na', 'Nauru'), ('nv', 'Navajo, Navaho'), ('nb', 'Norwegian Bokmål'), ('nd', 'North Ndebele'), ('ne', 'Nepali'), ('ng', 'Ndonga'), ('nn', 'Norwegian Nynorsk'), ('no', 'Norwegian'), ('ii', 'Nuosu'), ('nr', 'South Ndebele'), ('oc', 'Occitan'), ('oj', 'Ojibwe, Ojibwa'), ('cu', 'Old Church Slavonic'), ('om', 'Oromo'), ('or', 'Oriya'), ('os', 'Ossetian, Ossetic'), ('pa', 'Panjabi, Punjabi'), ('pi', 'Pāli'), ('fa', 'Persian'), ('pl', 'Polish'), ('ps', 'Pashto, Pushto'), ('pt', 'Portuguese'), ('qu', 'Quechua'), ('rm', 'Romansh'), ('rn', 'Kirundi'), ('ro', 'Romanian, Moldavan'), ('ru', 'Russian'), ('sa', 'Sanskrit (Saṁskṛta)'), ('sc', 'Sardinian'), ('sd', 'Sindhi'), ('se', 'Northern Sami'), ('sm', 'Samoan'), ('sg', 'Sango'), ('sr', 'Serbian'), ('gd', 'Scottish Gaelic'), ('sn', 'Shona'), ('si', 'Sinhala, Sinhalese'), ('sk', 'Slovak'), ('sl', 'Slovene'), ('so', 'Somali'), ('st', 'Southern Sotho'), ('es', 'Spanish; Castilian'), ('su', 'Sundanese'), ('sw', 'Swahili'), ('ss', 'Swati'), ('sv', 'Swedish'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('ti', 'Tigrinya'), ('bo', 'Tibetan'), ('tk', 'Turkmen'), ('tl', 'Tagalog'), ('tn', 'Tswana'), ('to', 'Tonga'), ('tr', 'Turkish'), ('ts', 'Tsonga'), ('tt', 'Tatar'), ('tw', 'Twi'), ('ty', 'Tahitian'), ('ug', 'Uighur, Uyghur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('cy', 'Welsh'), ('wo', 'Wolof'), ('fy', 'Western Frisian'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang, Chuang'), ('zu', 'Zulu')], max_length=2),
        ),
        migrations.AlterField(
            model_name='blogspecialization',
            name='specialization',
            field=models.CharField(choices=[('TECH', 'Tech'), ('FUN CONTENT', 'Fun content'), ('BEAUTY', 'Beauty'), ('TRAVEL', 'Travel'), ('KIDS', 'Kids'), ('SPORT', 'Sport'), ('HUMOR', 'Humor'), ('SOCIETY', 'Society'), ('BUSINESS/FINANCES', 'Business/Finances'), ('DESIGN', 'Design'), ('VIDEO GAMES', 'Video games'), ('ANIMALS', 'Animals'), ('IT', 'IT'), ('CREATIVITY', 'Creativity'), ('FOOD/DRINKS', 'Food/Drinks'), ('LIFESTYLE', 'Lifestyle'), ('MUSIC/MOVIES', 'Music/Movies'), ('EDUCATION', 'Education'), ('HEALTH', 'Health'), ('WEB-SITES/APPLICATIONS', 'Web-sites/Applications'), ('AUTO/MOTO', 'Auto/Moto'), ('BOOKS', 'Books'), ('HOUSE/RENOVATION', 'House/Renovation')], max_length=100),
        ),
    ]
