import time
import pandas as pd
import numpy as np
#author: Sanem Kocak Balkan
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ["chicago", "new york city", "washington"]

months = ["january", "february", "march", "april", "may", "june", "all"]

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). 
    city = input("Please enter one of these cities; chicago, new york city, washington: ").lower()
    if city in cities:
        is_city_correct = True
    else:
        is_city_correct = False
    while is_city_correct == False:
        city = input("Please enter one of these cities; chicago, new york city, washington: ").lower()
        if city in cities:
            break
        else:
            print("Please try again enter one of these cities; chicago, new york city, washington: ")
   # get user input for month (all, january, february, ... , june) 
    month = input("Please enter all or a specific month from; january, february, march, april, may, june: ").lower()
    if month in months:
        month_filter_correct = True
    else:
        month_filter_correct = False
    while month_filter_correct == False:
        month = input("Please enter all or a specific month from january, february, march, april, may, june: ").lower()
        if month in months:
            break
        else:
            print("Please try again enter one of these months or enter all for no filter: ")
 # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter all or a specific day from these days or enter all if you dont want to limit to a single day: ").lower()
    if day in days:
        day_filter_correct = True
    else:
        day_filter_correct = False
    while day_filter_correct == False:
        day= input("Please enter all or a specific day from these days or enter all if you dont want to limit to a single day: ").lower()
        if day in days:
            break
        else:
            print("Please try again enter one of these days or enter all for no filter: ")
    
    print('-'*40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    month = df['Start Time'].dt.month
    popular_month = month.mode()[0]    
    print('Most Popular Start Hour:', popular_month)
    
    # display the most common day of week
    weekday_name = df['Start Time'].dt.weekday_name
    popular_day_of_week = weekday_name.mode()[0]
    print('Most common day of week: ', popular_day_of_week)

    # display the most common start hour
    hour = df['Start Time'].dt.hour
    popular_start_hour = hour.mode()[0]
    print('Most frequent start hour: ', popular_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #lndisplay most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print("The most popular start station is {}.".format(popular_start_station))

    #display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("The most polular end station is {}.".format(popular_end_station))

    #display most frequent combination of start station and end station trip
    both_start_end_stations = df['Start Station'] + "," + df['End Station']
    common_station = both_start_end_stations.value_counts().idxmax()
    print('Most frequent used combinations are:\n{} \nto\n{}'.format(common_station.split(',')[0], common_station.split(',')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    travel_time = df["Trip Duration"]
    total_travel_time = travel_time.sum()
    print("The total travel time is {} seconds.".format(total_travel_time))

    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    #Display counts of gender

    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest year of birth: " + str(earliest_birth_year))
        print("\nMost recent year of birth: " + str(most_recent_birth_year))
        print("\nMost common year of birth: " + str(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """Displays raw data if user wants to see."""
    inputs = ['yes', 'no']
    line_number = 0
    user_input = input('Do you want to see raw data? Enter yes or no.')
    
    while True:
        if user_input not in inputs:
            user_input = input('Do you want to see raw data? Enter yes or no.').lower() 
        elif user_input.lower() == 'yes': 
            print(df.iloc[line_number : line_number + 5])
            line_number += 5
            user_input = input('Do you want to see more raw data? Enter yes or no.')
        else:
            break 

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
