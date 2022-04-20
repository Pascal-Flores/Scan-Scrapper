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
            print("your request was refused by the server :'('")
        if page.status_code == 404:
            print("your URL was not found :(")
        elif page.status_code == 408:
            print("your request timed out :/")
        elif page.status_code >= 500:
            print("the server shat himself (╯°□°)╯︵ ┻━┻")
        elif page.status_code >= 300:
            print("something bad happened ¯\_(ツ)_/¯")
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
            return links

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

                if "http://" not in url:

                    print("l'url ne contient pas de lien")

                else:
 
                    print(getLinks(values['-LIEN-']))


    Main()