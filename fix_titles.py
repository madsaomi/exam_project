import os
import glob
import re

files = glob.glob('templates/staff/*_form.html') + ['templates/staff/confirm_delete.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('{% block title %}{{ title }}{% endblock %}', '{% block title %}{{ title_key }}{% endblock %}')
    content = re.sub(r'(<h1[^>]*)>{{ title }}</h1>', r'\1 data-i18n="{{ title_key }}"></h1>', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
