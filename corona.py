# import Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly as py
import matplotlib.pyplot as plt
import plotly.graph_objs as go
#Sending request using URL
page = requests.get('https://www.worldometers.info/coronavirus/')
#print(page) #To check wheather page is accessible or not
#print(page.status_code) # 200  means Page Found OK

#print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

Location = []
Victims = []
df = pd.DataFrame(columns=["Location","Victims"])

print("COVID-19 CORONAVIRUS OUTBREAK")
for info in soup.find_all('div',id='maincounter-wrap'):
    print(info.text)

# Extracting table data
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    Location.append(td[0].text)
    Victims.append(td[1].text)
print(Location)
print(Victims)
df = pd.DataFrame({'Location':Location,'Victims':Victims})
#Printing collected data
print(df)
df.to_csv("Corona.csv",index=False)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('Corona.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
writer.save()

fig = go.Figure(data=go.Choropleth(
    locations = df['Location'],
    locationmode = 'country names',
    z = df['Victims'],
    colorscale = 'Reds',
    marker_line_color = 'black',
    marker_line_width = 0.5,
))
fig.update_layout(
    title_text = 'Corona Virus:Country Vs Victims except China (Live Graph)',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
        projection_type = 'equirectangular'
    )
)
fig.show()
