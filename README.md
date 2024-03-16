# Sales Data Analysis Project 
## Overview 
This project is designed to manage and analyze sales data for a retail store. It uses the Peewee ORM for database operations, connecting to a PostgreSQL database to store and manipulate sales data. The application imports sales data from a JSON file into the database and provides a functionality to display sales report charts based on the most sold items. The reports can be generated by running the program with specific command-line arguments. 

## Features 
- Database Management: Utilizes Peewee ORM for efficient operations on a PostgreSQL database, including creating tables for sales data.
- Data Import: Features an import functionality to load sales data from a JSON file into the database.
- Sales Reports: Generates visual sales report charts for the most sold items when the application is run with the -r or --report command-line argument.
## Getting Started

### Prerequisites - Python 3.6 or newer. - PostgreSQL database.

### Installation

1. Clone the project repository: 

```
git clone 
```

2. Change to the project directory: 

```
cd
``` 

3. Install the required dependencies: 

```
pip install -r requirements.txt
```

### Configuring the Database 
1. Create a new PostgreSQL database for the project.
2. Copy sample_setting.py to local_setting.py.
3. Edit local_setting.py following the provided guidelines to configure your database connection.

### Running the Application To run the application and generate sales report charts, use: 

```
python main.py -r
```

or 

```
python main.py --report
```

This will execute the program and display the sales report charts based on the most sold items. 
## Contributing
Contributions to this project are welcome! Feel free to fork the repository, make your changes, and submit a pull request. If you encounter any issues or have suggestions for improvements, please open an issue. 
