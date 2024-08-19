import requests
import json
import time

def get_weather_info(city, apikey, lang="en", units="metric"):
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units={units}"

    result = requests.get(api)
    data = json.loads(result.text)

    weather_info = {
        "location": data["name"],
        "weather": data["weather"][0]["description"],
        "temperature": {
            "current": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "min": data["main"]["temp_min"],
            "max": data["main"]["temp_max"]
        }
    }

    return weather_info

def save_weather_info(weather_info, filename="./resource/intentRecognition/complicateIntent/weather_info.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(weather_info, f, ensure_ascii=False, indent=4)

def main():
    start_time = time.time()  # Start timing

    city = "Ulsan"
    apikey = "1665f8090ad1a59a2f0e7205979435e6"
    lang = "kr"

    weather_info = get_weather_info(city, apikey, lang)

    # Print the weather information
    print(f"{weather_info['location']}의 날씨입니다.")
    print(f"날씨는 {weather_info['weather']}입니다.")
    print(f"현재 온도는 {weather_info['temperature']['current']}입니다.")
    print(f"하지만 체감 온도는 {weather_info['temperature']['feels_like']}입니다.")
    print(f"최저 기온은 {weather_info['temperature']['min']}입니다.")
    print(f"최고 기온은 {weather_info['temperature']['max']}입니다.")

    # Save the weather information to a JSON file
    save_weather_info(weather_info)

    end_time = time.time()  # End timing
    execution_time = end_time - start_time

    # # Add execution time to the weather_info dictionary
    # weather_info["execution_time"] = f"{execution_time:.4f} seconds"

    # Print execution time
    print(f"\n실행 시간: {execution_time:.4f} 초")

    # Return the weather information as JSON
    return json.dumps(weather_info, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print(main())