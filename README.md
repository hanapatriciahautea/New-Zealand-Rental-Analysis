# New-Zealand-Rental-Analysis
This group project is a part of the *Data Wrangling* `DATA422` course at the University of Canterbury. This course provides an introduction to Data Wrangling, also called Data Engineering, a critical
component of any Data Science project. [See Course Information](https://courseinfo.canterbury.ac.nz/GetCourseDetails.aspx?course=DATA422)

## The Datasets
### 1. AirBnB
This is the 19 June, 2026 New Zealand dataset from https://insideairbnb.com/get-the-data/

**Data Dictionary**
| Field Name | Data Type | Description |
|---|---|---|
| `id` | integer |Airbnb's unique identifier for the listing |
| `listing_url` | text<sup>1</sup> ||
| `scrape_id` | bigint<sup>1</sup> |Inside Airbnb "Scrape" this was part of |
| `last_scraped` | datetime<sup>1</sup> |UTC. The date and time this listing was "scraped". |
| `source` | text |One of "neighbourhood search" or "previous scrape". "neighbourhood search" means that the listing was found by searching the city, while "previous scrape" means that the listing was seen in another scrape performed in the last 65 days, and the listing was confirmed to be still available on the Airbnb site. |
| `name` | text |Name of the listing |
| `description` | text |Detailed description of the listing |
| `neighborhood_overview` | text |Host's description of the neighbourhood |
| `picture_url` | text |URL to the Airbnb hosted regular sized image for the listing |
| `host_id` | integer |Airbnb's unique identifier for the host/user |
| `host_url` | text<sup>1</sup> |The Airbnb page for the host |
| `host_name` | text |Name of the host. Usually just the first name(s). |
| `host_since` | date |The date the host/user was created. For hosts that are Airbnb guests this could be the date they registered as a guest. |
| `host_location` | text |The host's self reported location |
| `host_about` | text |Description about the host |
| `host_response_time` |  ||
| `host_response_rate` |  ||
| `host_acceptance_rate` |  |That rate at which a host accepts booking requests. |
| `host_is_superhost` | boolean ||
| `host_thumbnail_url` | text ||
| `host_picture_url` | text ||
| `host_neighbourhood` | text ||
| `host_listings_count` | text |The number of listings the host has (per Airbnb unknown calculations) |
| `host_total_listings_count` | text |The number of listings the host has (per Airbnb unknown calculations) |
| `host_verifications` |  ||
| `host_has_profile_pic` | boolean ||
| `host_identity_verified` | boolean ||
| `neighbourhood` | text ||
| `neighbourhood_cleansed` | text<sup>1</sup> |The neighbourhood as geocoded using the latitude and longitude against neighborhoods as defined by open or public digital shapefiles. |
| `neighbourhood_group_cleansed` | text<sup>1</sup> |The neighbourhood group as geocoded using the latitude and longitude against neighborhoods as defined by open or public digital shapefiles. |
| `latitude` | numeric |Uses the World Geodetic System (WGS84) projection for latitude and longitude. |
| `longitude` | numeric |Uses the World Geodetic System (WGS84) projection for latitude and longitude. |
| `property_type` | text |Self selected property type. Hotels and Bed and Breakfasts are described as such by their hosts in this field |
| `room_type` | text |[Entire home/apt|Private room|Shared room|Hotel]All homes are grouped into the following three room types:Entire placePrivate roomShared roomEntire placeEntire places are best if you're seeking a home away from home. With an entire place, you'll have the whole space to yourself. This usually includes a bedroom, a bathroom, a kitchen, and a separate, dedicated entrance. Hosts should note in the description if they'll be on the property or not (ex: "Host occupies first floor of the home"), and provide further details on the listing.Private roomsPrivate rooms are great for when you prefer a little privacy, and still value a local connection. When you book a private room, you'll have your own private room for sleeping and may share some spaces with others. You might need to walk through indoor spaces that another host or guest may occupy to get to your room.Shared roomsShared rooms are for when you don't mind sharing a space with others. When you book a shared room, you'll be sleeping in a space that is shared with others and share the entire space with other people. Shared rooms are popular among flexible travelers looking for new friends and budget-friendly stays. |
| `accommodates` | integer |The maximum capacity of the listing |
| `bathrooms` | numeric |The number of bathrooms in the listing |
| `bathrooms_text` | string |The number of bathrooms in the listing. On the Airbnb web-site, the bathrooms field has evolved from a number to a textual description. For older scrapes, bathrooms is used. |
| `bedrooms` | integer |The number of bedrooms |
| `beds` | integer |The number of bed(s) |
| `amenities` | json ||
| `price` | currency |daily price in local currency.NOTE: the $ sign is a technical artifact of the export, please ignore it |
| `minimum_nights` | integer |minimum number of night stay for the listing (calendar rules may be different) |
| `maximum_nights` | integer |maximum number of night stay for the listing (calendar rules may be different) |
| `minimum_minimum_nights` | integer<sup>1</sup> |the smallest minimum_night value from the calender<sup>2</sup> |
| `maximum_minimum_nights` | integer<sup>1</sup> |the largest minimum_night value from the calender<sup>2</sup> |
| `minimum_maximum_nights` | integer<sup>1</sup> |the smallest maximum_night value from the calender<sup>2</sup> |
| `maximum_maximum_nights` | integer<sup>1</sup> |the largest maximum_night value from the calender<sup>2</sup> |
| `minimum_nights_avg_ntm` | numeric<sup>1</sup> |the average minimum_night value from the calender<sup>2</sup> |
| `maximum_nights_avg_ntm` | numeric<sup>1</sup> |the average maximum_night value from the calender<sup>2</sup> |
| `calendar_updated` | date ||
| `has_availability` | boolean |[t=true; f=false] |
| `availability_30` | integer<sup>1</sup> |avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host. |
| `availability_60` | integer<sup>1</sup> |avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host. |
| `availability_90` | integer<sup>1</sup> |avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host. |
| `availability_365` | integer<sup>1</sup> |avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host. |
| `calendar_last_scraped` | date ||
| `number_of_reviews` | integer |The number of reviews the listing has |
| `number_of_reviews_ltm` | integer<sup>1</sup> |The number of reviews the listing has (in the last 12 months) |
| `number_of_reviews_l30d` | integer<sup>1</sup> |The number of reviews the listing has (in the last 30 days) |
| `first_review` | date<sup>1</sup> |The date of the first/oldest review |
| `last_review` | date<sup>1</sup> |The date of the last/newest review |
| `review_scores_rating` |  ||
| `review_scores_accuracy` |  ||
| `review_scores_cleanliness` |  ||
| `review_scores_checkin` |  ||
| `review_scores_communication` |  ||
| `review_scores_location` |  ||
| `review_scores_value` |  ||
| `license` | text |The licence/permit/registration number |
| `instant_bookable` | boolean |[t=true; f=false]. Whether the guest can automatically book the listing without the host requiring to accept their booking request. An indicator of a commercial listing. |
| `calculated_host_listings_count` | integer<sup>1</sup> |The number of listings the host has in the current scrape, in the city/region geography. |
| `calculated_host_listings_count_entire_homes` | integer<sup>1</sup> |The number of Entire home/apt listings the host has in the current scrape, in the city/region geography |
| `calculated_host_listings_count_private_rooms` | integer<sup>1</sup> |The number of Private room listings the host has in the current scrape, in the city/region geography |
| `calculated_host_listings_count_shared_rooms` | integer<sup>1</sup> |The number of Shared room listings the host has in the current scrape, in the city/region geography |
| `reviews_per_month` | numeric<sup>1</sup> |The average number of reviews per month the listing has over the lifetime of the listing.Psuedocoe/~SQL:IF scrape_date - first_review <= 30 THEN number_of_reviewsELSE number_of_reviews / ((scrape_date - first_review + 1) / (365/12)) |
    
*Notes:* <sup>1</sup>Calculated from other fields. <sup>2</sup>Looking 365 nights in the future.

# References & Sources
1. [Airbnb NZ Dataset of 19-June-2026](https://data.insideairbnb.com/new-zealand/2026-06-19/visualisations/listings.csv)
2. [Data dictionary for Airbnb Dataset](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing)
