# Curb the Violations

Created for the KnoxvilleHackathon2019 #knxhx

# Inspiration
Challenge - curbside violations

# What it does
 * Intranet website
   * Input
   * Map
   * Stats
 * Postcards
   * Postcard automatically created for addresses that had violations
   * Can filter by number of violations
   * Postcard notes the date and type of violation, and has optional comments from pick-up crew
   * Handles edge cases of too many violations to fit on a card and empty violations records
   * Generates a single PDF containing all postcards from LaTeX
   * Has URL and QR code for site giving guidelines for putting out trash

# How we built it
 * Open source
 * Microservices
 * Containers

# Challenges we ran into

 * Excel files
 * docker on Mac
 * LaTeX for properly formatting card

# Accomplishments that we're proud of

 * simplified deployment with docker
 * tangible artifact -- printed cards

# What we learned

 * docker + PostGIS
 * printing card is expensive and wastes lots of paper

# What's next for Curb the Violations

 * fix hiccups
 * refactoring database
 * full integration
 * advanced web-based dashboard
