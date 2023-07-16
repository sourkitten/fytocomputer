import json
import os
import random

custom_image = ['evident']
custom_image_html = {
    "evident": '''<div style="width:100%;height:100%;background-color: black; background-image: radial-gradient(circle at 50% 50%, #492b0b, black 200%);">
		<span class="link-text">evident</span>
		</div>'''
}

def get_home_directories():
    home_directory = '/home/'
    directories = [entry for entry in os.listdir(home_directory) if os.path.isdir(os.path.join(home_directory, entry))]
    return directories


def import_internal_users():
    with open('/home/grafana/homepage-randomizer/internal-users.json', 'r') as file:
        data = json.load(file)
    usernames = data['usernames']
    return usernames


def get_user_list():
    users = [user for user in get_home_directories() if user not in import_internal_users()]
    random.shuffle(users)
    return users

def create_html_file(user_list):
    html_content = '''<meta http-equiv="content-type" content="text/html; charset=ISO-8859-7">
        <title>
                        Fytocomputer
                </title>
                <link rel="icon" type="image/png" href="fyto.png">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	
	<body>
	<div class="container">'''
    
    for user in user_list:
        html_content += f'\t<a class="link" href="~{user}">\n'
        if user in custom_image:
            html_content += custom_image_html.get(user)
        else:
            html_content += f'\t\t<img class="link-image" src="~{user}/banner.jpg" alt="Get a banner kid.">\n'
        html_content += f'\t\t<span class="link-text">{user}</span>\n'
        html_content += '\t</a>\n'
    
    html_content += '''<a class="link" href="changelog">
		<img class="link-image" src="changelog/banner.jpg" alt="Fyto lol"> <!-- add class to image -->
                <span class="link-text">changelog</span> <!-- add class to text -->
	  </a>
	</div>
    </body>\n</html>'''
    return html_content


def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)


write_to_file('/var/www/html/index.html', create_html_file(get_user_list()))