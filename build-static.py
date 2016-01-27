#!/usr/bin/env python

import jinja2
import json
import markdown
import os

current_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(current_path, './templates/index.html')
output_path = os.path.join(current_path, './static/index.html')
spec_path = os.path.join(current_path, './spec.json')

json_str = json.load(open(spec_path))
index_str = open(template_path, 'r').read().decode('utf-8')

md = markdown.Markdown(extensions=['meta'])
env = jinja2.Environment()
env.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
env.filters['jsonstring'] = lambda data: json.dumps(data)
env.filters['responsestring'] = lambda data: json.dumps(data) if isinstance(data, dict) else data

rendered = env.from_string(index_str).render(json_str)
open(output_path, 'w').write(rendered.encode('utf-8'))
