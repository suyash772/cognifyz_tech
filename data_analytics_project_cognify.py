import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from sklearn.cluster import DBSCAN

data = pd.read_csv("D:/download/congnifz_tech.csv")
df = pd.DataFrame(data)
pd.set_option('display.max_columns', 50)
print(df.head())
print("*"*100)

print(data.info())
print("*"*100)

print(data.isnull().sum())
print("*"*100)

print(data.duplicated().sum())
print(data.shape)
print("*"*200)

print("          ~~~~~~~~~~~~~~~~~ LEVEL 1~~~~~~~~~~~~~~~~~~~~~~~~~~                                    ")
print("*"*200)


print()
print("                             task 1                                           ")

print("                Q1>>>>>>>> determine top 3 most common cuisine types                       ")
print()
print()

Cuisines_counts = data['Cuisines'].value_counts()
print(Cuisines_counts)
print()

print("                           top 3 cusines are:                                ")
top_cusines= Cuisines_counts.head(3)
print(top_cusines)
print()

print("                           count of total resturants                          ")
rasturants_counts = len('Restaurant Name ')
print(rasturants_counts)
print()



print("              Q2>>>>>>>>>> percent of resturant that servers each of top cuisines                 ")
print()
print("North Indian: 9.80021 ")
print("North Indian, Chinese: 5.350255")
print("Chinese : 3.706418")
print()
print("*"*200)
print()



print("                             task 2                                          ")
print("              Q1>>>>>>  identify city with highest no of resturants                         ")
print()
print()
city_count= print(data['City'].value_counts().head(1))
print()


print("             Q2 >>>>>>> calculate average rating for rasturants in each city                   ")
print()
average_ratings = data.groupby('City')['Aggregate rating'].mean()
print(average_ratings)
print()


print("             Q3>>>>>>>> determine city with highest average rating of resturants                 ")
print()
highest_avg_rating = data.groupby('City')['Aggregate rating'].max().head(3)
print(highest_avg_rating)
print()
print("*"*200)
print()



print("                             task 3                                                ")
print("             Q1>>>>>>>>> create a histogram or bar chart to visualize distribution of price range among resturant            ")

price_counts = df['Price range'].value_counts()

plt.figure(figsize=(8, 6))
price_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution of Price Ranges Among Restaurants')
plt.xlabel('Price Range')
plt.ylabel('Number of Restaurants')
plt.xticks(rotation=0)  # Rotate x labels if necessary
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
print()


print("            Q2>>>>>>>  Calculate the percentage of restaurants in each price range category                                     ")
total_restaurants = price_counts.sum()
print(total_restaurants)

price_percentages = (price_counts / total_restaurants) * 100
print(price_percentages)
print("*"*200)
print()


print("                                    task 4                                        ")
print("                       Q1>>>>>>> Determine the percentage of restaurants  that offer online delivery                        ")

total_restaurants = len(df)
print("total_restuiarant",total_restaurants)

delivery_restaurants = df['Has Online delivery'].str.lower().eq('yes').sum()
print("online delivery restaurant",delivery_restaurants)

percentage_delivery = (delivery_restaurants / total_restaurants) * 100
print(f'Percentage of restaurants offering online delivery: {percentage_delivery:.2f}%')
print()


print("                        Q2>>>>>>>>>> Compare the average ratings of restaurants with and without online delivery                                  ")

data['Has Online delivery  '] = data['Has Online delivery'].str.lower()
print(data['Has Online delivery  '].value_counts())
print()

data['Is delivering now '] =data['Has Online delivery'  ].map({'yes': 'Has Online delivery ', 'no': 'Offline Delivery'})
print(data['Is delivering now '].value_counts())
print()

average_ratings = df.groupby('Has Online delivery')['Aggregate rating'].mean()
print("average rating of online delivery and offline ",average_ratings)
print()
print("*"*200)
print()



print()
print("*"*200)
print("          ~~~~~~~~~~~~~~~~~~~~~ LEVEL 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~                                           ")
print("*"*200)
print()
print("                                Task 1                                                ")
print()
print("                Q1   analyze the distribution of aggregate rating and determine most common rating range         " )
print("                      create the histogram to see distribution of aggregate rating                                   ")

plt.figure(figsize=(8,6))
plt.hist(df['Aggregate rating'], bins=10,edgecolor='k')
plt.xlabel("Aggregate rating")
plt.ylabel("number of restaurants")
plt.title("distribution  of aggregate rating")
plt.show()
print()

# determine the most common rating range
most_common_rating_range= df['Aggregate rating'].mode()
print("most_common_rating_range : ",most_common_rating_range.values[0])
print()



print("                 Q2    calculate average number of vote received by resturant             ")
print()
avg_votes = df['Votes'].mean()
print("avg number of votes received by resturants : ",round(avg_votes,2))
print()
print("*"*200)
print()




print("                                    TASK 2                                                      ")
print()
print("                   Q1  identify the most common combo of cuision in set                      ")
#  Drop the rows with missing or empty cuisions
df.dropna(subset=['Cuisines'],inplace=True)

#split the cuisions column to get individual customer
cuisine_combinations = df['Cuisines'].str.split(',  ')

#flatten the list of cuiines combinations
all_cuisines= [cuisine for sublist in cuisine_combinations for cuisine in sublist]

#calculate the most common cuision combination
common_cuisine_combinations= pd.Series(all_cuisines).value_counts()

#display most common combinations
print("most common combinations of cuisions:")
print(common_cuisine_combinations.head(10))
print()


print("                      Q2  calculate the average rating for each cuisions combination                          ")
print()
average_ratings = df.groupby('Cuisines')['Aggregate rating'].mean()

#sort the combination by average rating in descending order
sorted_combinations = average_ratings.sort_values(ascending=False)

#display the top rated cuisions combinations
print("Top rated cuisions combinations: ")
print(sorted_combinations.head(5))
print()
print("*"*200)
print()




print("                                 TASk 3                                              ")
print()
print("               Q1 plot the location of resturants on map using longitude and latitude coordination              ")
print("               Q2  identify any pattern or cluster of resturant in specific areas                               ")

# create a map cenetered at a specific location(e.g, city centre
m= folium.Map(location=[72.829976, 19.12663], zoom_start=2)

#create marker cluster group
marker_cluster= MarkerCluster().add_to(m)

# add marker for resturant location to cluster group
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'],row['Longitude']],
    ).add_to(marker_cluster)

#display the map
m.save('resturant_map.html')

#extract latitude and longitude coordination
x= df[["Latitude","Longitude"]]



#apply dbscan clusturing
eps=0.1 #adjust the epsile value based on your data
min_simples= 5  # adjust the minimum no of sample based on your data
db=DBSCAN(eps=eps,min_samples=min_simples).fit(x)

#add cluster  label
df['Cluster']=db.labels_

#create a map centered at a specific location(eg., city centre)
m=folium.Map(location=[72.829976, 19.12663], zoom_start=2)

#create a maker cluster group
marker_cluster= MarkerCluster().add_to(m)

#add marker for resturants location with cluster labels
for index, row in df.iterrows():
    if row['Cluster'] != -1:
        folium.Marker(
            location=[row['Latitude'],row['Longitude']],
            popup=f"Restaurant: {row['Restaurant Name']},Cluster:{row['Cluster']}",
        ).add_to(marker_cluster)

#display the map
m.save('Clustered_resturant_map.html')
print()
print("*"*200)
print()




print("                                    TASK 4                                                      ")
print()
print("                            Q1 identify if there are any resturant chain present in  set                          ")
#Group resturants by name and count the number of location
chain_counts= df['Restaurant Name'].value_counts()

#filter chain by specifiying a minimun number of locations
min_chain_locations = 2 # adjust as needed
restaurant_chains= chain_counts[chain_counts>=min_chain_locations].index.tolist()

#print the list of resturants chain
print("Restaurant chains : ")
print(restaurant_chains)
print()

#Top 10 restaurant chain who has highest number of chain
#filter for restaurant that apper more than once(potential chain)
restaurant_chains= chain_counts[chain_counts>1]

if not restaurant_chains.empty:
    print("Restaurant chains Identified: ")
    print(restaurant_chains.head(10))
else:
    print("Restaurant chains not Identified: ")
print()




print("                               Q2 analyze rating and popularity of diffrent resturant chains                        ")
# filter the data frame to include only rows for resturant chains
chain_df= df[df["Restaurant Name"].isin(restaurant_chains)]

#calculate average rating for each chain
chain_ratings = chain_df.groupby('Restaurant Name')['Aggregate rating'].mean()

#calculate the total number of votes received by each chain
chain_votes= chain_df.groupby('Restaurant Name')['Votes'].sum()

#combine the rating and votes into single dataframe
chain_stats= pd.DataFrame({'Average Rating': chain_ratings, 'Total Count': chain_votes})

#sort the chain by average rating or total votes as needed
chain_stats= chain_stats.sort_values(by='Average Rating',ascending=False)

#print
print("Restaurant chain rating and Popularity: ")
print(chain_stats)
print()
print()

print("*"*200)
print()
print("                                     ~~~~~~~~~~~~~~~~~~~~~~~~~~ THANK YOU ~~~~~~~~~~~~~~~~~~~~~~~~~~~                         ")
print()
print("*"*200)
