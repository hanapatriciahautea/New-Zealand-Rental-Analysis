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


### 2. Rental bond data
The rental bond dataset was published by the The Ministry of Business, Innovation and Employment and made available on their Tenancy Services website. The data has been last updated on 10th September 2026 and it has been retrieve for this project on 10th September 2026. Specifically, the "Detailed quarterly report, January 2020 to April 2026" is used here ([The Ministry of Business, Innovation and Employment, 2026](#MBIE-2026)).

Note: The dataset uses Statistical Area 2 2019 (SA2-2019), which is a set of geographic boundaries as defined by Stats NZ and used for reporting population and demographic data ([Stats NZ, 2026](#StatsNZ-2026)).
'The SA2 geography aims to reflect communities that interact together socially and economically. In populated areas, SA2s generally contain similar-sized populations. SA2s in city council areas generally have a population of 2,000–4,000 residents while SA2s in district council areas generally have a population of 1,000–3,000 residents.' ([Stats NZ, 2019](#StatsNZ-2019))

For the translation of SA2-Code into city name, the "Dwellings dataset" from Christchurch City Council has been used. ([Christchurch City Council, n.d.](#CCC-nd))

**Data Dictionary** 
| Field Name | Data Type | Description |
|---|---|---|
|`TimeFrame`| text -> should be date | Reporting quarter, e.g. April 2026 = represents January, February, and March 2026. Data format: 01.04.2026 = DD.MM.YYYY |
|`Location Id`| text -> should be numeric | Geographic identifier. Six digit code. First number refers to island (North Island = 1,2 / South Island = 3). |
|`Dwelling Type`| text | Classification of the property. Available types: ALL, Apartment, Boarding House, Flat, House, Room. |
|`Number Of Beds`| text -> should be numeric | Number of bedrooms in the rental.|
|`Total Bonds`| numeric | The aggregate number of bonds processed, lodged, or accounted for during the defined time frame for that location and dwelling category.sup>3</sup> |
|`Active Bonds`| numeric | The count of rental bonds currently held by Tenancy Services that remain live and operational at the time the data snapshot was generated.<sup>3</sup> |
|`Closed Bonds`| numeric | The total count of rental bonds that were refunded, released, or officially closed out during the specified reporting timeframe.<sup>3</sup> |
|`Median Rent`| text -> should be numeric | Midpoint price of weekly rent entries. Exactly half of the properties are rented for more than this amount, and half for less. |
|`Geometric Mean Rent`| text -> should be numeric | Average of rental bond in NZD calculated by taking the nth root of the product of rental bonds. |
|`Upper Quartile Rent`| text -> should be numeric | 25th percentile meaning 25% of the rental bonds in NZD fall below this number and 75% fall above this number |
|`Lower Quartile Rent`| text -> should be numeric | 75th percentile meaning 75% of the rental bonds in NZD fall below this number and 25% fall above this number |
|`Log Std Dev Weekly Rent`| text -> should be numeric | The standard deviation of the natural logarithm of weekly rents. This is a statistical metric used to evaluate the relative dispersion or variance of rental costs within the sample, normalizing for scale across different price levels.<sup>3</sup> |

*Notes:* <sup>3</sup>Definition of marked items created with supportof Google Gemini due to lack of information or clarity on website.

## License
The Airbnb raw data is made available under a Creative Commons license by InsideAirbnb: [https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/).

The rental bond raw data is made available under a Creative Commons license by The Ministry of Business, Innovation and Employment: [https://creativecommons.org/licenses/by/3.0/nz/](https://creativecommons.org/licenses/by/3.0/nz/).

# References & Sources  
<a id="cox-nd"></a>Cox, M. (n.d.). *Get the data*. InsideAirbnb. Retrieved July 30, 2026, from [https://insideairbnb.com/get-the-data/](https://insideairbnb.com/get-the-data/)  

<a id="cox-2026"></a>Cox, M. (2026, June 19). *listings.csv*. Retrieved July 30, 2026, from [https://data.insideairbnb.com/new-zealand/2026-06-19/visualisations/listings.csv](https://data.insideairbnb.com/new-zealand/2026-06-19/visualisations/listings.csv)  

<a id="cox-2022"></a>Cox, M. (2022, August). *Inside Airbnb Data Dictionary.xlsx*. Retrieved July 30, 2026, from [https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?gid=1322284596#gid=1322284596](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?gid=1322284596#gid=1322284596)  

<a id="MBIE-2026"></a>The Ministry of Business, Innovation and Employment. (2026, September 10). *Rental bond data*. Retrieved September 10, 2026, from [https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/)

<a id="StatsNZ-2026"></a>Stats NZ. (2026, September 3). *Statistical Area 2 2019 (generalised)*. Retrieved September 10, 2026, from [https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/](https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/)

<a id="StatsNZ-2019"></a>Stats NZ. (2019, July 25). *Statistical Area 2 2029 V1.0.0*. Retrieved September 10, 2026, from [https://aria.stats.govt.nz/aria/?_ga=2.64351014.862326229.1560897363-450849000.1560897363#ClassificationView:uri=http://stats.govt.nz/cms/ClassificationVersion/VxisJjBFG2PtagMo](https://aria.stats.govt.nz/aria/?_ga=2.64351014.862326229.1560897363-450849000.1560897363#ClassificationView:uri=http://stats.govt.nz/cms/ClassificationVersion/VxisJjBFG2PtagMo)

<a id="CCC-nd"></a>Christchurch City Council. (n.d.). *Christchurch and Canterbury census data*. Retrieved September 14, 2026, from: [https://ccc.govt.nz/culture-and-community/statistics-and-facts/census-data](https://ccc.govt.nz/culture-and-community/statistics-and-facts/census-data)