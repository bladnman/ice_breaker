from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
  name = request.form['name']
  person_intel, twitter_pic_url = ice_break(name=name)
  return jsonify(
    {
      'name': name,
      'picture_url': twitter_pic_url,
      "summary": person_intel.summary,
      "facts": person_intel.facts,
      "interests": person_intel.topics_of_interest,
      "ice_breakers": person_intel.ice_breakers,
    }
  )


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=3131, debug=True)
