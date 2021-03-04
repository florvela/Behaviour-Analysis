from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
import os
import pdb
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import os

class GoogleeImageDownloader(object):

    # _URL = "https://www.google.co.in/search?q={}&source=lnms&tbm=isch&num=100"
    _URL = "https://www.google.com/search?hl=jp&q={}&btnG=Google+Search&tbs=0&safe=off&tbm=isch&num=100"
    _BASE_DIR = 'GoogleImages'
    _HEADERS = {
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    def __init__(self, query):
        # query = "pistola" #raw_input("Enter keyword to search images\n")
        self.dir_name = os.path.join(self._BASE_DIR, query.split()[0])
        self.url = self._URL.format(urllib.parse.quote(query))
        self.make_dir_for_downloads()
        self.initiate_downloads()

    def make_dir_for_downloads(self):
        print("Creating necessary directories")
        if not os.path.exists(self._BASE_DIR):
            os.mkdir(self._BASE_DIR)

        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

    def initiate_downloads(self):
        src_list = []
        for i in range(1,35):
            try:
                start = str(i * 21)
                html = urllib.request.urlopen(urllib.request.Request(self.url+'&start='+start,headers=self._HEADERS)).read().decode('utf-8')
                html = BeautifulSoup(html,'html.parser')
                elems = html.find_all('img')
                print(len(elems))
                print(i)
                for img in elems:
                    print(img)
                    if img.has_attr("data-src"):
                        src_list.append(img['data-src'])
                    elif img.has_attr("src"):
                        src_list.append(img['src'])
            except:
                break

        print("{} of images collected for downloads".format(len(src_list)))
        self.save_images(src_list)

    def save_images(self, src_list):
        print("Saving Images...")
        pdb.set_trace()
        for i , src in enumerate(src_list):
            try:
                req = urllib.request.Request(src, headers=self._HEADERS)
                raw_img = urllib.request.urlopen(req).read(1024)
                with open(os.path.join(self.dir_name , str(i)+".jpg"), 'wb') as f:
                    f.write(raw_img)
            except Exception as e:
                print ("could not save image")
                # raise e


from shutil import copyfile
from google_images_search import GoogleImagesSearch

def step1():
    instruction = "Go to Google Images, make a search, open the console, scroll!!! And then, add the following code to the JS console:"
    JScode = """
    /**
     * simulate a right-click event so we can grab the image URL using the
     * context menu alleviating the need to navigate to another page
     *
     * attributed to @jmiserez: http://pyimg.co/9qe7y
     *
     * @param   {object}  element  DOM Element
     *
     * @return  {void}
     */
    function simulateRightClick( element ) {
        var event1 = new MouseEvent( 'mousedown', {
            bubbles: true,
            cancelable: false,
            view: window,
            button: 2,
            buttons: 2,
            clientX: element.getBoundingClientRect().x,
            clientY: element.getBoundingClientRect().y
        } );
        element.dispatchEvent( event1 );
        var event2 = new MouseEvent( 'mouseup', {
            bubbles: true,
            cancelable: false,
            view: window,
            button: 2,
            buttons: 0,
            clientX: element.getBoundingClientRect().x,
            clientY: element.getBoundingClientRect().y
        } );
        element.dispatchEvent( event2 );
        var event3 = new MouseEvent( 'contextmenu', {
            bubbles: true,
            cancelable: false,
            view: window,
            button: 2,
            buttons: 0,
            clientX: element.getBoundingClientRect().x,
            clientY: element.getBoundingClientRect().y
        } );
        element.dispatchEvent( event3 );
    }
    
    /**
     * grabs a URL Parameter from a query string because Google Images
     * stores the full image URL in a query parameter
     *
     * @param   {string}  queryString  The Query String
     * @param   {string}  key          The key to grab a value for
     *
     * @return  {string}               value
     */
    function getURLParam( queryString, key ) {
        var vars = queryString.replace( /^\?/, '' ).split( '&' );
        for ( let i = 0; i < vars.length; i++ ) {
            let pair = vars[ i ].split( '=' );
            if ( pair[0] == key ) {
                return pair[1];
            }
        }
        return false;
    }
    /**
     * Generate and automatically download a txt file from the URL contents
     *
     * @param   {string}  contents  The contents to download
     *
     * @return  {void}
     */
    function createDownload( contents ) {
        var hiddenElement = document.createElement( 'a' );
        hiddenElement.href = 'data:attachment/text,' + encodeURI( contents );
        hiddenElement.target = '_blank';
        hiddenElement.download = 'urls.txt';
        hiddenElement.click();
    }
    
    /**
    * grab all URLs va a Promise that resolves once all URLs have been
     * acquired
     *
     * @return  {object}  Promise object
     */
    function grabUrls() {
        var urls = [];
        return new Promise( function( resolve, reject ) {
            var count = document.querySelectorAll(
                '.isv-r a:first-of-type' ).length,
                index = 0;
            Array.prototype.forEach.call( document.querySelectorAll(
                '.isv-r a:first-of-type' ), function( element ) {
                // using the right click menu Google will generate the
                // full-size URL; won't work in Internet Explorer
                // (http://pyimg.co/byukr)
                simulateRightClick( element.querySelector( ':scope img' ) );
                // Wait for it to appear on the <a> element
                var interval = setInterval( function() {
                    if ( element.href.trim() !== '' ) {
                        clearInterval( interval );
                        // extract the full-size version of the image
                        let googleUrl = element.href.replace( /.*(\?)/, '$1' ),
                            fullImageUrl = decodeURIComponent(
                                getURLParam( googleUrl, 'imgurl' ) );
                        if ( fullImageUrl !== 'false' ) {
                            urls.push( fullImageUrl );
                        }
                        // sometimes the URL returns a "false" string and
                        // we still want to count those so our Promise
                        // resolves
                        index++;
                        if ( index == ( count - 1 ) ) {
                            resolve( urls );
                        }
                    }
                }, 10 );
            } );
        } );
    }
    /**
     * Call the main function to grab the URLs and initiate the download
     */
    grabUrls().then( function( urls ) {
        urls = urls.join( '\n' );
        createDownload( urls );
    } );
    """
    print(instruction)
    print(JScode)

from imutils import paths
import argparse
import requests
import cv2
import os

def downloadUrls(urlfile=None, path_to_download=None):
    # construct the argument parse and parse the arguments
    if not urlfile or not path_to_download:
        ap = argparse.ArgumentParser()
        ap.add_argument("-u", "--urls", required=True,
                        help="path to file containing image URLs")
        ap.add_argument("-o", "--output", required=True,
                        help="path to output directory of images")
        args = vars(ap.parse_args())
        urlfile = args["urls"]
        path_to_download = args["output"]
    # grab the list of URLs from the input file, then initialize the
    # total number of images downloaded thus far
    rows = open(urlfile).read().strip().split("\n")
    total = 0
    # loop the URLs
    for url in rows:
        try:
            # try to download the image
            r = requests.get(url, timeout=60)
            # save the image to disk
            p = os.path.sep.join([path_to_download, "{}.jpg".format(
                str(total).zfill(8))])
            f = open(p, "wb")
            f.write(r.content)
            f.close()
            # update the counter
            print("[INFO] downloaded: {}".format(p))
            total += 1
        # handle if any exceptions are thrown during the download process
        except:
            print("[INFO] error downloading {}...skipping".format(p))



if __name__ == "__main__":

    step1()
    dataset_dir = '.\\dataset\\images\\'
    urls = '.\\urls.txt'
    downloadUrls(urls, dataset_dir)

    ####################### https://www.pyimagesearch.com/2017/12/04/how-to-create-a-deep-learning-dataset-using-google-images/


    # gis = GoogleImagesSearch('AIzaSyDw1cFMA-OPEkQkxxNa2HSosqidxgEQt3E', 'bead3dc84fc55baf4')
    # _search_params = {
    #     'num': 1000,
    #     'fileType': 'jpg',
    # }
    #
    # for elem in ['pistola', 'gun']:
    #     _search_params['q'] = elem
    #     gis.search(search_params=_search_params)
    #     for image in gis.results():
    #         print(image)
    #         try:
    #             image.download('.//GoogleImages//')
    #         except Exception as e:
    #             print(e)
        # for i in range(30):
            # gis.next_page()
            # for image in gis.results():
            #     image.download('.//GoogleImages//')

    # for elem in ['pistola', 'gun']:
    #     GoogleeImageDownloader(elem)

    dataset_dir = '.\\dataset\\images\\'
    #
    # if not os.path.exists(dataset_dir):
    #     os.mkdir(dataset_dir)
    #
    # folders = ['GoogleImages/'+elem+'/' for elem in os.listdir('GoogleImages')]
    # files = []
    # for folder in folders:
    #     files += [folder+file for file in os.listdir(folder)]
    #
    # for i, file in enumerate(files):
    #     print(f'copying images: {i+1}/{len(files)} DONE')
    #     copyfile(file, dataset_dir+f'{i}.jpg')

