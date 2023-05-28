input_file = 'significant_gene.txt'
url = 'https://maayanlab.cloud/Enrichr'
from bs4 import BeautifulSoup 
import requests

with open(input_file, 'r') as f:
    gene_names = [line.strip() for line in f]

gene_names = ['ACTR2','ACTR3']

# Set up the Enrichr API endpoint
url = 'https://maayanlab.cloud/Enrichr/addList'

# Prepare the payload
payload = {
    'list': (None, '\n'.join(gene_names)),
    'description': (None, 'Gene List')
}

response = requests.post(url, files=payload)

if response.ok:
    # Get the enrichment results URL
    data = response.json()
    file_content = response.content
    short_id = data['shortId']
    print('shortId', short_id)
    results_url = f'https://maayanlab.cloud/Enrichr/enrich?dataset={short_id}'

    print(f"Enrichment analysis completed successfully! You can view the results at:\n{results_url}")
    print(file_content)

else:
    print("Error occurred while performing enrichment analysis.")
    print(f"Status code: {response.status_code}")
    print(f"Error message: {response.text}")



response = requests.get(results_url)

soup = BeautifulSoup(response.text, 'html.parser')
soup_txt = str(soup)
with open('bs.txt', 'w') as fout:
	fout.write(soup_txt)



tag_element = [x for x in soup.findAll('a') if x.get('id')=='KEGG_2021_Human-BarGraph-link'][0]
print('question is how to extract the url from')
print(tag_element)







# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import time
# import requests

# def download_image_with_selenium(url, tag_name, onclick_value):
#     # Set up Selenium web driver (assuming Chrome)
#     chrome_path = '/Users/tianfanfu/Downloads/GenoCraft/chrome_driver/chromedriver'  # Replace with the actual path to chromedriver executable
#     service = Service(chrome_path)
#     driver = webdriver.Chrome(service=service)


#     driver.get(url)

#     # Find the element with the specified tag and onclick value
#     element = driver.find_element(By.XPATH, f"//{tag_name}[contains(@onclick, '{onclick_value}')]")


#     # # try:
#     # #     # Open the URL
#     # #     driver.get(url)

#     # #     # Find the element with the specified tag and onclick value
#     # #     element = driver.find_element(By.XPATH, f"//{tag_name}[contains(@onclick, '{onclick_value}')]")
        
#     #     # # Simulate the click event
#     #     # element.click()
        
#     #     # # Wait for the page to load or add explicit waits as needed
#     #     # time.sleep(2)  # Adjust the wait time as per your requirements
        
#     #     # # Extract the image URL from the current page or perform further processing
#     #     # image_url = driver.current_url
        
#     #     # # Download the image using requests
#     #     # response = requests.get(image_url)
        
#     #     # if response.status_code == 200:
#     #     #     file_name = image_url.split('/')[-1]
            
#     #     #     with open(file_name, 'wb') as file:
#     #     #         file.write(response.content)
#     #     #     print(f"Image '{file_name}' downloaded.")
#     #     # else:
#     #     #     print(f"Error downloading image: {response.status_code} - {response.reason}")
    
#     # finally:
#     #     # Quit the driver to close the browser
#     #     driver.quit()

# # Example usage:
# url = 'https://maayanlab.cloud/Enrichr/enrich?dataset=df29735164fc4ae4bc56946451d798e9'
# tag_name = 'button'
# onclick_value = "NavigateTo(0, '#KEGG_2021_Human', 62597200)"

# download_image_with_selenium(url, tag_name, onclick_value)








