from datetime import datetime
import requests
import json

from PIL import Image, ImageDraw, ImageFont


font16 = ImageFont.truetype('fonts/JF-Dot-jiskan16s-2000.ttf', 16)
font14 = ImageFont.truetype('fonts/JF-Dot-K14-2004.ttf', 14)

forecast_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json'

class Weather_Forecast():
    # https://www.jma.go.jp/bosai/common/const/area.json
    area_code = ('230000','230010')
    data = {}
    forecast_url = ''
    telops = {}

    def __init__(self, area_code=None):
        if area_code is not None:
            self.area_code = area_code
        self.forecast_url = forecast_url.replace('{}', self.area_code[0])

        with open('./telops.json','r') as fp:
            self.telops = json.load(fp)


    def update(self):
            headers = {'content-type': 'application/json'}
            response = requests.get(self.forecast_url, headers=headers)
            response = response.json()

            data = {}
            for weather_set in response[0]['timeSeries']:
                for area in weather_set['areas']:
                    if area['area']['code'] == self.area_code[1]:
                        data.update(area)
                        break
                else:
                    pass

            self.data = data


    def get_icon(self, update=False):
        icon = [('☀',(255,128,16)),('☁',(128,128,128)),('☂',(32,32,255)),('☃',(160,160,160)),('★',(255,255,16))]

        def make_icon(weather1, weather2=None, LATER=False):
             nonlocal draw
             if weather2 is None:
                 draw.text((6,0), weather1[0], weather1[1], font=font16)
             else:
                 draw.text((0,0), weather1[0], weather1[1], font=font16)
                 draw.text((15,0), weather2[0], weather2[1], font=font14)
             if LATER:
                draw.polygon(((11,10),(11,14),(15,12)), fill=(64,128,0), outline=(64,128,0))

        daytime = datetime.now().hour > 3 or datetime.now().hour < 18
        CLEAR = icon[0] if daytime else icon[4]
        CLOUDY = icon[1]
        RAIN = icon[2]
        SNOW = icon[3]

        if update:
            self.update()

        code = self.data['weatherCodes'][0]
        telop = self.telops[code]

        image = Image.new('RGB',(29,16),(0,0,0))
        draw = ImageDraw.Draw(image)

        if telop[0] == '100.svg':   # CLEAR
            make_icon(CLEAR)
        elif telop[0] == '101.svg': # PARTLY CLOUDY
            make_icon(CLEAR, CLOUDY)
        elif telop[0] == '102.svg': # CLEAR, OCCASIONAL SCATTERED SHOWERS
            make_icon(CLEAR, RAIN)
        elif telop[0] == '104.svg': # CLEAR, SNOW FLURRIES
            make_icon(CLEAR, SNOW)
        elif telop[0] == '110.svg': # CLEAR, PARTLY CLOUDY LATER
            make_icon(CLEAR, CLOUDY, LATER=True)
        elif telop[0] == '112.svg': # CLEAR, RAIN LATER
            make_icon(CLEAR, RAIN, LATER=True)
        elif telop[0] == '115.svg': # CLEAR, SNOW LATER
            make_icon(CLEAR, SNOW, LATER=True)
        elif telop[0] == '200.svg': # CLOUDY
            make_icon(CLOUDY)
        elif telop[0] == '201.svg': # MOSTLY CLOUDY
            make_icon(CLOUDY, CLEAR)
        elif telop[0] == '202.svg': # CLOUDY, OCCASIONAL SCATTERED SHOWERS
            make_icon(CLOUDY, RAIN)
        elif telop[0] == '204.svg': # CLOUDY, OCCASIONAL SNOW FLURRIES
            make_icon(CLOUDY, SNOW)
        elif telop[0] == '210.svg': # CLOUDY, CLEAR LATER
            make_icon(CLOUDY, CLEAR, LATER=True)
        elif telop[0] == '212.svg': # CLOUDY, RAIN LATER
            make_icon(CLOUDY, RAIN, LATER=True)
        elif telop[0] == '215.svg': # CLOUDY, SNOW LATER
            make_icon(CLOUDY, SNOW, LATER=True)
        elif telop[0] == '300.svg': # RAIN
            make_icon(RAIN)
        elif telop[0] == '301.svg': # RAIN, PARTLY CLOUDY
            make_icon(RAIN, CLEAR)
        elif telop[0] == '302.svg': # SHOWERS THROUGHOUT THE DAY
            make_icon(RAIN, CLOUDY)
        elif telop[0] == '303.svg': # RAIN, FREQUENT SNOW FLURRIES
            make_icon(RAIN, SNOW)
        elif telop[0] == '308.svg': # RAINSTORM
            make_icon(RAIN, RAIN)
        elif telop[0] == '311.svg': # RAIN, CLEAR LATER
            make_icon(RAIN, CLEAR, LATER=True)
        elif telop[0] == '313.svg': # RAIN, CLOUDY LATER
            make_icon(RAIN, CLOUDY, LATER=True)
        elif telop[0] == '314.svg': # RAIN, SNOW LATER
            make_icon(RAIN, SNOW, LATER=True)
        elif telop[0] == '400.svg': # SNOW
            make_icon(SNOW)
        elif telop[0] == '401.svg': # SNOW, FREQUENT CLEAR
            make_icon(SNOW, CLEAR)
        elif telop[0] == '402.svg': # SNOW THROUGHOUT THE DAY
            make_icon(SNOW, CLOUDY)
        elif telop[0] == '403.svg': # SNOW, FREQUENT SCCATERED SHOWERS
            make_icon(SNOW, RAIN)
        elif telop[0] == '406.svg': # SNOWSTORM
            make_icon(SNOW, SNOW)
        elif telop[0] == '411.svg': # SNOW, CLEAR LATER
            make_icon(SNOW, CLEAR, LATER=True)
        elif telop[0] == '413.svg': # SNOW, CLOUDY LATER
            make_icon(SNOW, CLOUDY, LATER=True)
        elif telop[0] == '414.svg': # SNOW, RAIN LATER
            make_icon(SNOW, RAIN, LATER=True)

        return image


if __name__ == '__main__':
    w = Weather_Forecast()
    w.update()
    print(w.data)
