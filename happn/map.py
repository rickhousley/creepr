import pygmaps 
import webbrowser 
mymap = pygmaps.maps(37.428, -122.145, 16)
mymap.addpoint(37.427, -122.145, "#0000FF") 
mymap.draw('mymap.draw.html') 
url = 'mymap.draw.html'
webbrowser.open_new_tab(url) 