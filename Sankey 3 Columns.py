# Importing Stuff I Need
import pandas as pd
import plotly.graph_objects as go
import warnings

# Ignoring Warnings lol
warnings.filterwarnings("ignore")

# Reading File
filenamepath = 'example_data.csv'

# Turning data in file into a dataframe
df = pd.read_csv(filenamepath)

#Uncomment if there are blanks in data. It will replace blank values with N/A, !!! May break graph when using many columns
#df.fillna("N/A",inplace=True)

# Image / Graph Options
pngwidth = 1080
pngheight = 720

# Coloring options
nodeAlpha = 0.8
nodeColorManual = 'rgba(23, 39, 54, 0.9)'
linkAlpha = 0.3

# Selecting the 4 columns to use within the dataframe
column1 = 'Detections'
column2 = 'Current Sources with S1'
column3 = 'Current Sources with S1 Location'

# Selecting the column with color values within the dataframe
colorColumn = 'Current Sources with S1 Color'

# Need to select columns that will always have a value. It will not be shown in graph
counterColumn = 'Detection ID'
column1_2_count = counterColumn
column2_3_count = counterColumn

# Creating 3 dataframes to hold values to create Sankey
df1 = df.groupby([column1,column2,colorColumn])[column1_2_count].count().reset_index()
df1.columns = ['source','target','colorNode','value']
df2 = df.groupby([column2,column3, colorColumn])[column2_3_count].count().reset_index()
df2.columns = ['source','target','colorNode','value']

# Uncomment if there are blanks in data. It will replace blank values with "Other1" or "Other2", !!! less likely to break graph
#df1.fillna("Other1",inplace=True)
#df2.fillna("Other2",inplace=True)

# Inserting color values into every dataframe
df1['colorLink'] = df1['colorNode']
df2['colorLink'] = df2['colorNode']

# Obtaining column length from Dataframes 
df1length = len(df1['value'])
df2length = len(df2['value'])

# The following is manipulating the color values to work with Sankey
for x in range(df1length):
    test = str(df1['colorLink'][x])
    test1 = test.rstrip(")")
    test2 = test1 + ', ' + str(linkAlpha) + ')'
    test3 = test2.lstrip("rgb")
    test4 = 'rgba' + test3
    df1['colorLink'][x] = test4

for x in range(df1length):
    df1['colorNode'][x] = nodeColorManual

for x in range(df2length):
    test = str(df2['colorLink'][x])
    test1 = test.rstrip(")")
    test2 = test1 + ', ' + str(linkAlpha) + ')'
    test3 = test2.lstrip("rgb")
    test4 = 'rgba' + test3
    df2['colorLink'][x] = test4

for x in range(df2length):
    df2['colorNode'][x] = nodeColorManual


# creating a single dataframe from 3 dataframes
links = pd.concat([df1, df2], axis=0)

# Uncomment to troubleshoot. Prints values before Sankey
#print(links)

# Creates list / dictionary to prepare for sankey
unique_source_target = list(pd.unique(links[['source','target']].values.ravel('k')))
mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
links['source'] = links['source'].map(mapping_dict)
links['target'] = links['target'].map(mapping_dict)
links_dict = links.to_dict(orient='list')

# Automatically creates a graph name from columns
graphtitle = column1 + ' to ' + column2 + ' to ' + column3
# Orientation of graph
orientationvalue= "h" #(v = Vertical or h = Horizontal)

# This Creates the Sankey
fig = go.Figure(data=[go.Sankey(
    node = dict(label = unique_source_target,
                color =  links['colorNode']
                ), 
    orientation= orientationvalue, 
    link = dict(source= links_dict['source'], 
                target = links_dict['target'], 
                value = links_dict['value'],
                color = links['colorLink']
                )
            )
        ]
    )

# This makes small changes to the Sankey
fig.update_layout(title=graphtitle, 
                  autosize=False, 
                  width=pngwidth,
                  height=pngheight,
                  #font_family="Courier New",
                  font_color="black",
                  #font_size=15,
                  #title_font_family="Times New Roman",
                  #title_font_color="black"
                  )

# This Displays the Sankey
fig.show()

# Uncommnet for HTML File
#fig.write_html(graphtitle + ".html")Current