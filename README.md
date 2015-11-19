# Rossmann-Store-Sale

## Timeline
|Days reminding|Date|Event|
|-----|-----|-----|
|14|11.18| Have Chosen the task|
|13|11.21| |
|12|11.20| |
|11|11.21| |
|10|11.22| |
|9|11.23| |
|8|11.24| |
|7|11.25| |
|6|11.26| |
|5|11.27| |
|4|11.28| |
|3|11.29| |
|2|11.30| Write the report|
|1|12.01| Deadline|


## Data Format

The data is a [{}].

Every list represents a line in data file.
In every list, you can use data[i]['Sales'] to choose the attribute you want.


**Example of data[i]:**

{'DayOfWeek': 5, 'Customers': 625, 'StateHoliday': '0', 'Promo': 1, 'Sales': 6064, 'Date': '2015-07-31', 'Open': 1, 'SchoolHoliday': '1', 'Store': 2}

'Store' is int

'DayOfWeek' is int

'Date' is string

'Sales' is int

'Customers' is int 

'Open' is int

'StateHoliday' is string

'SchoolHoliday' is string



## NOTICE
There are some mistake in data file (test.csv). I have found the solution in the official forums ([here](https://www.kaggle.com/c/rossmann-store-sales/forums/t/16835/open-is-blank-in-test-file-for-store-622)) and I have fixed it. Please use the data files in the Github.


## Reference
[How to read and write .csv in python](https://docs.python.org/2/library/csv.html)