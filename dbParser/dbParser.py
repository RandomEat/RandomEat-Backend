import json
import re
from geopy.geocoders import Nominatim

MANUALLY_INPUT = 0
geolocator = Nominatim(user_agent="random", timeout=10)


def parse_one_object(restaurant):
    output_restaurant_data = {}
    output_restaurant_data['restaurantId'] = restaurant['restaurantId']
    restaurant_title = restaurant['restaurantName'].split('|')
    restaurant_name = restaurant_title[0] if len(restaurant_title) < 2 else restaurant_title[1]
    output_restaurant_data['restaurantName'] = restaurant_name.split('—')[0].strip()
    restaurant_info = restaurant['restaurantInfo']
    output_restaurant_data['category'] = [cate.strip() for cate in restaurant_info['restaurantCategory'].split('/')]
    price_match = re.search(r'人均 \$(\d+)', restaurant['restaurantStateLabel'])
    if price_match:
        price = price_match.group(1)
        output_restaurant_data['price'] = price

    lat = restaurant_info['lat']
    lon = restaurant_info['lon']
    # location = geolocator.reverse(f"{lat}, {lon}")
    # region = location.raw['address'].get('town') if location.raw['address'].get('town') is not None \
    #     else location.raw['address'].get('suburb')
    output_restaurant_data['location'] = {
        'lat': lat,
        'lon': lon,
        # 'region': region
    }

    return output_restaurant_data


def main():
    file_name = input("enter input json file: ") if MANUALLY_INPUT else 'input.json'
    with open(file_name, "r") as f:
        content = f.read()

    json_data = json.loads(content)
    restaurants_data = json_data['data']['blocks']
    out_data = []
    print("parsing starts")
    i = 1
    for restaurant_data in restaurants_data:
        print("parsing restaurant", i)
        i += 1
        if restaurant_data['type'] == "normal":
            out_data.append(parse_one_object(restaurant_data['dataModule']['restaurant']))
    with open('output.json', "a") as out_f:
        json.dump(out_data, out_f, indent=2, ensure_ascii=False)
    print("parsing finishes")


if __name__ == "__main__":
    main()
