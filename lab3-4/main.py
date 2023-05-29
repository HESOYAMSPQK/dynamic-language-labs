from flask import Flask, request, render_template
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_trig():
    if request.method == 'POST':
        angle = float(request.form['angle'])
        precision = int(request.form['precision'])
        unit = request.form['unit']

        if unit == 'degrees':
            angle_rad = math.radians(angle) # Перевод угла в радианы, если выбраны градусы
        else:
            angle_rad = angle

        # Расчет тригонометрических значений
        sin_value = round(math.sin(angle_rad), precision)
        cos_value = round(math.cos(angle_rad), precision)
        tan_value = round(math.tan(angle_rad), precision)

        return render_template('result.html', sin_value=sin_value, cos_value=cos_value, tan_value=tan_value)   # Отображение результатов на странице result.html

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
