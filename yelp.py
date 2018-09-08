from yelpapi import YelpAPI

API_KEY= "bhKO-6PHuMI5XAJZg_AdiHe6a3yd3YLOP__iRbqNUCcV4TPWjtZNd_DpZ_H5K9hj45igcZrjzJEwRwZ_o7GH8M676M10RISkJCO4oxWdTEOQhCRc-iLnozk5rueJW3Yx"

yelp = YelpAPI(API_KEY)
search = yelp.search_query(longitude=-122.4392, latitude=37.7474)
