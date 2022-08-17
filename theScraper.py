try:
    from random import choice as c
    from os import system, mkdir, chdir, getcwd
    from sys import platform
    from time import sleep
    import argparse
    from bs4 import BeautifulSoup as bs 
    from requests import post, get
    import mechanize
except ImportError:
    system("pip install mechanize bs4 requests")
    try:
        from bs4 import BeautifulSoup as bs 
        from requests import post, get
        import mechanize
    except ImportError:
        exit("Try installing [requests / mechanize / bs4] manually.")
parser = argparse.ArgumentParser(description="Scrap anywebsite's content [css, js, html, img] Using Requests , BeautifulSoup and Mechanize")
parser.add_argument("-ua", type = str, help = "The user-agent [ android || iphone ]", default="android")
parser.add_argument("-f", type = str, help = "File with all the websites to scrap")
args = parser.parse_args()
ua, f = args.ua, args.f
android, iphone = [
                #"Mozilla/5.0 (X11: U: Linux 2.4.2-2 i586: en-US: m18) Gecko/20010131 Netscape6/6.01",
                "Mozilla/5.0 (Linux; Android 10; SM-G975U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 10; SM-G960F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 9; SM-A205U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 11; SM-G996U Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 11; SM-A715F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Build/NPPS26.102-49-11; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 10; SM-N960U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) ",
                "Mozilla/5.0 (Linux; Android 11; SM-G991B Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 11; SM-N975U Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 10; SM-G960U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 11; SM-N986U Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko)",
                "Mozilla/5.0 (Linux; Android 11; SM-G780F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko)"
],[
               "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) WebKit/8611 (KHTML, like Gecko)"]
if ua == "iphone":
    ua = c(iphone)
else:
    ua = c(android)
class WEB:
    """The main class to scrap anywebsite's content [css, js, html, img] Using Requests , BeautifulSoup and Mechanize"""
    def __init__(self, ua, url):
        self.ua, self.url = ua, url
    def start(self):
            headers = {
                "User-agent": ua
            }
            browser = mechanize.Browser()
            browser.set_handle_robots(False)
            browser.set_handle_equiv(False)
            browser.set_handle_referer(True)
            browser.set_handle_redirect(True)
            browser.addheaders = [("User-agent", ua)]
            browser.open(url)
            a = browser.response().read()
            pre = bs(a, "html.parser")
            if len(pre) > 0:
                try:
                    web = url.split("/")[2]
                    mkdir(web)
                except FileExistsError:
                    pass
                chdir(web)
                getLo = getcwd()
                for x in ["html", "css", "js", "img"]:
                    try:
                        mkdir(x)
                    except FileExistsError:
                        pass
                chdir("html")
                open(f"index.html", "w", encoding="utf-8").write(str(pre))
                chdir(getLo)
                sleep(2)
                chdir("css") 
                #############{CSS}########################
                def GetCss(self):
                    x_css = pre.find_all("link", attrs = {"rel" : "stylesheet"})
                    css_list_fill = []
                    for x in x_css:
                        if x.attrs["href"] and not "script" in str(x):
                            if x.attrs['href'].startswith("http"):
                                src = x.attrs['href']
                                css_list_fill.append(src)
                            elif x.attrs['href'].startswith("./"):
                                src = f'{url}{x.attrs["href"].replace("./","/")}'
                                css_list_fill.append(src)
                            elif x.attrs['href'].startswith("/"):
                                src = f'{url}{x.attrs["href"]}'
                                css_list_fill.append(src)
                            else:
                                src = f"{url}/{x.attrs['href']}"
                                css_list_fill.append(src)
                    for x in css_list_fill:
                        css_name = x.split("/")[-1]
                        if "?" in css_name:
                            css_name = str(css_name.replace("?", "C")) + ".css"
                        try:
                            xContent = get(x, headers  = headers, timeout = 10).content.decode(encoding="utf-8")
                            open(css_name, "w", encoding="utf-8").write(str(xContent))
                        except Exception as E:
                            print(E)
                GetCss(self) #Execute Css's function
                #############{JAVASCRIPT}################
                chdir(getLo)
                chdir("js")
                def GetJs(self):
                    find_js_tag = pre.find_all("script", attrs = {"type" : "text/javascript"})
                    x_js = [x.attrs for x in find_js_tag]
                    js_list_fill = []
                    for x in x_js:
                        try:
                            if x["src"].startswith("http"):
                                #print("http", x["src"])
                                src = x['src']
                                js_list_fill.append(src)
                            elif x["src"].startswith("./"):
                                src = f"{url}{x['src'].replace('./', '/')}"
                                js_list_fill.append(src)
                            elif x["src"].startswith("js"):
                                src = f"{url}/{x['src']}"
                                js_list_fill.append(src)
                        except:
                            pass
                    for x in js_list_fill:
                        try:
                            xContent = get(x, headers = headers, timeout = 25).content.decode("utf-8")
                            js_file_name = f'{x.split("/")[-1]}'
                            if not js_file_name.endswith(".js"):
                                js_file_name = f"{js_file_name}.js"
                            if "?" in js_file_name:
                                js_file_name = str(js_file_name).replace("?", "Q")
                            open(js_file_name, "w" ,encoding="utf-8").write(str(xContent))
                        except Exception as E:
                            exit(E)
                GetJs(self) #Execute js's function
                ###############{IMG}###################
                chdir(getLo)
                chdir("img")
                def GetIMG(self):
                    find_img_tag = pre.find_all("img")
                    x = [x.attrs for x in find_img_tag]
                    img_list_fill = []
                    for lx in x:
                        try:
                            if lx["src"].startswith("http"):
                                src = lx["src"]
                                img_list_fill.append(src)
                            elif lx["src"].startswith("./"):
                                src = f"{url}{lx['src'].replace('./', '/')}"
                                img_list_fill.append(src)
                            elif lx['src'].startswith("/"):
                                src = f"{url}{lx['src']}"
                                img_list_fill.append(src)
                        except:
                            pass
                    for dx in img_list_fill:
                        try:
                            if dx.endswith("png") or dx.endswith("jpg") or dx.endswith("jpeg"):
                                dxContent = get(dx, headers = headers, timeout = 25).content
                                imagename = f"{dx.split('/')[-1]}"
                                if "?" in imagename:
                                    imagename = imagename.replace("?", "I")
                                open(imagename, "wb").write(dxContent)
                        except Exception as E:
                            print(E)
                GetIMG(self)
                chdir(getLo)
                print(f"Succesfully saved in {getcwd()}")
if __name__ == "__main__":
    try:
        i = 0
        ha = list(open(f, "r").readlines())
        for x in range(len(ha)):
            if x == 0:
                i = 1
                done, left = i, len(ha)
                print("Progress", f"{done}/{left}\n")
                done += 1
            else:
                print(i)
                done, left = i, len(ha)
                print("Progress", f"{done}/{left}\n")
                done += 1
            url = ha[x].strip()
            if not "http://" in url:
                url = f"http://{url}"
            WEB(ua, url).start()
            i += 1
        print("Done")
    except Exception as MainError:
        print(MainError)
