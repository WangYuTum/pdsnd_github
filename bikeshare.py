import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
CITIES = ['chicago', 'new york city', 'washington']
DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'all']
FILTERS = ['month', 'day', 'both', 'none']


def get_city_filter():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to filter by
    """


    valid = False
    city = None
    # get user input for city (chicago, new york city, washington).
    while not valid:
        try:
            city = input('Which city (chicago, new york city, washington) would you like to explore? \n')
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if city == 'all':
                print('You can only explore one city at a time.')
            elif city in CITIES:
                valid = True
            else:
                print('Invalid city (case censitive)! Press [Control-C] if you want to exit program.')

    return city


def get_filter_choice():
    """
    Asks user which filters to apply among: month, day, both, none'

    Returns:
        (str) filter_by - the filter to apply to 
    """

    valid = False
    filter_by = None
    while not valid:
        try:
            filter_by = input('Would you like to filter the data by month, day, or both, or none? Type none if you don\'t want to filter. \n')
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if filter_by in FILTERS:
                valid = True
            else:
                print('Invalid filter. Please choose among: {}'.format(FILTERS))

    return filter_by


def get_month_filter():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """

    valid = False
    month = None

    # get user input for month (all, january, february, ... , june)
    while not valid:
        try:
            month = input('Which month (all, january, february, ... , june) would you like to explore? \n')
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if month in MONTHS:
                valid = True
            else:
                print('Invalid month (case censitive)! Press [Control-C] if you want to exit program.')

    return month


def get_day_filter():
    """
    Asks user to specify a day to analyze.

    Return:
        (str) day - name of the day to filter by, or "all" to apply no day filter
    """

    valid = False
    day = None

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while not valid:
        try:
            day = input('Which day of the week (all, monday, tuesday, ... sunday) would you like to explore? \n')
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if day in DAYS:
                valid = True
            else:
                print('Invalid day (case censitive)! Press [Control-C] if you want to exit program.')

    return day


def get_input_int(lower, upper):
    """
    Get an integer from user input.

    Arg(s):
        (int) lower - the lower bound of the integer
        (int) higher - the upper bound of the integer
    Return:
        (int) res - the acquired integer from the user which satisfies the specified boundaries
    """

    valid = False
    step = None
    while not valid:
        try:
            step = int(input('How many rows would you like to display at a time? (Input must be an integer in \
range [{}, {}] inclusive) \n'.format(lower, upper)))
        except ValueError as e:
            print('Error: {}'.format(e))
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if step >= lower and step <= upper:
                valid = True
            else:
                print('Input value {} is not in range [{}, {}]'.format(step, lower, upper))

    return step


def display_raw_data(df):
    """
    Asks user to display raw data. User must specify a stepsize first.

    Arg(s):
        df - DataFrame
    """

    # ask user whether or not show the raw data
    valid = False
    show_raw = None
    while not valid:
        try:
            show_raw = input('Would you like to explore the raw data? Enter yes or no\n')
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if show_raw == 'yes':
                show_raw = True
                valid = True
            elif show_raw == 'no':
                show_raw = False
                valid = True
            else:
                print('Invalid inputs! Press [Control-C] if you want to exit program.')

    if not show_raw:
        return

    # ask user for a stepsize of rows, constraint the stepsize in range [1, 10] inclusive
    step = get_input_int(1, 10)

    # print [stepsize] rows at a time
    iterator = df.iterrows()
    print_rows(iterator, step) # show the first step rows
    exit_flag = False
    user_input = None
    while not exit_flag:
        try:
            user_input = input('Show more {} rows? Enter y or n\n'.format(step))
        except KeyboardInterrupt:
            print('\nUser Interrupt: Exit Program!')
            sys.exit()
        else:
            if user_input != 'y' and user_input != 'n':
                print('Invalid inputs! Press [Control-C] if you want to exit program.')
            elif user_input == 'n':
                exit_flag = True
            else:
                print_rows(iterator, step) # show more rows

    print('-'*40)


def print_rows(iterator, stepsize):
    """
    Display rows using iterator from a DataFrame

    Arg(s):
        iterator - a row iterator of a DataFrame
        stepsize - number of rows to display
    """
    count = 0
    rows = []
    for row_index, row_data in iterator:
        count += 1
        rows.append(row_data)
        if count == stepsize:
            break

    if len(rows) == 0:
        return

    print(pd.DataFrame(rows))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get city filter
    city = get_city_filter()

    # get filter choices from the user
    filter_by = get_filter_choice()

    # get month and day filter values
    month = None
    day = None

    if filter_by == 'none':
        month, day = 'all', 'all'
    elif filter_by == 'both':
        month = get_month_filter()
        day = get_day_filter()
    elif filter_by == 'month':
        month = get_month_filter()
        day = 'all'
    else:
        day = get_day_filter()
        month = 'all'

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

    # # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df = df.iloc[:, 1:] # ignore the first unnamed column

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() ## in pandas version >= 0.23.0

    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month = MONTHS.index(month) + 1
    
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
    mon_id_list = list(df['month'].mode())
    mon_name_list = []
    for mon_id in mon_id_list:
        mon_name_list.append(MONTHS[mon_id - 1])

    print('The most common month(s): {}'.format(mon_name_list))

    # display the most common day of week
    day_name_list = list(df['day_of_week'].mode())
    print('The most common day(s) of week: {}'.format(day_name_list))

    # display the most common start hour
    hour_list = list(df['Start Time'].dt.hour.mode())
    print('The most common start hour(s): {}'.format(hour_list))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    stations_list = list(df['Start Station'].mode())
    print('The most commonly used start station(s): {}'.format(stations_list))

    # display most commonly used end station
    stations_list = list(df['End Station'].mode())
    print('The most commonly used end station(s): {}'.format(stations_list))

    # display most frequent combination of start station and end station trip
    pd_start_end = df['Start Station'] + '$$$$' + df['End Station']
    combined_list = list(pd_start_end.mode())
    start_end_list = []
    for item in combined_list:
        tmp = item.split('$$$$')
        start_end_list.append(tmp)
    print('The most frequent combination of start and end station(s):')
    for item in start_end_list:
        print('From \'{}\' To \'{}\''.format(item[0], item[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_seconds = df['Trip Duration'].sum()
    hours = sum_seconds // 3600
    minutes = (sum_seconds - hours * 3600) // 60
    seconds = sum_seconds - hours * 3600 - minutes * 60
    print('Total travel time: {} [hours], {} [minutes], {} [seconds].'.format(hours, minutes, seconds))

    # display mean travel time
    avg_seconds = df['Trip Duration'].mean()
    minutes = avg_seconds // 60
    seconds = avg_seconds - minutes * 60
    print('Mean travel time: {} [minutes], {} [seconds].'.format(minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_stat = df['User Type'].value_counts(dropna=False)
    nan_stat = user_stat[pd.isnull(user_stat.index)]
    nan_count = 0
    if not nan_stat.empty:
        nan_count = nan_stat[0]
    print('User type statistics: ')
    print('Count of {} users: {}'.format('Subscriber', user_stat.get('Subscriber', 0)))
    print('Count of {} users: {}'.format('Customer', user_stat.get('Customer', 0)))
    print('Count of {} users: {}'.format('Unknown/NaN', nan_count))

    columns = df.columns
    if 'Gender' in columns and 'Birth Year' in columns:
        # Display counts of gender
        gender_stat = df['Gender'].value_counts(dropna=False)
        nan_stat = gender_stat[pd.isnull(gender_stat.index)]
        nan_count = 0
        if not nan_stat.empty:
            nan_count = nan_stat[0]
        print('User gender statistics: ')
        print('Count of {} users: {}'.format('Female', gender_stat.get('Female', 0)))
        print('Count of {} users: {}'.format('Male', gender_stat.get('Male', 0)))
        print('Count of {} users: {}'.format('Unknown/NaN', nan_count))

        # Display earliest, most recent, and most common year of birth
        year_min = df['Birth Year'].min()
        year_max = df['Birth Year'].max()
        year_mode = list(df['Birth Year'].mode())
        print('Birth Year statistics: ')
        print('The earliest year of birth: {}'.format(year_min))
        print('The most recent year of birth: {}'.format(year_max))
        print('The most common year(s) of birth (except for NaN value): {}'.format(year_mode))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # display raw data if user asks to
        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
