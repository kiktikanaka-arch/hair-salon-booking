from flask import Flask, request, redirect, render_template_string
from datetime import datetime

app = Flask(__name__)

bookings = []

HTML = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ร้านทำผม</title>
<style>
body {
    font-family: Arial, sans-serif;
    background:#fff0f6;
    margin:0;
    padding:20px;
}
.container {
    max-width:600px;
    margin:auto;
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 4px 15px #ddd;
}
h1 {
    text-align:center;
    color:#d63384;
}
label {
    display:block;
    margin-top:15px;
    font-weight:bold;
}
input, select, button {
    width:100%;
    padding:12px;
    margin-top:6px;
    box-sizing:border-box;
    border-radius:10px;
    border:1px solid #ccc;
}
button {
    margin-top:20px;
    background:#d63384;
    color:white;
    border:none;
    font-size:16px;
}
.card {
    background:#fff5fa;
    padding:15px;
    margin-top:15px;
    border-radius:12px;
}
</style>
</head>

<body>
<div class="container">

<h1>💇 ร้านจองคิวทำผม</h1>

<form method="POST">

<label>ชื่อลูกค้า</label>
<input name="name" required>

<label>เบอร์โทรศัพท์</label>
<input name="phone" required>

<label>บริการ</label>
<select name="service">
<option>ตัดผม</option>
<option>สระ + ไดร์</option>
<option>ย้อมผม</option>
<option>ดัดผม</option>
<option>ทรีตเมนต์</option>
</select>

<label>ช่าง</label>
<select name="staff">
<option>ช่างคนที่ 1</option>
<option>ช่างคนที่ 2</option>
<option>ช่างคนที่ 3</option>
</select>

<label>วันที่</label>
<input type="date" name="date" required>

<label>เวลา</label>
<input type="time" name="time" required>

<button type="submit">📅 จองคิว</button>

</form>

<h2>📋 รายการจอง</h2>

{% for b in bookings %}
<div class="card">
<b>👤 {{b.name}}</b><br>
📞 {{b.phone}}<br>
💇 {{b.service}}<br>
👩‍🦰 {{b.staff}}<br>
📅 {{b.date}} เวลา {{b.time}}
</div>
{% else %}
<p>ยังไม่มีรายการจอง</p>
{% endfor %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        bookings.append({
            "name": request.form["name"],
            "phone": request.form["phone"],
            "service": request.form["service"],
            "staff": request.form["staff"],
            "date": request.form["date"],
            "time": request.form["time"],
            "created": datetime.now().isoformat()
        })
        return redirect("/")

    return render_template_string(HTML, bookings=bookings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
