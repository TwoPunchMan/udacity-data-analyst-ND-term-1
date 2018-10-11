import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while city not in CITY_DATA.keys():
        city = input('Enter a city: ').lower()
        if city not in CITY_DATA:
            print("Invalid input!")

    # TO DO: get user input for month (all, january, february, ... , june)
    months = {'all': 0, 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
              'june': 6}

    month = None
    while month not in months.keys():
        month = input("Enter a month (from January to June)\n(Type \'all\' for no month filter): ").lower()
        if month not in months:
            print("Invalid input!")

    month = months[month]

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = {'all': 7, 'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                   'friday': 4, 'saturday': 5, 'sunday': 6}

    day = None
    while day not in day_of_week.keys():
        day = input("Enter a day of the week (Type 'all' for no day filter): ").lower()
        if day not in day_of_week:
            print("Invalid input!")

    day = day_of_week[day]

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if month == 0:                                      # all months filter
        pass
    else:
        df = df.loc[df['Start Time'].dt.month == month]

    if day == 7:                                        # all days filter
        pass
    else:
        df = df.loc[df['Start Time'].dt.dayofweek == day]

    return df

def df_counter(df_col, converter, counter):
    """
    Args: data column, data converter, dictionary for counting

    For dealing with converting string data for counting
    Converts string column data to tally into dictionary counter

    Returns: dictionary with tallied values
    """
    for item in df_col:
        item = converter[str(item)]
        counter[item] += 1
    return counter


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_count = {'January': 0, 'Feburary': 0, 'March': 0, 'April': 0, 'May': 0, 'June': 0}
    month_int_to_str = {'1': 'January', '2': 'Feburary', '3': 'March', '4': 'April',
                        '5': 'May', '6': 'June'}
    months = df['Start Time'].dt.month

    month_count = df_counter(months, month_int_to_str, month_count)
    most_common_month = max(month_count, key=month_count.get)
    print("The most common month for traveling is {}.".format(most_common_month))

    # display the most common day of week
    day_count = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0,
                 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
    day_int_to_str = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                      '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}
    days_of_week = df['Start Time'].dt.dayofweek

    day_count = df_counter(days_of_week, day_int_to_str, day_count)
    most_common_day = max(day_count, key=day_count.get)
    print("The most common day of travel is a {}.".format(most_common_day))

    # display the most common start hour
    hour_count = {str(hour): 0 for hour in range(24)}
    hour_int_to_str = {str(hour): str(hour) for hour in range(24)}
    hour_of_day = df['Start Time'].dt.hour

    hour_count = df_counter(hour_of_day, hour_int_to_str, hour_count)
    most_common_hour = max(hour_count, key=hour_count.get)
    print("The most common hour traveling is at {}:00 local time.".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def stat_counter(item_list):
    """
    Args: list of items

    Tallies items in the list of each type

    Return: returns dictionary with each value tallied
    """
    item_count = {}
    for item in item_list:
        if item not in item_count:
            item_count[item] = 1
        else:
            item_count[item] += 1
    return item_count


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_stations = list(df['Start Station'])
    start_station_count = stat_counter(start_stations)
    most_common_start_station = max(start_station_count, key=start_station_count.get)
    print("The most common starting station is at: {}.".format(most_common_start_station))

    # display most commonly used end station

    end_stations = list(df['End Station'])
    end_station_count = stat_counter(end_stations)
    most_common_end_station = max(end_station_count, key=end_station_count.get)
    print("The most common ending station is at: {}.".format(most_common_end_station))

    # display most frequent combination of start station and end station trip

    station_grouped_count = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    station_grouped_count_sorted = station_grouped_count.sort_values('Count', ascending=False)
    start_end_station_combo_max = (station_grouped_count_sorted['Start Station'].iloc[0],
                                   station_grouped_count_sorted['End Station'].iloc[0])
    print("The most frequent starting station is at: {} \nand the ending station at: {}".format(
        *start_end_station_combo_max))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def seconds_to_humantime(seconds):
    """
    Args: seconds of time

    Function converts seconds of time to human readable time

    Return: years, months, days, hours, minutes, seconds
    """
    remaining_secs = seconds
    years = int(remaining_secs / 31104000)
    remaining_secs -= years * 31104000
    months = int(remaining_secs / 2592000)
    remaining_secs -= months * 2592000
    days = int(remaining_secs / 86400)
    remaining_secs -= days * 86400
    hours = int(remaining_secs / 3600)
    remaining_secs -= hours * 3600
    minutes = int(remaining_secs / 60)
    remaining_secs -= minutes * 60

    return years, months, days, hours, minutes, remaining_secs

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time_in_s = df['Trip Duration'].sum()
    total_travel_time_in_hms = seconds_to_humantime(total_travel_time_in_s)
    print(
        "The total travel time overall is: {} years, {} months, {} days, {} hours, {} minutes, and {} seconds.".format(
            *total_travel_time_in_hms))

    # display mean travel time

    avg_travel_time_in_s = df['Trip Duration'].mean()
    avg_travel_time_in_hms = seconds_to_humantime(avg_travel_time_in_s)
    print("The average travel time overall is: {3} hours, {4} minutes, and {5:.3f} seconds."
          .format(*avg_travel_time_in_hms))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def clean_dfcol_of_nan_values(df, df_col):
    """

    Args: dataframe, dataframe column

    Function replaces column NaN values if any with "Unknown" and tallies values

    Return dictionary of tallied types and values
    """
    if df[df_col].isnull().any() == True:
        clean_df = df[df_col].fillna(value="Unknown")
        types = list(clean_df)
        return stat_counter(types)
    return stat_counter(list(df[df_col]))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:                                       # check column exists
        user_type_count = clean_dfcol_of_nan_values(df, 'User Type')
        if 'Unknown' in user_type_count.keys():                         # check for NaN values in column
            print("There are the following user types:")
            print("=" * 35)
            print("Subscribers: \t{Subscriber}\nCustomers: \t{Customer}\nUnknown: \t{Unknown}\n".format(
                **user_type_count))
        else:
            print("There are the following user types:")
            print("=" * 35)
            print("Subscribers: \t{Subscriber}\nCustomers: \t{Customer}\n".format(**user_type_count))
    else:
        print("User Type data Missing.\n")

    # Display counts of gender
    if 'Gender' in df.columns:                                          # check column exists
        gender_type_count = clean_dfcol_of_nan_values(df, 'Gender')
        if 'Unknown' in gender_type_count.keys():                       # check for NaN values in column
            print("The following genders are:")
            print("=" * 26)
            print("Male: \t\t{Male}\nFemale: \t{Female}\nUnknown: \t{Unknown}\n".format(**gender_type_count))
        else:
            print("The following genders are:")
            print("=" * 26)
            print("Male: \t\t{Male}\nFemale: \t{Female}\n".format(**gender_type_count))
    else:
        print("Gender data Missing.\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:                                      # check column exists
        birth_years_no_nan = df['Birth Year'].dropna()                  # clean column of NaN values
        earliest_birth_year = birth_years_no_nan.sort_values().iloc[0]
        most_recent_birth_year = birth_years_no_nan.sort_values(ascending=False).iloc[0]
        most_common_birth_year = birth_years_no_nan.mode()[0]
        print("Birth data:")
        print("=" * 11)
        print("Earliest birth year: \t" + str(int(earliest_birth_year)))
        print("Most recent birth year: " + str(int(most_recent_birth_year)))
        print("Most common birth year: " + str(int(most_common_birth_year)))
    else:
        print("Birth Year data Missing.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
