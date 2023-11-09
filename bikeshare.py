import time

import numpy as np
import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

# was generated with `df['day_of_week'].unique()` statement then add `All`
DAYS_OPTION = [
    "all",
    "friday",
    "thursday",
    "wednesday",
    "monday",
    "tuesday",
    "saturday",
    "sunday",
]

# was generated with `df['month'].unique()` statement then add `All`
MONTHS_OPTIONS = ["all", "june", "may", "january", "march", "april", "february"]


def handle_invalid_input(input_question: str, checklist: list) -> str:
    """
    An helper function, helps to reduce code repetition.
    It handles the invalid inputs entered by users.

    Args:
        (str) input_question - question that prompt to users.
        (list) checklist - list of values to check for input validation.

    Returns:
        (str) choice - what the user entered at the prompt.
    """
    choice = input(input_question).lower().strip()
    # handle invalid city inputs
    while choice not in checklist:
        print("Invalid input! Please, try again!\n\n")
        choice = input(input_question).lower().strip()

    if choice == "all":
        return "all"
    return choice


def get_filters() -> tuple:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    month = "all"
    day = "all"
    city = handle_invalid_input(
        "Would you like to see data for Chicago, New York City, or Washington? ",
        CITY_DATA,
    )
    # get user input for month (all, january, february, ... , june)
    filter_choice = (
        input(
            "Would you like to filter the data by month, day, both or not at all? Type 'none' for no time filter: "
        )
        .lower()
        .strip()
    )

    if filter_choice == "month":
        month = handle_invalid_input(
            "Which month - January, February, March, April, May, or June? ",
            MONTHS_OPTIONS,
        )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filter_choice == "day":
        day = handle_invalid_input(
            "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ",
            DAYS_OPTION,
        )

    elif filter_choice == "both":
        month = handle_invalid_input(
            "Which month - January, February, March, April, May, or June? ",
            MONTHS_OPTIONS,
        )
        day = handle_invalid_input(
            "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ",
            DAYS_OPTION,
        )

    else:
        print("-" * 40)
        return city, filter_choice

    print("-" * 40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load the city data
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the "Start Time" column to datetime object
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extracts new columns from the "Start Time" column (feature extraction)
    df["month"] = df["Start Time"].dt.month_name()
    df["day_of_week"] = df["Start Time"].dt.day_name()

    if month != "all":
        month = df["month"] == month.title()
    else:
        month = df.notna()

    if day != "all":
        day = df["day_of_week"] == day.title()
    else:
        day = df.notna()

    df = df[month][day]

    return df


def time_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    print("The most frequent month of travel: {}".format(df["month"].mode()[0]))

    # display the most common day of week
    print(
        "The most frequent day of the week of travel: {}".format(
            df["day_of_week"].mode()[0]
        )
    )

    # display the most common start hour
    print("The most common start hour: {}".format(df["Start Time"].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station: {}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station: {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    print(
        "The most frequent combination of start station and end station trip: {}".format(
            (df["Start Station"] + " - " + df["End Station"]).mode()[0]
        )
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("Total travel time: {} seconds".format(df["Trip Duration"].sum()))

    # display mean travel time
    print("Average travel time: {} seconds".format(df["Trip Duration"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df: pd.DataFrame) -> None:
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    print("\n")
    print("Types of user:")
    for user, count in zip(df["User Type"].unique(), df["User Type"].value_counts()):
        print(f"{user}: {count}")

    # Display counts of gender
    print("\n")
    print("Gender:")
    for gender, count in zip(df["Gender"].unique(), df["Gender"].value_counts()):
        print(f"{gender}: {count}")

    # Display earliest, most recent, and most common year of birth
    print("\n")
    print("The earliest year of birth: {}\n".format(int(np.min(df["Birth Year"]))))
    print("The most recent year of birth: {}\n".format(int(np.max(df["Birth Year"]))))
    print("The common year of birth: {}\n".format(int(df["Birth Year"].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_data(df: pd.DataFrame, display_stats: str) -> None:
    buffer = 0
    while display_stats.lower() == "yes":
        print(df.iloc[buffer : buffer + 5, :])
        buffer += 5
        display_stats = input(
            "\nWould you like to see the next 5 line of the data? Enter yes or no: "
        )


def main() -> None:
    while True:
        filtered_data = get_filters()
        if len(filtered_data) == 3:
            city, month, day = filtered_data
        else:
            city = filtered_data[0]
            month = "all"
            day = "all"

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        try:
            user_stats(df)
        except KeyError:
            print("Sorry! No statistics on user gender.")

        display_stats = input(
            "\nWould you like to see 5 line of the data? Enter yes or no: "
        )
        if display_stats.lower() != "yes":
            break
        else:
            display_data(df, display_stats)

        restart = input("\nWould you like to restart? Enter yes or no: \n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
