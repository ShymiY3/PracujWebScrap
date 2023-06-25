from bs4 import BeautifulSoup
import requests
import pandas as pd

class PracujScraper():
    def __init__(self, url, title=None) -> None:
        self.url = url
        self.title = title
        self.request = requests.get(self.url)
        self.soup = BeautifulSoup(self.request.text, 'html.parser')
        self.categories = ['Ofert_Title', 'Company', 'Localization', 'More_Info']
        self.df = pd.DataFrame({x:[] for x in self.categories}, columns=self.categories)
        
    def get_info(self, child):
        ofert = child.find('div', class_='listing_c7z99rl')
        if ofert:
            info = [x.text for x in ofert.find_all(['h2', 'h4', 'h5'])]
            info.append(' | '.join([x.text for x in ofert.find_all('li')]))
            return {x:y for x,y in zip(self.categories, info)}
        return dict()
    def print_info(self):
        if self.title: print(self.title)
        print('-'*20)
        print(self.df.to_string())
        print('-'*20)
        print()
    
    def run(self):
        for child in self.soup.find('div', attrs={'data-test':'section-offers'}):
            if values:= self.get_info(child):
                self.df = pd.concat([self.df, pd.Series(values).to_frame().T], ignore_index=True)
        self.print_info()
        
def main():
    scrap1 = PracujScraper('https://www.pracuj.pl/praca/python;kw/praca%20zdalna;wm,home-office?et=1', "Zdalne praktyki")
    scrap1.run()
    scrap2 = PracujScraper('https://www.pracuj.pl/praca/python;kw/wroclaw;wp?rd=30&et=1', "Wroclaw praktyki")
    scrap2.run()
    scrap3 = PracujScraper('https://www.pracuj.pl/praca/python;kw/praca%20zdalna;wm,home-office?et=1', "Wroclaw junior")
    scrap3.run()
    
if __name__ == '__main__':
    main()