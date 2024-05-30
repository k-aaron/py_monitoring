import requests
import json
import time
from datetime import datetime

#
# 제주도닷컴에서 원하는 조건의 항공편이 있는지 확인하는 프로그램입니다.
#

# URL로부터 데이터를 가져오고, 파싱하는 함수
def fetch_and_parse_json(url):
    try:
        # URL로부터 데이터를 가져옵니다.
        response = requests.get(url)
        # 응답 코드가 200(성공)일 경우
        if response.status_code == 200:
            # JSON 데이터를 파싱합니다.
            data = response.json()
            return data
        else:
            print(f"Error: Unable to fetch data. HTTP Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred: {e}")
        return None

# 슬랙으로 메시지를 보내는 함수
def send_slack_webhook(text):
    # Webhook URL
    webhook_url = 'https://hooks.slack.com/services/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'

    # 메시지 데이터
    message_data = {
        "text": text
    }

    # HTTP POST 요청 보내기
    response = requests.post(
        webhook_url,
        headers = {'Content-Type': 'application/json'},
        data = json.dumps(message_data)
    )

    # 응답 확인
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')

# 메인 함수
def main():
    # 검색 조건
    #dep = "GMP"
    #arr = "CJU"
    dep = "CJU"
    arr = "GMP"
    search_date = "20240609"
    start_time_str = "14:00"
    end_time_str = "17:10"
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    # 확인 할 URL 목록
    urls = [f'https://apisc.jejudo.com/api/7C/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/LJ/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/ZE/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/TW/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/RS/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/4V/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/KE/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/OZ/{dep}/{arr}/1/0/0/{search_date}/0/default',
    f'https://apisc.jejudo.com/api/BX/{dep}/{arr}/1/0/0/{search_date}/0/default']

    while True:
        print(f"[{search_date}][{dep}->{arr}] Working for a flight ticket departing between {start_time_str} and {end_time_str}.")
        resultText = ""
        for url in urls:
            json_data = fetch_and_parse_json(url)

            if json_data is not None:
                # schedule 리스트에서 CarrierName과 DepTime을 출력
                for flight in json_data['schedule']:
                    carrier_name = flight.get('CarrierName')
                    dep_time_str = flight.get('DepTime')
                    dep_time = datetime.strptime(dep_time_str, "%H:%M").time()

                    # start_time ~ end_time 사이의 시간인지 확인
                    if start_time <= dep_time <= end_time:
                        resultText = f"[{search_date}][{dep}->{arr}] {carrier_name}, DepTime: {dep_time}"
                        print(resultText)
                        send_slack_webhook(resultText)
        
        # 10초 대기
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print("Process interrupted by user")
            break

# 메인 함수 호출
if __name__ == "__main__":
    main()
