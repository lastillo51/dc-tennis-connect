# DC Tennis Connect — Court Data Source Research

## 1. Research Objective

Identify reliable, authorized public information that can support tennis court discovery, published operating schedules, known restrictions, and Google Maps navigation in Washington, D.C.

The application will use this information to help players coordinate matches around potential playing times.

## 2. Research Questions

### Court Locations

- Which public tennis courts are available in Washington, D.C.?
- Are official names, addresses, and geographic coordinates published?
- Can court locations and accessible entrances be verified?

### Court Scheduling

- Are court operating hours published?
- Are operating hours seasonal?
- Are there holiday restrictions?
- Are maintenance closures publicly documented?
- Which courts operate on a first-come, first-served basis?
- Which courts support reservations?
- Are public reservation schedules accessible?
- How frequently are schedules updated?

### Data Access

- Are downloadable datasets available?
- Are official APIs available?
- Is automated retrieval permitted?
- Are there usage limits or licensing restrictions?
- Can the information be reused in a public application?

## 3. Candidate Sources

### DC Department of Parks and Recreation

Website: https://dpr.dc.gov/

Investigate:

- Tennis court directories.
- Court operating hours.
- Reservation policies.
- Facility closures.
- Seasonal restrictions.

### DC Open Data

Website: https://opendata.dc.gov/

Investigate:

- Recreation facility datasets.
- Tennis court locations.
- Facility coordinates.
- Published facility attributes.

### Official Reservation Systems

Investigate whether public reservation schedules are accessible through authorized methods.

Do not assume that reservation information is available through a public API.

### Google Maps

Google Maps will be used for navigation rather than as the authoritative source of court schedules.

Official documentation:

https://developers.google.com/maps/documentation/urls/guide

## 4. Data Classification

| Classification | Meaning |
|---|---|
| Published Open Hours | The facility is scheduled to be open |
| Verified Reservable Slot | An authorized source identifies an open booking slot |
| Published Reservation | An authorized source identifies a reserved period |
| First-Come, First-Served | Access depends on physical occupancy |
| Published Closure | Court is unavailable due to a documented closure |
| Unknown | Insufficient information to determine scheduling status |

## 5. Data Quality Requirements

Each court record should include, where available:

- Court name.
- Address.
- Latitude and longitude.
- Number of courts.
- Surface type.
- Published operating hours.
- Reservation policy.
- Known closures.
- Information source.
- Last verification date.

Each scheduling record should include:

- Court identifier.
- Applicable date or recurring schedule.
- Start time.
- End time.
- Time zone.
- Original source.
- Verification timestamp.
- Scheduling classification.

All scheduling times should be interpreted using the Washington, D.C. local time zone.

## 6. Data Collection Strategy

### Initial MVP

Begin with a small set of manually verified public courts.

Collect:

- Court names and locations.
- Published operating hours.
- Reservation policies.
- Known closures.
- Original source URLs.
- Last verification timestamps.

Do not label a court as physically available solely because it is open.

### Later Development

Evaluate authorized automated imports from public datasets or official APIs.

Potential capabilities include:

- Scheduled data refreshes.
- Change detection.
- Data freshness monitoring.
- Alerts for published schedule changes.

Automated retrieval shall only be implemented when permitted by the data provider.

## 7. Scheduling Implications

Public schedule information will help players select potential match times.

The application shall not:

- Guarantee physical court availability.
- Automatically reserve courts.
- Treat player-created matches as official reservations.
- Assume that all published open hours are unreserved.

When reliable reservation information is unavailable, the interface should communicate that the court may be occupied.

## 8. Google Maps Validation

Before publishing a court location:

1. Verify its official address.
2. Confirm coordinates where available.
3. Check that the Google Maps destination identifies the correct facility.
4. Verify the nearest appropriate entrance where practical.
5. Record any location discrepancies.

## 9. Research Findings

No court schedule sources have been verified yet.

Findings will be documented as official sources are investigated.

## 10. Key Risks

### Incomplete Reservation Data

Published operating hours may not reveal whether a court is reserved or occupied.

### Outdated Public Information

Court hours and restrictions may change without immediate notice.

### Location Accuracy

Large parks may contain tennis courts far from the park's main address.

### Third-Party Restrictions

Some public-facing reservation systems may prohibit automated data collection.

## 11. Next Research Actions

1. Identify a small sample of DC public tennis courts.
2. Verify official locations and operating hours.
3. Document reservation policies.
4. Determine whether authorized reservation schedules are accessible.
5. Record source URLs and update frequency.
6. Evaluate whether the collected information is sufficient for the initial scheduling calendar.