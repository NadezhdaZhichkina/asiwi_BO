from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

SHEET_ID = "14RkrtefncVsHwnDMcWJyYvAQVn92iDRC2yRo58ila5k"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route("/save_case", methods=["POST"])
def save_case():
    data = request.json
    situation = data.get("situation")
    solution = data.get("solution", "")
    user = data.get("user", "Аноним")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if not situation:
        return jsonify({"error": "Ситуация пуста"}), 400
    
    sheet.append_row([now, user, situation, solution])
    return jsonify({"status": "Кейс успешно добавлен"})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
