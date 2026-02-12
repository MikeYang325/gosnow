import re

resort_key = 'niseko-united'
html = '<div class="resort-card" data-region="北海道" data-snow="0" data-forecast="0" onclick="window.location.href=\'resorts/niseko-united-new.html\'">'

# Current pattern
pattern = rf'(<div class="resort-card" data-region="[^"]*" data-snow=")[^"]*(" data-forecast=")[^"]*(" onclick="window\.location\.href=\'resorts/{re.escape(resort_key)}-new\.html\'">)'

match = re.search(pattern, html)
print('Pattern:', pattern)
print('Match:', match)
if match:
    print('Groups:', match.groups())
    replacement = rf'\g<1>0.4\g<2>2.3" data-depth="280"\g<3>'
    result = re.sub(pattern, replacement, html)
    print('Result:', result)
