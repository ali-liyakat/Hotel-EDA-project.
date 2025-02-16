import pandas as pd
import matplotlib.pyplot as plt



# Data Exploration


df_bookings = pd.read_csv('datasets/fact_bookings.csv')
print(df_bookings.head())
print(df_bookings.shape)
print(df_bookings.room_category.unique())
print(df_bookings.booking_platform.unique())
print(df_bookings.booking_platform.value_counts().plot(kind='bar'))
plt.show()
print(df_bookings.describe())


df_date = pd.read_csv("datasets/dim_date.csv")
df_hotels = pd.read_csv("datasets/dim_hotels.csv")
df_rooms = pd.read_csv("datasets/dim_rooms.csv")
df_agg_bookings = pd.read_csv("datasets/fact_aggregated_bookings.csv")

print(df_hotels.head())
print(df_hotels.category.value_counts())
print(df_hotels.city.value_counts().sort_values().plot(kind='bar'))
plt.show()


# Data Cleaning
# remove negative values
print(df_bookings[df_bookings.no_guests <= 0])

df_bookings = df_bookings[df_bookings.no_guests > 0]
print(df_bookings.shape)


print(df_bookings.revenue_generated.min(), df_bookings.revenue_generated.max())

avg, std = df_bookings.revenue_generated.mean(), df_bookings.revenue_generated.std()
print(avg, std)

higher_limit = avg + 3 * std
print(higher_limit)

lower_limit = avg - 3 * std
print(lower_limit)


# Removing outliers

df_bookings = df_bookings[df_bookings.revenue_generated < higher_limit]
print(df_bookings.shape)

print(df_bookings.revenue_realized.describe())

higher_limit = df_bookings.revenue_realized.mean() + 3 * df_bookings.revenue_realized.std()
print(higher_limit)

print(df_bookings[df_bookings.revenue_realized > higher_limit])

print(df_rooms)


# higher limit for RT4

print(df_bookings[df_bookings.room_category == "RT4"]. revenue_realized.describe())

print(23439 + 3 * 9048)

# Handling Null values
print(df_bookings.isnull().sum())


# Data Transformation

print(df_agg_bookings.head())

df_agg_bookings["Occ_pct"] =  df_agg_bookings["successful_bookings"] / df_agg_bookings["capacity"]
print(df_agg_bookings.head())

df_agg_bookings["Occ_pct"] = df_agg_bookings["Occ_pct"].apply(lambda x: round(x * 100, 2))
print(df_agg_bookings.head())


# Q1: Average occupancy rate in each of room categories.

df = pd.merge(df_agg_bookings, df_rooms, left_on="room_category", right_on="room_id")
print(df.head())
df.drop("room_id", axis=1, inplace=True)
print(df.groupby("room_class")["Occ_pct"].mean().round(2).plot(kind="bar"))
plt.title("Average Occupancy Rate for Each Room Category.")
plt.show()


# Q2 Print Average occupancy rate per city

print(df_hotels.head())
df= pd.merge(df, df_hotels, on="property_id")
print(df.head())

print(df.groupby("city")["Occ_pct"].mean().plot(kind="bar"))
plt.title("Average Occupancy Rate per City.")
plt.show()

# Q3 When was Occupancy better? Weekday or Weekend?

print(df_date.head())

df = pd.merge(df, df_date, left_on="check_in_date", right_on="date")
print(df.groupby("day_type")["Occ_pct"].mean().round(2).plot(kind="bar"))
plt.title("Better Occupancy Analysis")
plt.show()


# Q4 In June month, What was Occupancy in different cities?

print(df["mmm yy"].unique())

df_june_22 = df[df["mmm yy"]=="Jun 22"]
print(df_june_22.head(4))

print(df_june_22.groupby('city')['Occ_pct'].mean().round(2).sort_values(ascending=False).plot(kind="bar"))
plt.title("June Month Occupancy")
plt.show()

# Append August month data to existing data

df_august = pd.read_csv("datasets/new_data_august.csv")
print(df_august.head(4))

latest_df = pd.concat([df, df_august], ignore_index=True, axis=0)
print(latest_df.tail(4))

# Print Revenue Realized per city

df_bookings_all = pd.merge(df_bookings, df_hotels, on="property_id")
df_bookings_all.head(3)


print(df_bookings_all.groupby("city")["revenue_realized"].sum().plot(kind="bar"))
plt.title("Revenue Realized per City")
plt.show()

# print month by month revenue

print(df_bookings_all.head(4))

print(pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date"))

print(df_bookings_all.info())

print(df_date.info())

df_date["date"] = pd.to_datetime(df_date["date"])
print(df_date.head(3))

df_bookings_all["check_in_date"] = pd.to_datetime(df_bookings_all["check_in_date"], dayfirst=True, errors='coerce')
print(df_bookings_all.head(4))

df_bookings_all = pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date")
print(df_bookings_all.head(4))

print(df_bookings_all.groupby("mmm yy")["revenue_realized"].sum().plot(kind="bar"))
plt.title("Month by Month Revenue")
plt.show()

# print Revenue Realized per Hotel type

df_bookings_all.property_name.unique()
print(df_bookings_all.groupby("property_name")["revenue_realized"].sum().round(2).sort_values().plot(kind="bar"))
plt.title("Revenue Realized per hotel type")
plt.show()

# print average rating per day

print(df_bookings_all.groupby("city")["ratings_given"].mean().round(2).plot(kind="bar"))
plt.title("Average rating per day")
plt.show()


# Revenue Realized per Booking platform

print(df_bookings_all.groupby("booking_platform")["revenue_realized"].sum().plot(kind="pie").plot(kind="bar"))
plt.title("Revenue Realized per Booking Platform")
plt.show()