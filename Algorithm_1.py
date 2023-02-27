def find_preferred_city(city_distances, fuel, mpg):
    max_distance = 0
    preferred_city = None
    num_cities = len(city_distances)
    
    for i in range(num_cities):
        current_fuel = fuel[i]
        distance_traveled = 0
        j = i
        while current_fuel * mpg >= city_distances[j]:
            distance_traveled += city_distances[j]
            current_fuel -= city_distances[j] / mpg
            j = (j + 1) % num_cities
            if j == i:
                break
        
        if distance_traveled > max_distance:
            max_distance = distance_traveled
            preferred_city = i
    
    return preferred_city


city_distances = [5, 25, 15, 10, 15]
fuel = [1, 2, 1, 0, 3]
mpg = 10
print(find_preferred_city(city_distances, fuel, mpg))