import PySimpleGUI as sg
import os
import requests
import json
from lxml import html, etree

if __name__ == '__main__':

    def MakeWindow(theme):

        sg.theme(theme)

        layout = [[
            [sg.T('Lien du manga'), sg.Input(key='-LIEN-')],
            [sg.B('scrap')],
            [sg.T('destination (absolu)'),sg.Input(key='-DESTINATION-')]
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

    def scrapLink(url, tomeIndex, pageIndex):
        response = requests.get(url)
        if response.status_code >= 300:
            print("Error : image "+str(pageIndex)+" of volume "+str(tomeIndex)+" could not be retrieved...")
        else:
            img_data = requests.get(url).content
        return img_data

    def saveImage(imageData, path, tomeIndex, pageIndex):
        if path[len(path)-1] != '/':
            path += '/'
        destination = str(path)+"tome"+str(tomeIndex)
        if(os.path.isdir(destination) == False):
            os.mkdir(destination)
        with open(destination+'/'+str(pageIndex)+'.jpg', 'wb') as handler:
            handler.write(imageData)
        return

    def getVolume(imagesLinks, path, tomeIndex):
        pageIndex = 1
        for link in imagesLinks:
            saveImage(scrapLink(link, tomeIndex, pageIndex), path, tomeIndex, pageIndex)
            pageIndex += 1
        return

    def Main():

        window = MakeWindow(sg.theme('Dark Amber'))

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                break

            if event == 'scrap':
                url = values['-LIEN-']
                volumeLinks = getLinks(url)
                while True:
                    getVolume(volumeLinks[0], values['-DESTINATION-'], url[url.rfind('-')+1:url.rfind('/')])
                    url = volumeLinks[1]
                    volumeLinks = getLinks(url)
                    if "volume" in volumeLinks[1] == False:
                        break

    Main()
