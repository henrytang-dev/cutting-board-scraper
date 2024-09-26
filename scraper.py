import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = 'https://www.cuttingboards.net/'

# Send a GET request to the URL
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    header_div = body.find('header', class_=['main-header', 'home-header'])
    ul = header_div.find('nav', class_='header-nav-wrapper').find('ul', class_='header-nav')
    # print(ul.find_all('li'))

    links = set()
    for li in ul.find_all('li', class_='header-nav-item'):
        # print(li)
        div = li.find('div', class_='header-dropdown')
        # print(div)
        for d in div.find_all('div', class_='dropdown-menu-column'):
            a = d.find('ul').find('li').find('a')
            links.add(a['href'])
            # print(a.text, a['href'])
    
    product_links = set()
    for link in links:
        curr_link = link
        # print(curr_link)
        cnt = 1
        while True:
            # print(len(product_links))
            response = requests.get(curr_link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                body = soup.find('body')
                main = body.find('main', class_='main-content')
                section = main.find('section', class_='collection-page')
                div = section.find('div', class_='collection-products').find('div', class_='layout-container')
                form = div.find('form', class_='form')

                # footer = section.find('footer', class_='collection-footer')
                # page = footer.find('div', class_=['layout-container', 'collection-pagination']).find('div', class_='pagination')
                # next_page = None
                # if page is not None:
                #     print("got here")
                #     pagination = page.find('div', class_=['pagination-item', 'pagination-next'])
                #     print(pagination)
                #     a = pagination.find('a')
                #     print(a)
                #     if a is not None:
                #         print("got second stage")
                #         print(a['href'])
                #         next_page = a['href']



                for article in form.find_all('article', class_='product-item'):
                    figure = article.find('figure', class_='product-item-top')
                    a = figure.find('a', class_=['product-item-thumbnail', 'item-thumbnail', 'item-thumbnail', 'image-cover'])
                    product_links.add(a['href'])
                    # print(a['href'])
                
                # if next_page is None:
                #     break
                curr_link = link + "?page=" + str(cnt)
                cnt+=1
            else:
                break
            







    # Initialize lists to store scraped data
    products = []
    prices = []
    links = []

    # Find all the product elements (adjust the class based on the website structure)
    for product in soup.find_all('div', class_='product-item'):
        # Extract product name
        name = product.find('h2', class_='product-title').text.strip()
        products.append(name)
        
        # Extract product price
        price = product.find('span', class_='price').text.strip()
        prices.append(price)
        
        # Extract product URL
        link = product.find('a', href=True)['href']
        links.append(url + link)

    # Store the scraped data in a DataFrame
    data = pd.DataFrame({
        'Product Name': products,
        'Price': prices,
        'Product Link': links
    })

    # Display the DataFrame
    print(data)

else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")