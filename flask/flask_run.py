from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    name = "Hello World"
    return name

@app.route('/slack/events', methods=["POST"])
def slack_event_subscription():
    request_data = request.get_json()
    challenge_param = request_data['challenge']
    #print("received"+str(challenge_param))
    return '''
            "challenge": {}
            '''.format(challenge_param)


@app.route('/db')
def database():

    #db setting
    db = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='testdb',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
        )

    cur = db.cursor()
    sql = "select * from members"
    cur.execute(sql)
    members = cur.fetchall()

    cur.close()
    db.close()

    #return name
    return render_template('hello.html', title='flask test', members=members)

if __name__ == "__main__":
    app.run(debug=True, port=5000)