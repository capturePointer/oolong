import string
import itertools

from flask import Flask
from flask import request
from flask import Response
from flask import send_from_directory
from flask import render_template
import simplejson as json
from uuid import uuid4 as uuidgen

app = Flask(__name__)

md5 = {
    'zzz': 'only for test'
}

def content_genterator(s):
    count = 1
    while True:
        gen = apply(itertools.product, 
                    [string.ascii_letters for _ in range(count)])
        try:
            while True:
                yield ''.join(gen.next())
        except StopIteration:
            pass
        
        count += 1

content_maker = content_genterator(string.ascii_letters)

@app.route('/md5/task', methods=['POST'])
def _post_md5_task():
    js = {
        'id': str(uuidgen()),
        'b': [{'co': content_maker.next()}
                 for _ in range(500)]}
    return Response(json.dumps(js),
                    status=200,
                    mimetype='application/json')

@app.route('/md5/task/<id>', methods=['PUT'])
def _put_md5_task(id):
    data = json.loads(request.data)
    [md5.update({d['ci']: d['co']}) for d in data['b']]
    return Response(status=204)

@app.route('/md5/<ciph>', methods=['GET'])
def _get_md5(ciph):
    if ciph not in md5:
        return Response(status=404)
    resp = {
        'ci': ciph,
        'co': md5[ciph]}
    return Response(json.dumps(resp),
                    status=200,
                    mimetype='application/json')

@app.route('/')
def _index():
    return render_template('index.html')

@app.route('/js/<path:filename>')
def send_js(filename):
    return send_from_directory('static/js/', filename)

@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('static/css/', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
