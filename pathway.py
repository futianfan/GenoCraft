input_file = 'significant_gene.txt'
url = 'https://maayanlab.cloud/Enrichr'
from bs4 import BeautifulSoup 
import requests
import json, pickle 
with open(input_file, 'r') as f:
    gene_names = [line.strip() for line in f]
gene_names = ['ACTR2','ACTR3']

# Set up the Enrichr API endpoint
url = 'https://maayanlab.cloud/Enrichr/addList'

# Prepare the payload
payload = {
    'list': (None, '\n'.join(gene_names)),
    'description': (None, 'Gene List') }

response = requests.post(url, files=payload)

if response.ok:
    # Get the enrichment results URL
    data = response.json()
    field = data['userListId'] 
    # print('ok', field) ## 62702201
    url = 'https://maayanlab.cloud/Enrichr/enrich?backgroundType=KEGG_2021_Human&userListId=' + str(field)
    response = requests.get(url, files=payload)
    data = response.json()
    print(data)
    print(data['KEGG_2021_Human'])
    kegg = data['KEGG_2021_Human']
    '''
		>>> kegg[0]
		[1, 'Bacterial invasion of epithelial cells', 1.4629866961219494e-05, 39846.0, 443583.42086411105, ['ACTR3', 'ACTR2'], 0.00010475955322122831, 0, 0]
		>>> kegg[1]
		[2, 'Fc gamma R-mediated phagocytosis', 2.3279900715828513e-05, 39806.0, 424647.23147698573, ['ACTR3', 'ACTR2'], 0.00010475955322122831, 0, 0]
		>>> kegg[2]
		[3, 'Yersinia infection', 4.6580119344254854e-05, 39726.0, 396240.5009906518, ['ACTR3', 'ACTR2'], 0.00013974035803276456, 0, 0]
		>>> kegg[3]
		[4, 'Tight junction', 7.098046025863679e-05, 39662.0, 378895.287253843, ['ACTR3', 'ACTR2'], 0.00015813213098648266, 0, 0]
    '''
    # print(type(kegg), kegg[0])
    # pickle.dump(kegg, open('tmp.pkl', 'wb'))

else:
    print("Error occurred while performing enrichment analysis.")
    print(f"Status code: {response.status_code}")
    print(f"Error message: {response.text}")



# response = requests.get(results_url)

# soup = BeautifulSoup(response.text, 'html.parser')
# soup_txt = str(soup)
# with open('bs.txt', 'w') as fout:
# 	fout.write(soup_txt)



# tag_element = [x for x in soup.findAll('a') if x.get('id')=='KEGG_2021_Human-BarGraph-link'][0]
# print('question is how to extract the url from')
# print(tag_element)







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








