from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection details (replace with your credentials)
DB_NAME = "posts"
DB_USER = "postgres"
DB_PASSWORD = "5599emoyo"
DB_HOST = "localhost"
DB_PORT = 5533


def connect_to_db():
  conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
  return conn


@app.route("/")
def get_all_posts():
  conn = connect_to_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM posts")
  posts = cur.fetchall()
  cur.close()
  conn.close()
  return render_template("index.html", posts=posts)


@app.route("/posts", methods=["POST"])
def create_post():
  conn = connect_to_db()
  cur = conn.cursor()
  title = request.json["title"]
  content = request.json["content"]
  cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
  conn.commit()
  cur.close()
  conn.close()
  return jsonify({"message": "Post created successfully!"})


@app.route("/posts/<int:post_id>")
def get_post_by_id(post_id):
  conn = connect_to_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
  post = cur.fetchone()
  cur.close()
  conn.close()
  if post is None:
    return jsonify({"message": "Post not found!"})
  return jsonify(post)


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
  conn = connect_to_db()
  cur = conn.cursor()
  title = request.json.get("title")
  content = request.json.get("content")
  cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
  conn.commit()
  cur.close()
  conn.close()
  return jsonify({"message": "Post updated successfully!"})


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
  conn = connect_to_db()
  cur = conn.cursor()
  cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
  conn.commit()
  cur.close()
  conn.close()
  return jsonify({"message": "Post deleted successfully!"})

if __name__ == "__main__":
  app.run(debug=True, port=5000)