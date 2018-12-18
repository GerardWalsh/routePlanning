import numpy as np
import googlemaps as maps
from itertools import permutations

print "Please enter you Google Maps API key. If need be, register for the Maps, Routes and Places APIs here:\n"
print 'https://cloud.google.com/maps-platform/?__utma=102347093.467734242.1544379651.1545148171.1545148171.1&__utmb=102347093.0.10.1545148171&__utmc=102347093&__utmx=&__utmz=102347093.1545148171.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organicutmctr=(not%20provided)&__utmv=-&__utmk=124520586&_ga=2.126537550.214108381.1545047640-467734242.1544379651#get-started'

#API key
userKey = str(raw_input('\nAPI key:'))
gmap = maps.Client(key = userKey)
#Author's key : AIzaSyAgO_1n-Vb_copaVuGp-yq2y-zEBFXXLQQ

#Store locations
deliveryLocations = ['115 St Andrews Drive, Durban North, KwaZulu-Natal, South Africa', 
'67 Boshoff Street, Pietermaritzburg, KwaZulu-Natal, South Africa', 
'4 Paul Avenue, Fairview, Empangeni, KwaZulu-Natal, South Africa',
'166 Kerk Street, Vryheid, KwaZulu-Natal, South Africa', 
'9 Margaret Street, Ixopo, KwaZulu-Natal, South Africa', 
'16 Poort Road, Ladysmith, KwaZulu-Natal, South Africa']

#function returns location coordinates
def coords(address):
	location = gmap.geocode(address)
	latitude = location[0]["geometry"]["location"]["lat"]
	longitude = location[0]["geometry"]["location"]["lng"]
	return (str(latitude) + ',' + str(longitude))

#Populate matrix with distances 
locationCount  = len(deliveryLocations)
distanceMatrix = np.zeros((locationCount, locationCount, 2))

for i in range(0, locationCount):

	origin = coords(deliveryLocations[i])

	for j in range(0, locationCount):

		destination = coords(deliveryLocations[j])
		directions_result = gmap.directions(origin, destination, mode="driving")

		if (i == j):
			distanceMatrix[i][j][0] = np.inf	
			distanceMatrix[i][j][1] = np.inf
		else:
			distanceMatrix[i][j][0] = directions_result[0]['legs'][0]['distance']['value']
			distanceMatrix[i][j][1] = directions_result[0]['legs'][0]['duration']['value']

combinations = list(permutations([0, 1, 2, 3, 4, 5]))

shortestDistance = 10000000000
shortestDuration = 10000000000
distance = 0
duration = 0
store = 10000000

#Brute force the shortest distance
for i in range(0, len(combinations)):

	j = 0

	while j < 5:
		start = combinations[i][j]
		next = combinations[i][j+1]
		dist = distanceMatrix[start][next][0]
		duration = distanceMatrix[start][next][1]
		distance += dist
		duration += duration
		j += 1


	if distance < shortestDistance:
		shortestDistance = distance
		shortestDuration = duration
		store = i
		distance = 0
	else:
		distance = 0
route = combinations[store]

print ("\nThe shortest trip time is: "+str(int(shortestDuration/60))+"mins, with a distance of: "+str(int(shortestDistance/1000))+"km\n")
print "Route order:"
for l in range(0, 6):
	print (deliveryLocations[route[l]])

#Generate url to plot route
center = 'KwaZulu-Natal'
urlStart = 'https://maps.googleapis.com/maps/api/staticmap?center='
mapZoom = '&zoom=7&size=1280x920&maptype=roadmap'
marker = '&markers=color:blue%7Clabel:'
locationNumber = '%7C'
path = '&path=color:blue|weight:5|'
key = '&key=AIzaSyAgO_1n-Vb_copaVuGp-yq2y-zEBFXXLQQ'

newUrl = urlStart+center+mapZoom

#Append the url with successive locations
for j in range(0, (len(route)-1)):
	newUrl = newUrl + marker + str(j+1) + locationNumber + coords(deliveryLocations[route[j]]) + path + coords(deliveryLocations[route[j]])+ '|'+ coords(deliveryLocations[route[j+1]])

newUrl = newUrl +  marker + str(len(route)) + locationNumber+ coords(deliveryLocations[route[5]]) + key

print "\nThe map is depicting the optimal route can be found at the following url: \n"
print newUrl







