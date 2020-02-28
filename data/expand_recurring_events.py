#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime


NOW = datetime.date.today()
PATH = "recurring_events.csv"
extra_cols = ["DayOfWeek", "WeekOfMonth", "Recurring"]


# Map day to 0-index int
def day_string_to_int(events) :
    for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) :
        events["DayOfWeek"] = events["DayOfWeek"] \
                                .replace(day, i)
    return events



def get_month_week_number(date_) :
    return (date_.day - 1) // 7 + 1


def create_weekly_events(events, days_ahead=60) :
    events_with_dates = pd.DataFrame()
    
    weekly_events = events[events.WeekOfMonth.isna()]
    date_list = [NOW + datetime.timedelta(days=x) \
                    for x in range(days_ahead)]
    
    for day in date_list :
        current_weekday = day.weekday()
        days_events = weekly_events[weekly_events["DayOfWeek"] \
                                        == current_weekday]
        days_events["Date"] = day.strftime("%d-%m-%Y")
        events_with_dates = events_with_dates.append(days_events)

    return events_with_dates \
            .drop(extra_cols, axis=1)


def create_monthly_events(events, days_ahead=60) :
    events_with_dates = pd.DataFrame()
    monthly_events = events[events.WeekOfMonth.notnull()]
    monthly_events["WeekOfMonth"] = monthly_events["WeekOfMonth"] \
                                        .astype('Int64')
    date_list = [NOW + datetime.timedelta(days=x) \
                    for x in range(days_ahead)]

    for day in date_list :
        week = get_month_week_number(day)
        weekday = day.weekday()
        this_week_events = monthly_events[monthly_events["WeekOfMonth"] \
                                            == week]
        days_events = this_week_events[this_week_events["DayOfWeek"] \
                                        == weekday]
        days_events["Date"] = day.strftime("%d-%m-%Y")
        events_with_dates = events_with_dates.append(days_events)

    return events_with_dates \
            .drop(extra_cols, axis=1)


def get_all_recurrers(days=60) :
    recurring_events = pd.read_csv(PATH)
    recurring_events = day_string_to_int(recurring_events)
    # Create weekly events
    weekly_events_with_dates = create_weekly_events(recurring_events, days)
    # And monthly events
    events_with_dates = weekly_events_with_dates.append(
        create_monthly_events(recurring_events, days)
    )
    return events_with_dates


if __name__ == "__main__":
    events = get_all_recurrers()
    events.to_csv("expanded_events.csv")