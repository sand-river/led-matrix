import time
from datetime import date, datetime, timedelta, timezone
from datetime import time as dtime
import sys
import requests
import json
import xml.etree.ElementTree as ET
import threading

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont, ImageOps

import characters
import weather
import googlecalendar

BACKGROUND = (0,0,0)
ORANGE = (255,128,0)
BLUE = (64,64,255)
GREEN = (64,255,64)

font16 = ImageFont.truetype('fonts/JF-Dot-jiskan16s-2000.ttf', 16)
font14 = ImageFont.truetype('fonts/JF-Dot-K14-2004.ttf', 14)


def main():
    try:
        matrix = get_matrix()
        mario = characters.Mario()
        sch = googlecalendar.GoogleCalendar()
        image, draw = init_matrix()

        thread_clock = threading.Thread(target=disp_clock, args=(image,))
        thread_weather = threading.Thread(target=disp_weather, args=(image,))
        thread_clock.setDaemon(True)
        thread_weather.setDaemon(True)
        thread_clock.start()
        thread_weather.start()

        print("Press CTRL-C to stop.")

        while True:
            events = sch.get_ut_schedules()
            for event in events:
                startdt = event['start'].get('dateTime', event['start'].get('date'))
                startdt = datetime.fromisoformat(startdt)
                day = '今日' if datetime.combine((date.today() + timedelta(days=1)),
                dtime(tzinfo=timezone(timedelta(hours=9)))) > startdt else '明日'
                
                start_time =startdt.strftime('%H:%M')
                print(day + start_time, event['summary'])
                news = day + start_time + ' ' + event['summary']

                l = len(news) * 16 - 12
                # create news image 
                lower_image = Image.new('RGB',(l,16),BACKGROUND)
                lower_draw = ImageDraw.Draw(lower_image)
                lower_draw.text((0,0), news, GREEN, font=font16)

                image.paste(lower_image, (0,16))

                matrix.SetImage(image)
                time.sleep(1.8)

                for i in range(l):
                    image.paste(lower_image, (-i,16))
                    matrix.SetImage(image)
                    time.sleep(0.015)

            # News topics
            rss = get_news()

            for item in rss.iter('item'):
                # get news item
                if item.find('title') is None:
                    continue
                news = item.find('title').text
                if item.find('description') is not None:
                    news += '　　' + item.find('description').text

                l = len(news) * 16
                # create news image 
                lower_image = Image.new('RGB',(l,16),BACKGROUND)
                lower_draw = ImageDraw.Draw(lower_image)
                lower_draw.text((0,0), news, ORANGE, font=font16)

                image.paste(lower_image, (0,16))

                matrix.SetImage(image)
                time.sleep(1.8)

                for i in range(l):
                    image.paste(lower_image, (-i,16))
                    matrix.SetImage(image)
                    time.sleep(0.015)

            for i in range(20):
                image_m = image.copy()
                image_m.paste(mario.images[i%2+1], (i*4-16,16))
                matrix.SetImage(image_m.convert('RGB'))
                time.sleep(0.15)

    except KeyboardInterrupt:
        sys.exit(0)


def init_matrix():
    # Initialize
    image = Image.new('RGB',(64,32),BACKGROUND)
    draw = ImageDraw.Draw(image)

    return image, draw

def get_matrix():
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'regular'

    options.gpio_slowdown = 2
    options.limit_refresh_rate_hz = 120
    # options.show_refresh_rate = 1
    options.brightness = 50 
    # options.disable_hardware_pulsing = True

    return RGBMatrix(options = options)


def get_news():
    url = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'
    try:
        response = requests.get(url)
        data = response.text
        root = ET.fromstring(data)
    except:
        root = {} 
    return root


def disp_clock(image):
    image_blank = Image.new('RGB',(35,16),BACKGROUND)
    image_clock = image_blank.copy()
    draw = ImageDraw.Draw(image_clock)

    clock0 = datetime.now().strftime('%H:%M')
    draw.text((0,0), clock0, ORANGE, font=font14)
    image.paste(image_clock, (0,0))

    separator = ':'
    while True:
        clock1 = datetime.now().strftime('%H' + separator + '%M')
        separator = ' ' if separator == ':' else ':'
        clock0 = clock1
        image_clock = image_blank.copy()
        draw = ImageDraw.Draw(image_clock)
        draw.text((0,0), clock0, ORANGE, font=font14)
        image.paste(image_clock, (0,0))
        time.sleep(0.9)

def disp_weather(image):
    x = 29
    y = 16

    image_blank = Image.new('RGB',(x,y*2),BACKGROUND)

    masks = list(range(y+1))
    for i in range(y+1):
        mask = Image.new('1', (x,y*2), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rectangle((0,i,x,y+i), fill=1, outline=1)
        masks[i] = mask.copy()

    wf = weather.Weather_Forecast()
    while True:
        image_weather = image_blank.copy()
        draw = ImageDraw.Draw(image_weather)

        weather_icon = wf.get_icon(update=True)
        image_weather.paste(weather_icon, (0,0))
        draw.text((2,y), '{:>3}%'.format(wf.data['pops'][0]), BLUE, font=font14)

        image.paste(image_weather, (35,0), masks[0])
        for _ in range(20):
            time.sleep(15)
            for i in range(y):
                image.paste(image_weather, (35,-i-1), masks[i+1])
                time.sleep(0.045)
            time.sleep(15)
            for i in range(y):
                image.paste(image_weather, (35,-y+1+i), masks[y-1-i])
                time.sleep(0.045)


if __name__ == '__main__':
    main()

