# meeting-tracker

## Contents
[Introduction](#introduction)

[Context](#context)

[Approach](#approach)

## Introduction

This spike uses the Google Api to develop metrics on calendar events. 

It seeks to answer the following questions:

* How many meetings exist in a given calendar?
* How many events are created with an agenda?
* Who organises meetings?
* How long do meetings last?

This is achieved by creating a standard meeting title format based on the [Karma Commit Convention](http://karma-runner.github.io/3.0/dev/git-commit-msg.html).

## Context

Meetings can be pain but they don't have to be. I recently wrote about it [here](https://sarahseewhy.github.io/2019/02/01/reflection-week-5.html).

I wanted to create a way to start measuring how my team was investing their collaboration energy. Through measuring we could begin to make improvements.

We've been experimenting with using the Karma Commit Convention (`<type>(scope):<subject>`) on my team's meeting invites which creates a standard meeting format, one that's a lot easier to query and measure.

Right now for example, we have the following:
```
meet(graphite): Develop SLIs
retro(team): Last iteration
huddle(slackbot-spike): How to productionise?
1-1(sarah): Discuss meeting-tracker project
``` 

We're still working on allowed `type` values.

Hopefully this will generate some interesting information and conversations.

## Approach

I'm following a few resources to get this spike working:

- [Google Calendar API's Python Quickstart](https://developers.google.com/calendar/quickstart/python)
- [Google Calendar's API Docs](https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/)
- [Google Calendar's API Client Library](https://developers.google.com/api-client-library/python/apis/calendar/v3)
- [Parsing Google Calendar events with Python](https://qxf2.com/blog/google-calendar-python/)
- 