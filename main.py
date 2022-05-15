import time
from datetime import date, datetime, timedelta, timezone, time as dtime
import sys
import requests
import json
import xml.etree.ElementTree as ET
import threading
import queue

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont, ImageOps

import weather
import googlecalendar
import charm

BACKGROUND = (0,0,0)
ORANGE = (255,128,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

font16 = ImageFont.truetype('fonts/JF-Dot-jiskan16s-2000.ttf', 16)
font14 = ImageFont.truetype('fonts/JF-Dot-K14-2004.ttf', 14)


def main():
    global image
    try:
        char = charm.Charm()

        q = queue.Queue()
        image = Image.new('RGB',(64,32),BACKGROUND)
        draw = ImageDraw.Draw(image)


        thread_refresh = threading.Thread(target=refresh, args=(get_matrix(),))
        thread_clock = threading.Thread(target=disp_clock)
        thread_weather = threading.Thread(target=disp_weather)
        thread_sch = threading.Thread(target=get_schedules, args=(q,))
        thread_news = threading.Thread(target=get_news, args=(q,))
        thread_refresh.setDaemon(True)
        thread_clock.setDaemon(True)
        thread_weather.setDaemon(True)
        thread_sch.setDaemon(True)
        thread_news.setDaemon(True)
        thread_refresh.start()
        thread_clock.start()
        thread_weather.start()
        thread_sch.start()
        thread_news.start()

        print("Press CTRL-C to stop.")

        while True:
            while not q.empty():
                try:
                    item = q.get_nowait()
                except:
                    continue
                if item['type'] == 'news':
                    scroll(item['text'], ORANGE, 16)
                else:
                    scroll(item['text'], GREEN, 14)
                q.task_done()

            char.random(image)


    except KeyboardInterrupt:
        sys.exit(0)


def refresh(matrix):
    while True:
        matrix.SetImage(image)
        time.sleep(0.015)


def scroll(text, color, point):
    font = font16 if point == 16 else font14    
    l = len(text) * point
    # create news image 
    text_image = Image.new('RGB',(l,16),BACKGROUND)
    draw = ImageDraw.Draw(text_image)

    draw.text((0,0), text, color, font=font)

    image.paste(text_image, (0,16))
    time.sleep(1.5)

    for i in range(l):
        image.paste(text_image, (-i,16))
        time.sleep(0.015)


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


def get_news(queue):
    url = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'
    while True:
        try:
            response = requests.get(url)
            data = response.text
            root = ET.fromstring(data)
        except:
            root = {} 

        for item in root.iter('item'):
            if item.find('title') is None:
                continue
            news = item.find('title').text
            if item.find('description') is not None:
                news += '　　' + item.find('description').text
            queue.put({'type': 'news', 'text': news})
        queue.join()


def get_schedules(queue):
    sch = googlecalendar.GoogleCalendar()
    while True:
        try:
            events = sch.get_ut_schedules() or []
        except:
            events = []

        for event in events:
            startdt = event['start'].get('dateTime', event['start'].get('date'))
            startdt = datetime.fromisoformat(startdt)
            day = '今日' if datetime.combine((date.today() + timedelta(days=1)),
            dtime(tzinfo=timezone(timedelta(hours=9)))) > startdt else '明日'
            
            start_time =startdt.strftime('%H:%M')
            news = day + start_time + ' ' + event['summary']
            queue.put({'type': 'schedule', 'text': news})
        queue.join()


def disp_clock():
    image_blank = Image.new('RGB',(35,16),BACKGROUND)
    separator = ':'
    while True:
        clock = datetime.now().strftime('%H' + separator + '%M')
        separator = ' ' if separator == ':' else ':'

        image_clock = image_blank.copy()
        draw = ImageDraw.Draw(image_clock)
        draw.text((0,0), clock, ORANGE, font=font14)
        image.paste(image_clock, (0,0))
        time.sleep(1)

def disp_weather():
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

