from recipes.models import Recipe
from io import BytesIO 
import base64
import matplotlib.pyplot as plt

def get_recipename_from_id(val):
   #this ID is used to retrieve the name from the record
   recipename=Recipe.objects.get(id=val)
   #and the name is returned back
   return recipename

def get_graph():
   buffer = BytesIO()
   #create plot with byte object
   plt.savefig(buffer, format = 'png')
   buffer.seek(0) #set cursor to start of stream
   image_png = buffer.getvalue() #retrieve content of file
   graph = base64.b64encode(image_png) #encode
   graph = graph.decode('utf-8') #decode
   buffer.close()
   return graph

def get_chart(chart_type, data, **kwargs):
   #switch plot backend to AGG, to write to file
   plt.switch_backend('AGG')
   fig = plt.figure(figsize = (6,3)) #configure 

   #select chart type and configure based on user choice
   if chart_type == '#1':
      plt.bar(data['difficulty'], data['cooking_time'])
   
   plt.tight_layout() #layout details
   chart = get_graph()
   return chart

