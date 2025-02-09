import json
import urllib.parse
import webbrowser
import math
import requests

# Chart.js 구성 (Python 딕셔너리)

data1_raw = [1000000, 3000000, 4000000, 5700000,
             7700000, 8077000, 8609090, 8579090, 
             9779090, 10179090, 10432282, 10432282 + 1910000]
data2_raw = [992924, 2967439, 4029655, 6117580,
             9506232, 9876232, 10622363, 10674526,
             11818529, 11968519, 12774855, 14582481]

data1 = [int(i/10000) for i in data1_raw]
data2 = [int(i/10000) for i in data2_raw]

max_val = math.ceil(max(max(data1), max(data2)) / 1000) * 1000
step = math.ceil(max_val / 4)
y_max = step * 4

chart_config = {
    "type": "line",
    "data": {
        "labels": [
            "24/07/18", "24/09/02", "24/09/30", "24/10/31",
            "24/11/29", "24/11/30", "24/12/21", "24/12/28", 
            "24/12/30", "25/01/09", "25/01/24", "24/02/09"
        ],
        "datasets": [
            {
                "label": "누적합",
                "data": data1,
                "fill": False,
                "borderColor": "#FF0000",
                "borderWidth": 1,
                "lineTension": 0.1,
                "pointRadius": 1,
            },
            {
                "label": "value2",
                "data": data2,
                "fill": False,
                "borderColor": "#00B050",
                "borderWidth": 1,
                "lineTension": 0.1,
                "pointRadius": 1,
                "spanGaps": True  # null 값이 있어도 선이 끊기지 않게 함
            }
        ]
    },
    "options": {
        "legend": {
            "display": False,
            "labels": {
                "fontSize": 7,
                "fontColor": "white"
            }
        },
        "title": {
            "display": False
        },
        "scales": {
            "xAxes": [{
                "gridLines": {
                    "display": False
                },
                "ticks": {
                    "fontSize": 7,
                    "fontColor": "white"
                }
            }],
            "yAxes": [{
                "gridLines": {
                    "display": True,
                    # 짧은 선과 긴 간격으로 듬성듬성 찍히게 수정
                    "borderDash": [0.5, 1.5],
                    "color": "gray"
                },
                "ticks": {
                    "fontSize": 7,
                    "fontColor": "white",
                    "min": 0,
                    "max": max_val,
                    "stepSize": step,
                }
            }]
        },
        # 각 데이터 점 위에 값 표시 (Chart.js datalabels 플러그인 사용)
        "plugins": {
            "datalabels": {
                "display": True,
                "align": "top",
                "anchor": "end",
                "color": "white",
                "font": {
                    "size": 7
                }
            }
        }
    }
}

# JSON 문자열로 변환 (공백을 줄여서)
json_str = json.dumps(chart_config, separators=(',', ':'))
# URL 인코딩
encoded_config = urllib.parse.quote(json_str)

# QuickChart URL 생성
# 배경색은 구글 크롬 다크모드에 맞춘 "#202124", 가로 넓이는 1000px로 지정
url = f"https://quickchart.io/chart?c={encoded_config}&bkg=%23202124&width=700&devicePixelRatio=2"

print("QuickChart URL:", url)
webbrowser.open(url)

response = requests.get(url)

with open("chart.png", "wb") as file:
    file.write(response.content)
