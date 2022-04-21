import PySimpleGUI as sg
import os
import sys
import requests
import json
import re
from lxml import html, etree

if __name__ == '__main__':

    def MakeWindow(theme):

        sg.theme(theme)

        layout = [[
            [sg.T('Lien du manga'), sg.Input(key='-LIEN-')],
            [sg.B('scrap')]
        ]]
        window = sg.Window('scrap manga', layout, size = (400,400))

        return window

    def getLinks(url):
        page = requests.get(url)
        if page.status_code == 403:
            print("Error 403 : your request was refused by the server (ง •̀_•́)ง")
            return
        if page.status_code == 404:
            print("Error 404 : your URL was not found |-_-|")
            return
        elif page.status_code == 408:
            print("Error 408 : your request timed out ( -_-)zZ")
            return
        elif page.status_code >= 500:
            print("Error 500+ : the server shat himself (╯°□°)╯︵ ┻━┻")
            return
        elif page.status_code >= 300:
            print("Unknown error : something bad happened ¯\_(ツ)_/¯")
            return
        else:
            pageContent = html.fromstring(page.content)
            readerScript = pageContent.xpath("//script[contains(text(), 'ts_reader.run')]/text()")
            jsonFromReaderScript = json.loads(readerScript[0][readerScript[0].find("{"):readerScript[0].rfind("}")+1])
            links = 0
            for sources in range(len(jsonFromReaderScript["sources"])):
                if links == 0:
                    links = jsonFromReaderScript["sources"][sources]["images"]
                else:
                    links.append(jsonFromReaderScript["sources"][sources]["images"])
            nextTome = jsonFromReaderScript["nextUrl"]
            return (links, nextTome)

    #print(getLinks("https://sushi-scan.su/berserk-volume-1/"))

    def Main():

        window = MakeWindow(sg.theme('Dark Amber'))

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                break

            if event == 'scrap':
                url = values['-LIEN-']
                print(getLinks(values['-LIEN-']))


    Main()
