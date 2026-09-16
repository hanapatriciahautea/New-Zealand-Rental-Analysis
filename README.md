# New-Zealand-Rental-Analysis
This group project is a part of the *Data Wrangling* `DATA422` course at the University of Canterbury. This course provides an introduction to Data Wrangling, also called Data Engineering, a critical
component of any Data Science project. [See Course Information](https://courseinfo.canterbury.ac.nz/GetCourseDetails.aspx?course=DATA422)

The data comes from  *insideairbnb.com* - a mission driven project that provides data and advocacy about Airbnb's impact on residential communities ([Cox, n.d.](#cox-nd)).

## The Datasets
### 1. AirBnB
The New Zealand-specific dataset was published on the 19 June, 2026 ([Cox, 2026](#cox-2026)).

**Data Dictionary** [Cox (2022)](#cox-2022)  
| Field Name | Data Type | Description |
|---|---|---|
| `availability_365` | integer<sup>1</sup> |The availability of the listing x days in the future as determined by the calendar. <br> Note a listing may not be available because it has been booked by a guest or blocked by the host. |
| `calculated_host_listings_count` | integer<sup>1</sup> | The number of listings the host has in the current scrape, in the city/region geography. |
| `host_id` | integer | Airbnb's unique identifier for the *host/user*. |
| `host_name` | text | Name of the host, usually just the first name(s). |
| `id` | integer | Airbnb's unique identifier for the *property listing*. |
| `last_review` | date<sup>1</sup> | The date of the last/newest review. |
| `latitude` | numeric | Uses the World Geodetic System (WGS84) projection for latitude and longitude. |
| `longitude` | numeric | Uses the World Geodetic System (WGS84) projection for latitude and longitude. |
| `minimum_nights` | integer | Minimum number of night stay for the listing (calendar rules may be different). |
| `name` | text | Name of the listing. |
| `neighbourhood` | text ||
| `neighbourhood_group_cleansed` | text<sup>1</sup> | The neighbourhood group as geocoded using the latitude and longitude against neighborhoods as defined by open or public digital shapefiles. |
| `number_of_reviews` | integer | The number of reviews for the property listing. |
| `number_of_reviews_ltm` | integer<sup>1</sup> | The number of reviews the listing has in the last 12 months. |
| `price` | currency | Daily price in local currency. **NOTE:** the `$` sign is a technical artifact of the export, please ignore it |
| `reviews_per_month` | numeric<sup>1</sup> | The average number of reviews per month the listing has over the lifetime of the listing. |
| `room_type` | text |All homes are grouped into `Entire place`, `Private room`, `Shared room`. For more description of these labels, see the source dataset's [data dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing) |

*Notes:* <sup>1</sup>Calculated from other fields. <sup>2</sup>Looking 365 nights in the future.


# References & Sources  
<a id="cox-nd"></a>Cox, M. (n.d.). *Get the data*. InsideAirbnb. Retrieved July 30, 2026,  [https://insideairbnb.com/get-the-data/](https://insideairbnb.com/get-the-data/)  

<a id="cox-2026"></a>Cox, M. (2026, June 19). *listings.csv*. Retrieved July 30, 2026, [https://data.insideairbnb.com/new-zealand/2026-06-19/visualisations/listings.csv](https://data.insideairbnb.com/new-zealand/2026-06-19/visualisations/listings.csv)  

<a id="cox-2022"></a>Cox, M. (2022, August). *Inside Airbnb Data Dictionary.xlsx*. Retrieved July 30, 2026, [https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?gid=1322284596#gid=1322284596](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?gid=1322284596#gid=1322284596)  
